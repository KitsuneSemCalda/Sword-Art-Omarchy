#!/usr/bin/env bash

set -Eeuo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

fail() {
  printf 'FAIL: %s\n' "$*" >&2
  exit 1
}

pass() {
  printf 'PASS: %s\n' "$*"
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || fail "required command not found: $1"
}

require_file() {
  local path="$1"

  [[ -f "$path" && ! -L "$path" ]] || fail "required regular file missing: $path"
}

check_png() {
  local path="$1"
  local expected_geometry="$2"
  local alpha_mode="$3"
  local format geometry channels size

  format=$(identify -quiet -format '%m' -- "$path") || fail "cannot read image: $path"
  [[ "$format" == PNG ]] || fail "$path is not a PNG image"

  geometry=$(identify -quiet -format '%wx%h' -- "$path") || fail "cannot read dimensions: $path"
  [[ "$geometry" == "$expected_geometry" ]] || {
    fail "$path has geometry $geometry; expected $expected_geometry"
  }

  channels=$(identify -quiet -format '%[channels]' -- "$path") || fail "cannot read channels: $path"
  channels=${channels,,}
  if [[ "$alpha_mode" == required ]]; then
    [[ "$channels" == *a* ]] || fail "$path must contain an alpha channel"
  else
    [[ "$channels" != *a* ]] || fail "$path must not contain an alpha channel"
  fi

  size=$(stat -c '%s' -- "$path") || fail "cannot read file size: $path"
  if [[ "$path" == preview.png || "$path" == preview-unlock.png ]]; then
    (( size <= 2 * 1024 * 1024 )) || fail "$path is larger than 2 MiB"
  fi
}

require_command identify
require_command stat
require_command python3

required_files=(
  README.md
  LICENSE
  colors.toml
  shell.toml
  icons.theme
  unlock.png
  preview.png
  preview-unlock.png
  backgrounds/1-ember.png
  backgrounds/2-horizon.png
  backgrounds/3-void.png
  backgrounds/omarchy.png
)

for path in "${required_files[@]}"; do
  require_file "$path"
done
pass "required theme files are present"

declare -a required_colors=(
  mode
  accent selection muted
  background dark_background darker_background lighter_background
  foreground dark_foreground light_foreground bright_foreground
  red yellow orange green cyan blue magenta brown
  bright_red bright_yellow bright_green bright_cyan bright_blue bright_magenta
)

for key in "${required_colors[@]}"; do
  line_count=$(grep -Ec "^[[:space:]]*${key}[[:space:]]*=" colors.toml || true)
  (( line_count == 1 )) || fail "colors.toml must define $key exactly once"

  value=$(sed -n -E "s/^[[:space:]]*${key}[[:space:]]*=[[:space:]]*\"([^\"]*)\"[[:space:]]*$/\1/p" colors.toml)
  [[ -n "$value" ]] || fail "colors.toml has an invalid value for $key"

  if [[ "$key" == mode ]]; then
    [[ "$value" == dark ]] || fail "colors.toml mode must be dark"
  else
    [[ "$value" =~ ^#[[:xdigit:]]{6}$ ]] || fail "$key must be a #RRGGBB value"
  fi
done
pass "colors.toml contains the complete dark semantic palette"

python3 tests/validate-config.py
pass "TOML syntax and shell surface values are valid"

icon_theme=$(sed -n '/[^[:space:]]/p' icons.theme | head -n 1)
[[ "$icon_theme" =~ ^[[:alnum:]_.+-]+$ ]] || fail "icons.theme contains an invalid icon theme name"
pass "icons.theme contains a valid icon theme name"

shopt -s nullglob
backgrounds=(backgrounds/*.png)
(( ${#backgrounds[@]} >= 3 )) || fail "theme must contain at least 3 background PNGs"

for path in "${backgrounds[@]}"; do
  check_png "$path" 3840x2160 opaque
done
pass "all background PNGs are valid opaque 4K images"

check_png preview.png 1800x1012 opaque
check_png preview-unlock.png 1920x1080 opaque
check_png unlock.png 800x378 required
pass "selector previews and unlock logo have the expected formats"

printf 'All Sword Art Omarchy theme checks passed.\n'
