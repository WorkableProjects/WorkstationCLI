"""Unit tests for interactive Periodic Table domain model, canonical lookup, and electron config visualization."""

import unittest
from chemistry.periodic_table import (
    find_element,
    find_grid_coordinates,
    get_shell_summary,
    format_subshell_display,
    format_element_detail,
    PERIODIC_TABLE_GRID,
)
from utils.parser import load_periodic_table


class TestPeriodicTable(unittest.TestCase):
    def test_canonical_lookup_by_symbol(self):
        res = find_element("H")
        self.assertIsNotNone(res)
        symbol, data = res
        self.assertEqual(symbol, "H")
        self.assertEqual(data["name"], "Hydrogen")

        # Case-insensitive
        res_lc = find_element("fe")
        self.assertIsNotNone(res_lc)
        self.assertEqual(res_lc[0], "Fe")

    def test_canonical_lookup_by_name(self):
        res = find_element("Gold")
        self.assertIsNotNone(res)
        self.assertEqual(res[0], "Au")
        self.assertEqual(res[1]["number"], 79)

    def test_canonical_lookup_by_atomic_number(self):
        res = find_element("118")
        self.assertIsNotNone(res)
        self.assertEqual(res[0], "Og")

        res_int = find_element("6")
        self.assertIsNotNone(res_int)
        self.assertEqual(res_int[0], "C")

    def test_lookup_not_found(self):
        self.assertIsNone(find_element("Unobtanium"))

    def test_grid_coordinates_mapping(self):
        pt_data = load_periodic_table()

        # Check H at (0, 0)
        pos_h = find_grid_coordinates("H", pt_data)
        self.assertEqual(pos_h, (0, 0))

        # Check He at (0, 17)
        pos_he = find_grid_coordinates("He", pt_data)
        self.assertEqual(pos_he, (0, 17))

        # Check Lanthanides row (row 8) e.g., La at (8, 3)
        pos_la = find_grid_coordinates("La", pt_data)
        self.assertEqual(pos_la, (8, 3))

        # Check Actinides row (row 9) e.g., Og at (6, 17) and U at (9, 6)
        pos_u = find_grid_coordinates("U", pt_data)
        self.assertEqual(pos_u, (9, 6))

    def test_electron_configuration_parsing_and_formatting(self):
        # Chromium ground-state exception: [Ar] 4s1 3d5
        cr_res = find_element("Cr")
        self.assertIsNotNone(cr_res)
        cr_data = cr_res[1]
        self.assertEqual(cr_data["electron_configuration"], "[Ar] 4s1 3d5")

        shells_cr = get_shell_summary(cr_data["electron_configuration"], cr_data["number"])
        self.assertEqual(shells_cr[1], 2)
        self.assertEqual(shells_cr[2], 8)
        self.assertEqual(shells_cr[3], 13)
        self.assertEqual(shells_cr[4], 1)

        # Copper exception: [Ar] 4s1 3d10
        cu_res = find_element("Cu")
        self.assertEqual(cu_res[1]["electron_configuration"], "[Ar] 4s1 3d10")

        # Subshell superscript formatting
        formatted = format_subshell_display("[Ar] 4s1 3d10")
        self.assertIn("4s¹", formatted)
        self.assertIn("3d¹⁰", formatted)

    def test_grid_selector_cursor_navigation(self):
        from core.ui import GridSelector
        pt_data = load_periodic_table()
        selector = GridSelector(
            title="Test Grid",
            grid_matrix=PERIODIC_TABLE_GRID,
            items_dict=pt_data,
            tile_renderer=lambda k, d, sel, comp: ""
        )
        # Initial selection is H at (0, 0)
        self.assertEqual(selector.get_selected_key(), "H")

        # Move right from (0, 0) -> skips empty slots (cols 1..16) and lands on He at (0, 17)
        selector.move_cursor(0, 1)
        self.assertEqual(selector.get_selected_key(), "He")

        # Move down from He (0, 17) -> lands on Ne at (1, 17)
        selector.move_cursor(1, 0)
        self.assertEqual(selector.get_selected_key(), "Ne")

        # Move left from Ne (1, 17) -> lands on F at (1, 16)
        selector.move_cursor(0, -1)
        self.assertEqual(selector.get_selected_key(), "F")

    def test_format_element_detail_contains_target_fields(self):
        res = find_element("Au")
        detail = format_element_detail("Au", res[1])
        self.assertIn("Gold", detail)
        self.assertIn("79", detail)
        self.assertIn("196.97 g/mol", detail)
        self.assertIn("Transition Metal", detail)
        self.assertIn("Period 6, Group 11", detail)
        self.assertIn("ELECTRON CONFIGURATION", detail)


if __name__ == "__main__":
    unittest.main()
