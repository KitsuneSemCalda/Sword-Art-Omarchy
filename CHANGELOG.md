# Changelog

Notable changes to this theme, newest first. This project doesn't tag
Git releases yet, so the version numbers below are informal milestones
for readability, not `git tag` references.

## Unreleased — 2026-09-15

- Raised `muted` and `dark_foreground` contrast to WCAG AA (4.5:1+)
  against the `#08090a` background.
- Added an automated WCAG AA contrast gate to `tests/validate-config.py`,
  covering every text/background token pair, including alpha-blended
  highlights.
- Losslessly recompressed every tracked PNG (~80MB → ~72MB repo size).
- Reworked the Plymouth `unlock.png` wordmark with Aincrad-style HUD
  corner brackets and register lines.
- Added `COMPATIBILITY.md` and a fan-project/unofficial disclaimer in
  the README.

## 0.4.0 — 2026-09-14

- Interface screenshots and compatibility notes in the README
  (`docs/screenshots/`).
- `shell.toml` validated against Omarchy's TOML schema and shell
  surface tokens in CI, with a matching unittest suite.
- Launcher now shares the `[menu]` surface instead of a separate one.

## 0.3.0 — 2026-09-06 to 2026-09-12

- Added `tests/validate-config.py` and a CI workflow to run it.
- Reduced dependence on the `bright_*` color tokens.

## 0.2.0 — 2026-08-30

- README rewritten to describe the Aincrad-inspired interface and
  install steps; removed an unused preview asset.

## 0.1.0 — 2026-08-30

- Initial Sword Art Online–themed assets, wallpapers, and README.
