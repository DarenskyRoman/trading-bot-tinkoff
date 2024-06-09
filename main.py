import asyncio
import logging
import os


import instruments
from strategies.fabric import strategyBuilder
from tinkoff.invest import AsyncClient
from dotenv import load_dotenv 


logging.basicConfig(filename="logs.log", format="%(asctime)s %(levelname)s:%(message)s", level=logging.DEBUG)
logging.getLogger(__name__)


load_dotenv()
TOKEN = os.getenv("INVEST_TOKEN")
SANDBOX = os.getenv("SANDBOX")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")

if ACCOUNT_ID == "?":
    ACCOUNT_ID = None
    
    
async def run():    
    client = await AsyncClient(token=TOKEN).__aenter__()
    tasks = []
    
    for config in instruments.get_instruments("instruments.json")["instruments"]:
        strategy = strategyBuilder(
            figi = config["figi"],
            strategy_name = config["strategy"]["name"],
            client = client,
            accountID = ACCOUNT_ID,
            sandbox = SANDBOX,
            stats_handler = config["statistics"]["handler"],
            stats_config = config["statistics"]["parameters"],
            **config["strategy"]["parameters"],
        )
        tasks.append(asyncio.create_task(strategy.start()))
    await asyncio.wait(tasks)
    
    
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(loop.create_task(run()))
