"""Reject malformed theme configuration before it reaches the shell."""

import copy
import importlib.util
from pathlib import Path
import tomllib
import unittest

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("validator", ROOT / "tests/validate-config.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class ContrastTests(unittest.TestCase):
    def setUp(self):
        self.colors = tomllib.loads((ROOT / "colors.toml").read_text())
        self.shell = tomllib.loads((ROOT / "shell.toml").read_text())

    def test_current_theme(self):
        validator.validate_contrast(self.colors, self.shell)

    def test_contrast_ratio_known_values(self):
        self.assertAlmostEqual(validator.contrast_ratio("#ffffff", "#000000"), 21, places=0)
        self.assertAlmostEqual(validator.contrast_ratio("#000000", "#000000"), 1, places=0)

    def test_blend_at_full_and_zero_alpha(self):
        self.assertEqual(validator.blend("#3ee8ff", 1.0, "#16181b"), "#3ee8ff")
        self.assertEqual(validator.blend("#3ee8ff", 0.0, "#16181b"), "#16181b")

    def test_low_contrast_color_token_fails(self):
        colors = copy.deepcopy(self.colors)
        colors["muted"] = colors["background"]
        with self.assertRaises(ValueError):
            validator.validate_contrast(colors, self.shell)

    def test_low_contrast_shell_pair_fails(self):
        shell = copy.deepcopy(self.shell)
        shell["tooltip"]["text"] = shell["tooltip"]["background"]
        with self.assertRaises(ValueError):
            validator.validate_contrast(self.colors, shell)

    def test_low_contrast_selected_highlight_fails(self):
        shell = copy.deepcopy(self.shell)
        shell["menu"]["selected-text"] = shell["menu"]["background"]
        with self.assertRaises(ValueError):
            validator.validate_contrast(self.colors, shell)


class ShellValidationTests(unittest.TestCase):
    def setUp(self):
        self.data = tomllib.loads((ROOT / "shell.toml").read_text())

    def test_current_theme(self):
        validator.validate_shell(self.data)

    def test_bad_values(self):
        for key, values in {
            "background": ["cyan", "#12345", 123],
            "background-alpha": [-0.1, 1.1, "0.5", True, float("nan"), float("inf")],
            "border-width": [-1, True, "1 -1", "1px", "1 2 3 4 5", ""],
        }.items():
            for value in values:
                with self.subTest(key=key, value=value):
                    data = copy.deepcopy(self.data)
                    data["menu"][key] = value
                    with self.assertRaises(ValueError):
                        validator.validate_shell(data)

    def test_missing_and_unknown_tokens(self):
        for section, key in (("menu", "text"), ("controls", "focus-color")):
            data = copy.deepcopy(self.data)
            del data[section][key]
            with self.assertRaises(ValueError):
                validator.validate_shell(data)
            data[section][key + "-typo"] = "#ffffff"
            with self.assertRaises(ValueError):
                validator.validate_shell(data)

    def test_unknown_and_missing_sections(self):
        self.data["launcher"] = self.data["menu"]
        with self.assertRaises(ValueError):
            validator.validate_shell(self.data)
        del self.data["launcher"]
        del self.data["menu"]
        with self.assertRaises(ValueError):
            validator.validate_shell(self.data)

    def test_valid_widths_and_alpha_boundaries(self):
        for width in (0, 1.5, "1", "1 2", "1 2 3", "1 1 1 3"):
            for alpha in (0, 1):
                self.data["menu"]["border-width"] = width
                self.data["menu"]["background-alpha"] = alpha
                validator.validate_shell(self.data)
