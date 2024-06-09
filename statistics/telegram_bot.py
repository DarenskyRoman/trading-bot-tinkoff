import logging
import sys
from pprint import pformat


from aiogram import Bot, types
from aiogram import Dispatcher
from aiogram.filters.command import Command


from statistics.statistics_base import StatisticsBase
from cancel_orders import cancel_orders


logger = logging.getLogger(__name__)
dp = Dispatcher()


class TelegramHandler(StatisticsBase):
    def __init__(self, token, chat_id):
        self.__bot = Bot(token=token)
        self.__chat_id = chat_id
        
    async def add_order(self, **kwargs):
        logger.debug("Sending order info to telegram")
        text = pformat(kwargs)
        text = f"Order info:\n{text}"
        await self.__bot.send_message(chat_id=self.__chat_id, text=text)
        logger.debug(f"Telegram message has been sent.")
        
    async def update_order_status(self, **kwargs):
        logger.debug("Sending order info to telegram")
        text = pformat(kwargs)
        text = f"Order status update:\n{text}"
        await self.__bot.send_message(chat_id=self.__chat_id, text=text)
        logger.debug(f"Telegram message has been sent.")
