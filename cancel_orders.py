import logging
import asyncio
import os


from tinkoff.invest import AsyncClient
from dotenv import load_dotenv


import strategies.orders_handler as orders_handler


logger = logging.getLogger(__name__)

load_dotenv()
INVEST_TOKEN = os.getenv("INVEST_TOKEN")
SANDBOX = bool(os.getenv("SANDBOX"))


async def cancel_orders():
    if SANDBOX == False:
        client = await AsyncClient(token=INVEST_TOKEN).__aenter__()
        
        response = await orders_handler.get_accounts(client, SANDBOX)
        account, *_ = response.accounts
        ACCOUNT_ID = account.id
        
        logger.info("Orders: %s", await orders_handler.get_orders(client, SANDBOX, account_id=ACCOUNT_ID))
        await client.cancel_all_orders(account_id=ACCOUNT_ID)
        logger.info("Orders: %s", await orders_handler.get_orders(client, SANDBOX, account_id=ACCOUNT_ID))
        
    else:
        return
        
        
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(loop.create_task(cancel_orders()))
