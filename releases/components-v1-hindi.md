# Hindi addition to components-v1

This additive pack supplies Tilefinch's optional Devanagari glyphs for Hindi.
It uses the existing signed TFGF/TFGM format and bounded runtime provider.
Previously published assets are unchanged.

## Qualification record

- Release and signed-manifest tag: `components-v1`
- Component sequence: 1
- Manifest expiry: 2027-08-13 00:00:00 UTC
- Producer: Python 3.9.6, fontTools 4.60.1, Pillow 11.3.0,
  uharfbuzz 0.51.7 and freetype-py 2.5.1
- Shaping-dependency lock SHA-256:
  `9b3eb8b9578a4cb84a38f34d7745ac00b1291d130b63934cf3b6a7aeeb1b1859`
- The payload was rebuilt with byte-identical output.
- The exact signed envelope and payload passed the native Tilefinch consumer
  with its embedded production public root. The optimized host suite and
  both normal PSP executables built successfully.
- A physical PSP-3000 loaded the installed pack and Hindi interface catalog
  from an isolated USB-only tree. Scripted Settings and Appearance navigation
  completed, captures showed the translated rows, and shutdown was clean.
- Installer refusal, removal and rollback behavior are covered by the native
  component-store tests. A network download/install/removal journey on hardware
  is not claimed by this check.

## Glyph provenance and limits

The source is Noto Sans Devanagari Regular 2.002 under the SIL Open Font
License 1.1. The payload contains the complete OFL and original font digest.
HarfBuzz shapes the clusters offline; FreeType rasterizes bounded 16×16
monochrome cells. This covers common Hindi syllables and the current interface
clusters, not arbitrary runtime OpenType shaping of every Devanagari sequence.

| Input | SHA-256 |
|---|---|
| `NotoSansDevanagari-Regular.ttf` | `385e78e6359a9d88a0f243d53b1209d7548361ba2194e2b9ec779bcaa7e8949d` |
| Font OFL | `0dab92d0544f7b233403f14b84a663bdbfa746982eda629e7f4f9ffe1b036feb` |

## Published artifacts

| Asset | Entries | Bytes | SHA-256 |
|---|---:|---:|---|
| `tilefinch-glyph-devanagari-v1.tfgf` | 161 scalar glyphs + 3,755 clusters | 289,014 | `ccd49d8f786a2ad5192c68481f3670478daee48dafcf6eec88410e9026dc3850` |
| `tilefinch-glyph-devanagari-v1.tfgm` | — | 242 | `be6db4f6a312c1905c76f9b9a86a919a7318723d7b01eedc01eabc9fdf441f0f` |

Source fonts, signing keys, unsigned manifests and device evidence are release
inputs and are not committed to this repository.
