#!/usr/bin/env python3
"""Validate this theme's supported subset of Omarchy 4 shell tokens.

Reference: Omarchy 4.0.3-1 Commons/{Color,Style,Border}.qml.
This is a package contract, not a complete Omarchy schema. Extend it when
intentionally adding supported tokens; unknown keys otherwise hide typos.
"""

from pathlib import Path
import math
import re
import sys

if sys.version_info < (3, 11):
    sys.exit("FAIL: configuration validation requires Python 3.11 or newer")
import tomllib

SURFACE = {
    "background", "background-alpha", "text", "border", "border-alpha",
    "border-width",
}
MENU = SURFACE | {
    "scrim", "scrim-alpha", "selected-background", "selected-background-alpha",
    "selected-text", "selected-border", "selected-border-alpha",
}
SCHEMA = {
    "bar": {"background", "background-alpha", "text", "active"},
    "controls": {
        f"{state}-{token}"
        for state in ("normal", "hover-cursor", "focus", "selected")
        for token in ("color", "fill-alpha", "border", "border-width", "border-alpha")
    },
    "popups": SURFACE,
    "notifications": SURFACE | {"countdown"},
    "tooltip": SURFACE,
    "menu": MENU,
}


def number(value):
    return type(value) in (int, float) and math.isfinite(value)


def validate_shell(data):
    if data.keys() != SCHEMA.keys():
        raise ValueError(
            f"shell.toml sections: missing {sorted(SCHEMA.keys() - data.keys())}; "
            f"unknown {sorted(data.keys() - SCHEMA.keys())}"
        )
    for section, keys in SCHEMA.items():
        values = data[section]
        if not isinstance(values, dict):
            raise ValueError(f"shell.toml [{section}] must be a table")
        if values.keys() != keys:
            raise ValueError(
                f"shell.toml [{section}]: missing {sorted(keys - values.keys())}; "
                f"unknown {sorted(values.keys() - keys)}"
            )
        for key, value in values.items():
            if key.endswith("-alpha"):
                valid = number(value) and 0 <= value <= 1
                expected = "a number between 0 and 1"
            elif key.endswith("-width"):
                valid = number(value) and value >= 0
                if isinstance(value, str):
                    parts = value.split()
                    valid = 1 <= len(parts) <= 4 and all(
                        re.fullmatch(r"\d+(?:\.\d+)?", part) for part in parts
                    )
                expected = "a nonnegative width or 1–4 space-separated widths"
            else:
                valid = isinstance(value, str) and re.fullmatch(r"#[0-9a-fA-F]{6}", value)
                expected = "a #RRGGBB color"
            if not valid:
                raise ValueError(f"shell.toml {section}.{key} must be {expected}")


def main():
    root = Path(__file__).resolve().parent.parent
    try:
        for name in ("colors.toml", "shell.toml"):
            with (root / name).open("rb") as stream:
                data = tomllib.load(stream)
            if name == "shell.toml":
                validate_shell(data)
    except (OSError, ValueError) as error:
        sys.exit(f"FAIL: {error}")


if __name__ == "__main__":
    main()
