import json
from errors import InstrumentsError


def get_instruments(filename = "instruments.json"):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            return data
    except Exception:
        raise InstrumentsError(filename)