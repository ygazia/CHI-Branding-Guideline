# Colour

## The core three

CHI is a red, black and white brand. These three colours come straight from the logo artwork and do not change between themes.

| Colour | Token | HEX | RGB | Print |
|---|---|---|---|---|
| CHI Red | `chi-red` | #D9212D | 217 / 33 / 45 | Match to the approved press proof. Nearest coated spot reference: Pantone 1795 C, to be confirmed against a swatch book. |
| CHI Black | `chi-black` | #100F0D | 16 / 15 / 13 | 100K for type; rich black for large solids. |
| White | `chi-white` | #FFFFFF | 255 / 255 / 255 | Paper white. Specify a bright white, uncoated or silk stock. |

## Proportion

Red is powerful because there is not much of it. As a guide for any layout, pack or screen:

| Share | Colour | Role |
|---|---|---|
| 55% | White and `surface-raised` | Ground. Lets hair and product stand out. |
| 25% | `chi-black` / `ink` | Type, tool bodies, the Salon Black theme. |
| 15% | `chi-red` / `brand` | Logo, one headline panel, one action. |
| 5% | `silk` or the heat scale | Story accents. One accent family per piece. |

Campaign panels and packaging may invert the first and third rows, making red the ground. When they do, everything else on the panel is white. See **ColorProportion** in Components.

## Supporting colours

| Colour | Token | HEX | Use |
|---|---|---|---|
| Ceramic | `surface-raised` | #F6F4F2 | Cards, product tiles, alternate page bands. |
| Ceramic deep | `surface-sunken` | #ECE9E6 | Image placeholders, input wells. |
| Silk | `silk` | #EADFCF | Treatment, oil and care stories. A panel colour, with `on-silk` text. |
| Red deep | `brand-strong` | #B01822 | Hover and pressed states of red fills. |
| Red wash | `brand-tint` | #FCEBEC | Promotional notes, selected rows. |

Neutral greys lean slightly warm so they sit comfortably beside red and beside skin and hair in photography.

## The heat scale

Temperature is the one place CHI uses a colour sequence. `heat-low`, `heat-mid` and `heat-high` run from amber to orange to CHI Red, and each step is darker than the one before, so the order still reads in greyscale.

- Use the heat colours only for temperature settings and heat-protection content.
- Every band carries a temperature label in both °F and °C. The colour never stands alone.
- Text on `heat-low` and `heat-mid` is `on-heat`; text on `heat-high` is `on-brand`.

See **HeatScale** in Components.

## Text and contrast

Every pairing below meets WCAG AA (4.5:1) in both themes.

| Text | On | Light | Salon Black |
|---|---|---|---|
| `ink` | `surface` | 19.2:1 | 19.2:1 |
| `ink-muted` | `surface` / `surface-raised` | 7.1 / 6.5 | 8.8 / 8.0 |
| `brand-text` | `surface` / `surface-raised` | 6.0 / 5.5 | 7.6 / 6.9 |
| `on-brand` | `brand` | 5.0:1 | 5.0:1 |
| `on-brand` | `brand-strong` | 7.0:1 | 7.0:1 |
| `on-silk` | `silk` | 14.6:1 | 14.6:1 |

- White on `chi-red` is 4.99:1. It passes for all text sizes, with little to spare, so never lighten the red or use a tint behind white text.
- `chi-red` on `chi-black` is 3.8:1. That is enough for the logo and for headlines at 24px and above, and not enough for body copy. Red text on dark grounds uses `brand-text`.
- Never put `chi-red` text on `silk`, or on the heat colours.

## The Salon Black theme

The dark theme is not an inversion. It is the brand's black: tool bodies, backstage, the professional range. `surface` becomes `chi-black`, `ink` becomes white, and `brand` stays exactly `chi-red`. Use it for tools, professional and education content, and evening or event campaigns.

## Status colours

`success`, `caution` and `error` exist for interfaces only. Because `error` shares the brand red, every error message carries an icon and says what went wrong in words. `success` is a blue-leaning green so it is never confused with the red by hue alone.
