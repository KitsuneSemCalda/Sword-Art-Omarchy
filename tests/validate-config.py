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


# WCAG 2.x contrast (SC 1.4.3): relative luminance -> contrast ratio.
TEXT_CONTRAST_MIN = 4.5

# Token pairs from colors.toml that are used as text on a surface.
COLOR_TEXT_PAIRS = [
    ("foreground", "background"),
    ("foreground", "lighter_background"),
    ("light_foreground", "background"),
    ("muted", "background"),
    ("dark_foreground", "background"),
    ("accent", "background"),
    ("accent", "lighter_background"),
    ("red", "background"),
    ("green", "background"),
    ("yellow", "background"),
    ("orange", "background"),
    ("blue", "background"),
    ("magenta", "background"),
]

# (text section.key, background section.key) pairs from shell.toml. Panel
# background-alpha composites over the desktop/wallpaper, which this
# validator can't see, so these check the nominal (opaque) surface color.
SHELL_TEXT_PAIRS = [
    (("bar", "text"), ("bar", "background")),
    (("controls", "normal-color"), ("bar", "background")),
    (("popups", "text"), ("popups", "background")),
    (("notifications", "text"), ("notifications", "background")),
    (("tooltip", "text"), ("tooltip", "background")),
    (("menu", "text"), ("menu", "background")),
]


def _channels(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def relative_luminance(hex_color):
    def linearize(channel):
        c = channel / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (linearize(c) for c in _channels(hex_color))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(hex_a, hex_b):
    la, lb = relative_luminance(hex_a), relative_luminance(hex_b)
    lighter, darker = max(la, lb), min(la, lb)
    return (lighter + 0.05) / (darker + 0.05)


def blend(hex_fg, alpha, hex_bg):
    """Alpha-composite hex_fg over an opaque hex_bg."""
    fg, bg = _channels(hex_fg), _channels(hex_bg)
    mixed = (round(f * alpha + b * (1 - alpha)) for f, b in zip(fg, bg))
    return "#%02x%02x%02x" % tuple(mixed)


def _check_contrast(label, fg_hex, bg_hex, minimum):
    ratio = contrast_ratio(fg_hex, bg_hex)
    if ratio < minimum:
        raise ValueError(
            f"{label}: {fg_hex} on {bg_hex} is {ratio:.2f}:1, "
            f"below the {minimum}:1 WCAG AA text minimum"
        )


def validate_contrast(colors, shell):
    for fg, bg in COLOR_TEXT_PAIRS:
        _check_contrast(f"colors.toml {fg}/{bg}", colors[fg], colors[bg], TEXT_CONTRAST_MIN)

    for (fg_section, fg_key), (bg_section, bg_key) in SHELL_TEXT_PAIRS:
        label = f"shell.toml {fg_section}.{fg_key}/{bg_section}.{bg_key}"
        _check_contrast(
            label, shell[fg_section][fg_key], shell[bg_section][bg_key], TEXT_CONTRAST_MIN
        )

    # The menu's selected state is a translucent highlight over the menu's
    # own background, so its effective color can be computed exactly.
    menu = shell["menu"]
    effective_selected_bg = blend(
        menu["selected-background"], menu["selected-background-alpha"], menu["background"]
    )
    _check_contrast(
        "shell.toml menu.selected-text/menu.selected-background",
        menu["selected-text"],
        effective_selected_bg,
        TEXT_CONTRAST_MIN,
    )


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
        with (root / "colors.toml").open("rb") as stream:
            colors = tomllib.load(stream)
        with (root / "shell.toml").open("rb") as stream:
            shell = tomllib.load(stream)
        validate_shell(shell)
        validate_contrast(colors, shell)
    except (OSError, ValueError) as error:
        sys.exit(f"FAIL: {error}")


if __name__ == "__main__":
    main()
