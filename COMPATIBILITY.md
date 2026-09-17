# Compatibility

This theme targets **Omarchy 4 (Quattro)** and its Quickshell interface.
Omarchy 3 and older use a different shell stack and are not supported.

| Omarchy version | Status | Notes |
|---|---|---|
| 4.0.3-1 | Tested | Reference version for `shell.toml`; interface screenshots in the README were captured here. |
| 4.0.4-1 | Tested | `tests/validate-config.py`'s schema matches the installed `Commons/{Color,Style,Border}.qml` source. This theme now also sets the `[polkit]`, `[lock]`, and `[image-picker]` surface tokens Omarchy added since 4.0.3, giving those surfaces the carbon/cyan treatment too. |
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
