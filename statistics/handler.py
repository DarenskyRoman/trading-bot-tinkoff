from statistics.sqlite_stat import SQLiteHandler
from statistics.telegram_bot import TelegramHandler
from errors import HandlerError


handlers = {
    "sqlite": SQLiteHandler,
    "telegram": TelegramHandler  
}


def handlerBuilder(handler_name, *args, **kwargs):
    if handler_name not in handlers:
        raise HandlerError(handler_name, "can't build handler")
    else:
        return handlers[handler_name](*args, **kwargs)
        
        
class StatsHandler:
    def __init__(self, handler, params):
        self.handler = handlerBuilder(handler, **params)
    
    async def add_order(self, **kwargs):
        await self.handler.add_order(**kwargs)

    async def update_order_status(self, **kwargs):
        await self.handler.update_order_status(**kwargs)
