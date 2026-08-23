# Arabic and Hebrew additions to components-v1

This additive component set supplies Tilefinch's optional Arabic and Hebrew
page-text packs. Both remain within the existing signed TFGF/TFGM format,
component sequence, expiry, and runtime pack limits.

## Qualification record

- Release and signed-manifest tag: `components-v1`
- Component sequence: 1
- Manifest expiry: 2027-08-13 00:00:00 UTC
- Producer dependencies: fontTools 4.60.2 and Pillow 12.3.0
- Dependency-lock SHA-256:
  `10d6ed145977df8e2f3b27bb9813b0e46d35b4a477b5781220ed0cb2fdefe868`
- Raster weight: 400, explicitly selected on both variable fonts
- Both payloads were rebuilt twice with byte-identical output.
- Every final envelope and exact payload passed the Tilefinch consumer with
  the embedded production public root.
- The release proof required authored pixels for Arabic contextual form
  U+FEB3 and Hebrew letter U+05E9 rather than accepting `.notdef` fallback.
- Isolated PPSSPP launcher smokes attached Arabic plus emoji (`0x90`) and
  Hebrew plus emoji (`0x110`) through the PSP-target component path.

## Glyph provenance

The packs use official Noto Sans Arabic 2.012 and Noto Sans Hebrew 3.001
variable fonts under the SIL Open Font License 1.1. Each TFGF includes the
complete applicable OFL, the original source-font digest, and the explicit
regular raster-weight record.

| Input | SHA-256 |
|---|---|
| `NotoSansArabic.ttf` | `63111b5b2e074dd48cc67692e0a2726d86ee94c1c37fe8598257b7b4e87e869e` |
| Arabic OFL | `07fc70bfeb985cc1a87a8587d0a0c80bab11c86c9dc3fd95b6f0cb332f983e96` |
| `NotoSansHebrew.ttf` | `7ef36a2c3593758cdb622e1bdef4f84523e92fbc3ccc667438dd80ff54c2de88` |
| Hebrew OFL | `9b9fe028b5ba74d231659a1bbaf0ed09b11e759d1ca6a070999e16d151616b47` |

## Published artifact checksums

| Asset | Glyphs | Bytes | SHA-256 |
|---|---:|---:|---|
| `tilefinch-glyph-arabic-v1.tfgf` | 1,213 | 52,458 | `1c6169d93c1c9e708a7a6f800fa2ccdb4562a02fd961f6b35da7aecd1e89a530` |
| `tilefinch-glyph-arabic-v1.tfgm` | — | 234 | `10096c077b3753d581e6f58248044311455a1ea9f875830e31c9f0d6e63f9669` |
| `tilefinch-glyph-hebrew-v1.tfgf` | 134 | 17,750 | `539f85c76ff9adb7030ae74174fd60c1b9c150efffb7d58af4d519665d3100b2` |
| `tilefinch-glyph-hebrew-v1.tfgm` | — | 234 | `c075c1c48ebf5c7a86c2c1ced3848663de323d1d3cd2529c4340e271bb8dfaba` |

Source fonts, private keys, proof trees, unsigned manifests, and Python
environments are release inputs and are not committed to this repository.
