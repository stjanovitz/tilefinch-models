# Tilefinch optional components v2

This release updates the Hindi glyph pack for version 4 interface catalogs.
The catalogs translate menu-navigation instructions across all ten supported
interface languages and add Up/Down guidance. Compatible browser builds pin
the catalogs at `translations/ui/v4/`; older version paths remain unchanged.

All other glyph and voice payloads and envelopes are carried forward
byte-for-byte. The `components-v1` release remains unchanged. Fixed asset
names identify the package wire format, not the signed component revision.

## Updated Hindi pack

- Signed component sequence: 2; version: `devanagari-2`
- Signed-manifest tag: `components-v2`
- Manifest expiry: 2027-08-13 00:00:00 UTC
- Glyph inventory: 161 scalars and 3,758 shaped clusters
- Three new interface clusters; every previous cluster retains identical pixels
- Source: Noto Sans Devanagari Regular 2.002, SIL Open Font License 1.1
- Source-font SHA-256:
  `385e78e6359a9d88a0f243d53b1209d7548361ba2194e2b9ec779bcaa7e8949d`
- Font-license SHA-256:
  `0dab92d0544f7b233403f14b84a663bdbfa746982eda629e7f4f9ffe1b036feb`
- Shaping dependency-lock SHA-256:
  `9b3eb8b9578a4cb84a38f34d7745ac00b1291d130b63934cf3b6a7aeeb1b1859`

| Asset | Bytes | SHA-256 |
|---|---:|---|
| `tilefinch-glyph-devanagari-v1.tfgf` | 289,230 | `b6a660477a6c78ce008345e59433f4cdcd74d37734e08942fa1aa78a6e2402ec` |
| `tilefinch-glyph-devanagari-v1.tfgm` | 242 | `ff5066c1a60910b9ef57e9a6dfa3ddda2bd68e7e8b1e5d8b15b908bb4b885556` |

## Qualification

- Repeated producer builds are byte-identical.
- All ten glyph payload/envelope pairs pass the browser's embedded production
  root verification and installation proof.
- Integrated optimized host suite and both named PSP builds pass.
- Native menu geometry checks cover 7,282 frames and 91,738 complete labels
  across all ten languages and both themes, including actual Hindi and Arabic
  glyph packs.
- Hindi and Arabic Controls and Settings navigation were checked visually on
  a PSP; both scripted sessions completed and exited cleanly.

These checks establish integrity, bounded rendering and representative visual
coverage, not a claim of independent human review of every translation.
