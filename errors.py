class InstrumentsError(Exception):
    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return f"Error while reading {self.filename}"
    

class StrategyError(Exception):
    def __init__(self, strategy_name):
        self.strategy_name = strategy_name

    def __str__(self):
        return f"Strategy {self.strategy_name} is not found"
    

class CurrencyError(Exception):
    def __init__(self, currency):
        self.currency = currency

    def __str__(self):
        return f"Currency {self.currency} not found in portfolio"
    
    
class HandlerError(Exception):
    def __init__(self, handler_name, error):
        self.handler_name = handler_name
        self.error = error

    def __str__(self):
        return f"Error with {self.handler_name} handler: {self.error}"
