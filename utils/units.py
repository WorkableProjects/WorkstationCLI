def pressure_to_atm(value: float, unit: str) -> float:
    unit = unit.lower().strip()
    if unit in ["atm", "atmosphere"]:
        return value
    elif unit in ["mmhg", "torr"]:
        return value / 760.0
    elif unit in ["kpa", "kilopascal"]:
        return value / 101.325
    elif unit in ["pa", "pascal"]:
        return value / 101325.0
    elif unit in ["bar"]:
        return value / 1.01325
    else:
        raise ValueError(f"Unsupported pressure unit: '{unit}'")

def atm_to_pressure(value_atm: float, unit: str) -> float:
    unit = unit.lower().strip()
    if unit in ["atm", "atmosphere"]:
        return value_atm
    elif unit in ["mmhg", "torr"]:
        return value_atm * 760.0
    elif unit in ["kpa", "kilopascal"]:
        return value_atm * 101.325
    elif unit in ["pa", "pascal"]:
        return value_atm * 101325.0
    elif unit in ["bar"]:
        return value_atm * 1.01325
    else:
        raise ValueError(f"Unsupported pressure unit: '{unit}'")

def temp_to_kelvin(value: float, unit: str) -> float:
    unit = unit.lower().strip()
    if unit in ["k", "kelvin"]:
        return value
    elif unit in ["c", "celsius", "°c"]:
        return value + 273.15
    elif unit in ["f", "fahrenheit", "°f"]:
        return (value - 32.0) * (5.0 / 9.0) + 273.15
    else:
        raise ValueError(f"Unsupported temperature unit: '{unit}'")

def kelvin_to_temp(value_k: float, unit: str) -> float:
    unit = unit.lower().strip()
    if unit in ["k", "kelvin"]:
        return value_k
    elif unit in ["c", "celsius", "°c"]:
        return value_k - 273.15
    elif unit in ["f", "fahrenheit", "°f"]:
        return (value_k - 273.15) * (9.0 / 5.0) + 32.0
    else:
        raise ValueError(f"Unsupported temperature unit: '{unit}'")

def volume_to_liters(value: float, unit: str) -> float:
    unit = unit.lower().strip()
    if unit in ["l", "liter", "liters"]:
        return value
    elif unit in ["ml", "milliliter", "milliliters"]:
        return value / 1000.0
    elif unit in ["cm3", "cc"]:
        return value / 1000.0
    elif unit in ["m3", "cubic meter"]:
        return value * 1000.0
    else:
        raise ValueError(f"Unsupported volume unit: '{unit}'")
