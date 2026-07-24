from typing import Optional

def validate_positive_float(value_str: str, name: str = "Value") -> float:
    try:
        val = float(value_str)
        if val <= 0:
            raise ValueError(f"{name} must be greater than zero.")
        return val
    except ValueError as e:
        if "could not convert" in str(e):
            raise ValueError(f"Invalid number entered for {name}: '{value_str}'")
        raise e

def validate_non_negative_float(value_str: str, name: str = "Value") -> float:
    try:
        val = float(value_str)
        if val < 0:
            raise ValueError(f"{name} cannot be negative.")
        return val
    except ValueError as e:
        if "could not convert" in str(e):
            raise ValueError(f"Invalid number entered for {name}: '{value_str}'")
        raise e

def validate_temperature_k(value_str: str) -> float:
    val = validate_positive_float(value_str, "Temperature")
    return val
