# Compatibility

This theme targets **Omarchy 4 (Quattro)** and its Quickshell interface.
Omarchy 3 and older use a different shell stack and are not supported.

| Omarchy version | Status | Notes |
|---|---|---|
| 4.0.3-1 | Tested | Reference version for `shell.toml`; interface screenshots in the README were captured here. |
| 4.0.4-1 | Verified compatible | `tests/validate-config.py`'s schema still matches the installed `Commons/{Color,Style,Border}.qml` source. Omarchy added optional `[polkit]`, `[lock]`, and `[image-picker]` surface tokens since 4.0.3 that this theme does not yet set — Omarchy's own defaults apply there, so nothing breaks, but those surfaces don't get the theme's carbon/cyan treatment. |
| 4.1.x | Not tested | No access to a 4.1 install to verify against. |
| 4.2.x and newer | Not tested | |

## What "compatible" means here

`tests/validate-config.py` is a package contract, not a copy of Omarchy's
schema: it accepts a known subset of shell surface tokens and rejects
typos or unknown keys. A version bump is only a problem for this theme if
Omarchy renames or repurposes a token this theme sets in `shell.toml`, or
if a new required section appears with no fallback. Additive changes
(new optional sections, new tokens with defaults) do not require an
update here.

If you hit a breakage on a version not listed above, please open an
issue with your `omarchy version` output.
