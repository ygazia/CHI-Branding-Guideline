# Typography

## One family, two voices

The logo pairs very heavy letters with a very light descriptor. Typography does the same with a single family, **Archivo**, a grotesque sans serif with nine weights and matching italics, free under the SIL Open Font License.

| Voice | Weight | Case | Used for |
|---|---|---|---|
| **Heavy** | 800 to 900 | Sentence case | Headlines, campaign lines, prices |
| **Light** | 300 to 500 | Capitals, wide tracking | Line names, eyebrows, claim badges |
| **Regular** | 400, with 600 for emphasis | Sentence case | Everything people read at length |

Archivo is the typeface for communication. It is never used to imitate or rebuild the logo.

## The scale

| Style | Size / line | Weight | Tracking | Use |
|---|---|---|---|---|
| `display-xl` | 72 / 68 | 900 | -0.02em | Campaign headlines, posters |
| `display-l` | 48 / 48 | 900 | -0.015em | Page heroes, social tiles |
| `headline` | 32 / 36 | 800 | -0.01em | Section headlines |
| `title` | 22 / 28 | 700 | 0 | Product names, card titles |
| `descriptor-l` | 28 / 32 | 300 | 0.06em | Line names beside headlines, capitals |
| `descriptor-s` | 13 / 16 | 500 | 0.14em | Eyebrows, badges, labels, capitals |
| `lead` | 20 / 30 | 400 | 0 | Opening paragraph |
| `body` | 16 / 26 | 400 | 0 | Running copy |
| `body-strong` | 16 / 26 | 600 | 0 | Emphasis, button labels |
| `caption` | 13 / 18 | 400 | 0 | Sizes, captions, help text |
| `legal` | 11 / 16 | 400 | 0 | Trademark and regulatory lines |

Sizes are in pixels for screens. For print, keep the proportions and set `body` at 9.5pt on 14pt for brochures and 7pt on 9pt for pack backs. Regulatory copy is never smaller than 6pt.

## Setting type

- **Left-aligned, ragged right.** Centre only short lines on pack fronts and posters. Never justify.
- **Line length** of 45 to 75 characters for `body`.
- **Headlines** sit tight: use the line heights in the scale and do not add space between lines.
- **One heavy headline per view.** A second level uses `headline` or `title`, not another `display-l`.
- **A descriptor sits above or beside a headline,** separated by `space-2`, as the line name sits under the mark in the logo.
- **Italics** are for product names in running text in languages where that is the convention, and for stylist quotes. Not for emphasis.
- **Numerals** align in tables: use tabular figures for prices, sizes and temperatures.
- **Colour:** `ink`, `ink-muted`, `on-brand`, or `brand-text`. Headlines may be `brand-text` on white once per view.

## Pairing example

> SALON PROFESSIONAL
>
> **Heat, handled.**
>
> Ceramic plates heat evenly from root to tip, so one pass is enough. Pair with thermal protection up to 450°F / 232°C.

The eyebrow is `descriptor-s`, the line is `display-l`, the paragraph is `lead`.

## Fallbacks and other scripts

- When Archivo cannot be installed (email, office documents), use Helvetica Neue, then Arial, with the same weights: bold for headlines, regular for copy.
- For Arabic, Cyrillic, Greek, Thai, Chinese, Japanese and Korean, use the matching Noto Sans family. Use its heaviest weight for headlines and regular for copy. Descriptors in scripts without capitals are set in medium weight at normal tracking.

## Do not

- set headlines in light or regular weight
- set long passages in capitals
- track heavy headlines wider than the scale
- add a second typeface for "luxury" or "natural" lines; express those through `silk`, photography and copy
- outline, stretch or add effects to type
