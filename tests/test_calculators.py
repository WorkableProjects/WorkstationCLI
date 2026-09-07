"""Unit tests for chemistry calculators."""

from calculators.gas_laws import _solve_ideal_gas_law, R_ATM
from utils.parser import parse_chemical_formula, load_periodic_table

def test_parse_chemical_formula():
    counts = parse_chemical_formula("H2O")
    assert counts == {"H": 2, "O": 1}

    complex_counts = parse_chemical_formula("Ca(OH)2")
    assert complex_counts == {"Ca": 1, "O": 2, "H": 2}

def test_periodic_table_data():
    table = load_periodic_table()
    assert "H" in table
    assert table["H"]["name"] == "Hydrogen"
    assert table["H"]["mass"] > 1.0
