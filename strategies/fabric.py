from errors import StrategyError
from strategies.test.strategy import testStrategy
from strategies.sma.strategy import smaStrategy


strategies = {
    "sma": smaStrategy,
    "test": testStrategy  
}


def strategyBuilder(strategy_name: str, figi: str, *args, **kwargs):
    if strategy_name not in strategies:
        raise StrategyError(strategy_name)
    else:
        return strategies[strategy_name](figi=figi, *args, **kwargs)