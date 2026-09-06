# Sword Art Omarchy

An [Omarchy](https://omarchy.org/) theme inspired by Season 1 of Sword Art
Online — the black leather-and-steel look of Aincrad's system windows:
carbon-black backgrounds textured like a woven coat, with the bright
cyan-blue "Link Start" glow burning through the dark.

## Install

```bash
omarchy theme install https://github.com/KitsuneSemCalda/Sword-Art-Omarchy
omarchy theme set "Sword Art Omarchy"
```

## Palette

| | |
|---|---|
| Background | `#08090a` |
| Panel | `#16181b` |
| Accent (cyan) | `#3ee8ff` |
| Foreground | `#e9f2f5` |
| HP (red) | `#ff3b5c` |
| MP (blue) | `#4f8dff` |

Icons: `Yaru-blue-dark`.

## Backgrounds

Three 4K wallpapers — carbon-fiber texture only, no HUD elements, no
text. Just the material and a hint of ambient light, so icons and
windows stay legible on top.

<table>
<tr>
<td width="33%">

![ember](backgrounds/1-ember.png)
**`1-ember.png`**
A quiet cyan glow low in the corner.

</td>
<td width="33%">

![horizon](backgrounds/2-horizon.png)
**`2-horizon.png`**
The same glow, opposite corner.

</td>
<td width="33%">

![void](backgrounds/3-void.png)
**`3-void.png`**
No glow at all — pure carbon.

</td>
</tr>
</table>

`backgrounds/omarchy.png` is the wordmark wallpaper included in the theme's
background rotation, and `unlock.png` is the small logo mark shown on the
Plymouth unlock screen — both share the same carbon/cyan treatment.

`preview.png` and `preview-unlock.png` are compact selector previews derived
from the same artwork. They keep the theme visible in both the main Omarchy
theme picker and the Plymouth unlock-screen picker without loading the full
4K wallpapers.

![omarchy wordmark](backgrounds/omarchy.png)

All backgrounds and UI marks are original, generated artwork — no frames or
art from the anime were used.

## Development

Run the package checks locally with ImageMagick installed:

```bash
bash tests/validate-theme.sh
```

GitHub Actions runs the same validation on every push and pull request.
