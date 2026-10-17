# Tilefinch optional components v6

This resource update supports version 11 interface catalogs, including native
file downloads, ZIP installation, and installed-app management. All thirteen
available interface languages receive the new controls. Earlier translation
paths and component releases remain unchanged.

The Hindi and shared Bengali-Assamese packs add six bounded shaped clusters
each. All 3,929 previous Hindi cells and 3,707 previous Bengali-Assamese cells
retain identical pixels. Every other language and voice asset pair is carried
forward byte-for-byte. Fixed asset names identify the package format, not the
signed revision.

## Revised packs

Both manifests use root version 1 and release tag `components-v6`.

| Pack | Signed sequence | Scalars | Shaped clusters |
|---|---:|---:|---:|
| Devanagari | 6 | 161 | 3,774 |
| Bengali-Assamese | 2 | 98 | 3,615 |

| Asset | Bytes | SHA-256 |
|---|---:|---|
| `tilefinch-glyph-devanagari-v1.tfgf` | 290382 | `7348f243d90e177c197b02d218e2b7e89b907663ebc4ee91d5241f3e102c82da` |
| `tilefinch-glyph-devanagari-v1.tfgm` | 242 | `43157dff2053db8f962023409ed4a35d8dd87a2047d553760a81bba749267dc0` |
| `tilefinch-glyph-bengali-assamese-v1.tfgf` | 276872 | `ec270f4d8f50f14ee3f45bb588f4013e13f128e0add788477da7e95f7699995c` |
| `tilefinch-glyph-bengali-assamese-v1.tfgm` | 254 | `c38d0582f1bd669a8a1ea33983842c04c915e9161910b430cf2e2fea142e5aa0` |

## Provenance and verification

Sources remain Noto Sans Devanagari Regular 2.002 and Noto Sans Bengali
Regular from noto-fonts commit `ffebf8c1ee449e544955a7e813c54f9b73848eac`,
under SIL OFL 1.1. Exact source-font SHA-256 values:

- Devanagari: `385e78e6359a9d88a0f243d53b1209d7548361ba2194e2b9ec779bcaa7e8949d`
- Bengali: `6300c5370cd688b0641343de4c786de6d412bb6c578d129dae75e93a0322dcab`

The exact v11 browser inventories and `requirements-shaping.txt` produce
byte-identical payloads on repeated builds. Native layout checks cover
12,488 frames and 142,976 complete labels without overlap or clipping.
The production consumer verifies the embedded-root signatures, exact payload
hashes, installation, restart identity, rendering, removal, and zero owned
bytes at teardown. Interrupted installation and removal remain covered by
the component fault-injection tests. Isolated emulator menu checks exercise
the current browser with each revised pack.

These are bounded pre-shaped inventories, not general runtime Indic shaping
or independent native-speaker translation review. Source fonts, private keys,
unsigned manifests, and private captures are not published.
