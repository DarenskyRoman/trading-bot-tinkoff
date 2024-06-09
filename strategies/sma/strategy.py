import asyncio
import logging
from datetime import timedelta
from uuid import uuid4


from tinkoff.invest.grpc.instruments_pb2 import INSTRUMENT_ID_TYPE_FIGI
from tinkoff.invest.services import MarketDataStreamManager
from tinkoff.invest.exceptions import InvestError
from tinkoff.invest.utils import now
from tinkoff.invest.grpc.orders_pb2 import (
    ORDER_DIRECTION_SELL,
    ORDER_DIRECTION_BUY,
    ORDER_TYPE_MARKET,
)
from tinkoff.invest import (
    AsyncClient,
    AioRequestError,
    CandleInstrument,
    CandleInterval,
    OrderExecutionReportStatus
)


import strategies.orders_handler as orders_handler
from strategies.strategy_base import StrategyBase
from errors import CurrencyError
from statistics.handler import StatsHandler


logger = logging.getLogger(__name__)

FINAL_ORDER_STATUSES = [
    OrderExecutionReportStatus.EXECUTION_REPORT_STATUS_CANCELLED,
    OrderExecutionReportStatus.EXECUTION_REPORT_STATUS_REJECTED,
    OrderExecutionReportStatus.EXECUTION_REPORT_STATUS_FILL,
    OrderExecutionReportStatus.EXECUTION_REPORT_STATUS_PARTIALLYFILL
]


class smaStrategy(StrategyBase):
    def __init__(self, figi: str, client: AsyncClient, accountID = None, *args, **kwargs):
        assert kwargs["long_ma"] > kwargs["short_ma"]
        self.figi = figi
        self.client = client
        self.accountID = accountID
        self.long_ma = kwargs["long_ma"]
        self.short_ma = kwargs["short_ma"]
        self.quantity = kwargs["quantity"]
        self.sandbox = kwargs["sandbox"]
        self.signal = None
        self.instrument_info = None
        self.prices = None
        self.candle_interval = CandleInterval.CANDLE_INTERVAL_1_MIN
        self.market_data_stream: MarketDataStreamManager = None
        self.stats_handler = StatsHandler(kwargs["stats_handler"], kwargs["stats_config"])
        
        
    async def start(self):
        if self.accountID is None:
            try:
                self.accountID = (await orders_handler.get_accounts(self.client, self.sandbox)).accounts.pop().id

            except AioRequestError as are:
                logger.error(f"Error taking account id. Stopping strategy. {are}")
                return
        await self.main_cycle()
        
        
    async def main_cycle(self):
        self.prices = await self.get_historical_data()
        self.signal = await self.long_avg() > await self.short_avg()
        await self.stream_subscribtion()
        while True:
            try:
                await self.ensure_market_open()
                await self.get_instrument_info()
                
                async for market_data in self.market_data_stream:
                    logger.debug(f'Received market_data')
                    if market_data.candle:
                        await self.on_update(market_data.candle)
                    if market_data.trading_status and market_data.trading_status.market_order_available_flag:
                        logger.info(f'Trading is limited. Current status: {market_data.trading_status}')
                    await asyncio.sleep(60)

            except AioRequestError as are:
                logger.error("Client error %s", are)

            except InvestError as error:
                logger.info(f'Caught exception {error}, stopping trading')
                self.market_data_stream.stop()
                
                
    async def ensure_market_open(self):
        trading_status = await self.client.market_data.get_trading_status(figi=self.figi)
        while not (
            trading_status.market_order_available_flag and trading_status.api_trade_available_flag
        ):
            logger.debug(f"Waiting for the market to open. figi={self.figi}")
            await asyncio.sleep(60)
            trading_status = await self.client.market_data.get_trading_status(figi=self.figi)
            
            
    async def stream_subscribtion(self):
        logger.debug(f"Starting subscription to {self.figi}")
        self.market_data_stream: MarketDataStreamManager = self.client.create_market_data_stream()
        self.market_data_stream.candles.subscribe([
            CandleInstrument(
                figi=self.figi,
                interval=self.candle_interval)
        ])
        logger.debug(f'Subscribed to MarketDataStream, interval: {self.candle_interval}')
        
        
    async def get_instrument_info(self):
        self.instrument_info = (
            await self.client.instruments.get_instrument_by(id_type=INSTRUMENT_ID_TYPE_FIGI, id=self.figi)
        ).instrument
        
        
    async def get_last_price(self):
        last_price = await self.client.market_data.get_last_prices(figi=[self.figi])
        return last_price.last_prices[0].price
        
        
    async def get_historical_data(self):
        logger.debug(f"Start getting historical data for {self.long_ma} minutes back from now. figi={self.figi}",)
        candles = []
        async for candle in self.client.get_all_candles(
            figi=self.figi,
            from_=now() - timedelta(minutes=self.long_ma),
            to=now(),
            interval=CandleInterval.CANDLE_INTERVAL_1_MIN,
        ):
            if candle not in candles:
                if candle.is_complete:
                    candles.append(candle.close)
        return(candles)
        
        
    async def on_update(self, candle):
        self.prices = self.prices[1:] + [candle.close]
        
        new_signal = await self.long_avg() > await self.short_avg()

        try:

            balance = (
                await orders_handler.get_portfolio(self.client, self.sandbox, account_id = self.accountID)
                ).total_amount_currencies
            
            if balance.currency != self.instrument_info.currency:
                raise CurrencyError(balance.currency)
                        
            if new_signal != self.signal:
                if new_signal:
                    order = await self.post_order(self.quantity, ORDER_DIRECTION_BUY, ORDER_TYPE_MARKET)
                    await self.add_stats(order)
                else:
                    order = await self.post_order(self.quantity, ORDER_DIRECTION_SELL, ORDER_TYPE_MARKET) 
                    await self.add_stats(order)

                self.signal = new_signal

        except Exception as e:
            logger.debug(f"Can't get portfolio currency balance: {e}")
            raise Exception(f"Can't get portfolio currency balance: {e}")
            
            
    async def add_stats(self, order):
        try:
            order_state = await (orders_handler.get_order_state(
                self.client, self.sandbox, account_id=self.accountID, order_id=order.order_id))
        except AioRequestError:
            return
        
        await self.stats_handler.add_order(
            order_id=order.order_id,
            figi=order_state.figi,
            order_direction=str(order_state.direction),
            price=order_state.total_order_amount,
            quantity=order_state.lots_requested,
            status=str(order_state.execution_report_status)
        )

        while order_state.execution_report_status not in FINAL_ORDER_STATUSES:
            await asyncio.sleep(10)
            order_state = await (orders_handler.get_order_state(
                self.client, self.sandbox, account_id=self.accountID, order_id=order.order_id))
            
        await self.stats_handler.update_order_status(
            order_id=order.order_id, status=str(order_state.execution_report_status)
        )
        
        
    async def post_order(self, quantity, direction, order_type):
        return await orders_handler.post_order(
            client = self.client,
            sandbox = self.sandbox,
            order_id=str(uuid4()),
            figi=self.figi,
            direction=direction,
            quantity=int(quantity),
            order_type=order_type,
            account_id=self.accountID
        )
        
        
    async def long_avg(self):
        result = self.prices[0]
        
        for price in self.prices[1:]:
            result += price
        
        result.units = result.units // self.long_ma
        result.nano = result.nano // self.long_ma
        
        return result
        
        
    async def short_avg(self):
        result = self.prices[-self.short_ma]
        
        for price in self.prices[-self.short_ma+1:]:
            result += price
        
        result.units = result.units // self.long_ma
        result.nano = result.nano // self.long_ma
        
        return result
