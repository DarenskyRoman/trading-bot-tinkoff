from abc import ABC, abstractmethod


class StrategyBase(ABC):
    @abstractmethod
    def __init__(self, figi, *args, **kwargs):
        pass
        
    @abstractmethod
    async def start(self):
        pass
        
    @abstractmethod
    async def ensure_market_open(self):
        pass
        
    @abstractmethod
    async def post_order(self):
        pass
