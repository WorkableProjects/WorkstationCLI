import unittest
from utils.parser import parse_chemical_formula, load_periodic_table
from calculators.stoichiometry import get_molar_mass

class TestParser(unittest.TestCase):
    def test_periodic_table_loads(self):
        pt = load_periodic_table()
        self.assertIn("H", pt)
        self.assertEqual(pt["H"]["mass"], 1.01)
        self.assertEqual(pt["O"]["mass"], 16.0)
        self.assertEqual(pt["Cu"]["mass"], 63.55)

    def test_simple_formulas(self):
        self.assertEqual(parse_chemical_formula("H2O"), {"H": 2, "O": 1})
        self.assertEqual(parse_chemical_formula("NaCl"), {"Na": 1, "Cl": 1})
        self.assertEqual(parse_chemical_formula("CO2"), {"C": 1, "O": 2})

    def test_parentheses_formulas(self):
        self.assertEqual(parse_chemical_formula("Ca(OH)2"), {"Ca": 1, "O": 2, "H": 2})
        self.assertEqual(parse_chemical_formula("Al2(SO4)3"), {"Al": 2, "S": 3, "O": 12})
        self.assertEqual(parse_chemical_formula("Fe(NO3)3"), {"Fe": 1, "N": 3, "O": 9})

    def test_hydrate_formulas(self):
        counts = parse_chemical_formula("CuSO4·5H2O")
        self.assertEqual(counts, {"Cu": 1, "S": 1, "O": 9, "H": 10})

    def test_molar_mass_calculations(self):
        self.assertAlmostEqual(get_molar_mass("H2O"), 18.02, places=2)
        self.assertAlmostEqual(get_molar_mass("NaCl"), 58.44, places=2)

if __name__ == "__main__":
    unittest.main()
