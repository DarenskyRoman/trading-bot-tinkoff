from strategies.strategy_base import StrategyBase
import logging


logger = logging.getLogger(__name__)


class testStrategy(StrategyBase):
    def __init__(self, figi: str, *args, **kwargs):
        super().__init__(figi, *args, **kwargs)
        self.figi = figi
        
    async def start(self):
        logger.debug(f"I'm test strategy for figi {self.figi}")
        
    async def ensure_market_open(self):
        pass
        
    async def post_order(self):
        pass
