from abc import ABC, abstractmethod


class StatisticsBase(ABC):
    @abstractmethod
    def __init__(self, figi, *args, **kwargs):
        pass
        
    @abstractmethod
    async def add_order(self):
        pass
        
    @abstractmethod
    async def update_order_status(self):
        pass
