# Tilefinch optional components v5

This resource update adds the shared Bengali-Assamese glyph pack and extends
the Hindi pack for version 10 interface catalogs. Those catalogs add playlist
playback, queue and automatic-next controls in all available interface languages.
This is not a browser binary release.

All earlier translation paths and component releases remain immutable. Every
other language and voice asset pair is carried forward byte-for-byte. Fixed
asset names identify the package format, not its signed component revision.

## Revised Hindi pack

- Signed sequence 5; version `devanagari-5`; manifest tag `components-v5`
- 161 scalars and 3,768 bounded shaped clusters
- All 3,928 previous scalar/cluster cells retain identical pixels
- Source: Noto Sans Devanagari Regular 2.002, SIL OFL 1.1
- Source-font SHA-256: `385e78e6359a9d88a0f243d53b1209d7548361ba2194e2b9ec779bcaa7e8949d`

| Asset | Bytes | SHA-256 |
|---|---:|---|
| `tilefinch-glyph-devanagari-v1.tfgf` | 289,950 | `90701293fb8ac1789b34cd2bb68c3516c25a570b4f23bb1dc0048b07746fe525` |
| `tilefinch-glyph-devanagari-v1.tfgm` | 242 | `7227082c61798636d448c67329677ef85ab8a5ed5ada04055e510509af8348bb` |

## Shared Bengali-Assamese pack

- Signed sequence 1; version `bengali-assamese-1`
- Manifest tag `glyph-bengali-assamese-v1`
- 98 scalars and 3,609 bounded shaped clusters
- Source: Noto Sans Bengali Regular, noto-fonts commit
  `ffebf8c1ee449e544955a7e813c54f9b73848eac`, SIL OFL 1.1
- Source-font SHA-256: `6300c5370cd688b0641343de4c786de6d412bb6c578d129dae75e93a0322dcab`

| Asset | Bytes | SHA-256 |
|---|---:|---|
| `tilefinch-glyph-bengali-assamese-v1.tfgf` | 276,440 | `1a43c836fd570c2186bb92406f609b24443bb551f55dda07ee71a3cfc0fdcd85` |
| `tilefinch-glyph-bengali-assamese-v1.tfgm` | 266 | `223141416e22e5ba11013a96abc8ca823ebc8b7a59008ef9cc47014f183f0f18` |

## Qualification

The source-font license digest is
`0dab92d0544f7b233403f14b84a663bdbfa746982eda629e7f4f9ffe1b036feb`;
the shaping dependency-lock digest is
`9b3eb8b9578a4cb84a38f34d7745ac00b1291d130b63934cf3b6a7aeeb1b1859`.
Both packs rebuild deterministically and pass the browser's embedded-root
signature, exact payload, installation, restart identity, removal and Budget
teardown checks.

The shared native painter checks cover 11,760 frames and 139,692 complete
labels, both player orientations, provider pages and menu states, including
actual Hindi, Arabic and Bengali-Assamese packs. No overlap or clipping was
detected. Integrated optimized host, fidelity and named PSP build gates pass.
These are host painter and cross-build checks, not a new physical-device
locale-menu qualification or independent native-speaker translation review.
Coverage is a bounded pre-shaped inventory, not general runtime Indic shaping.

Source fonts, signing keys, unsigned manifests and private captures are not
published. Compatible browser builds pin each exact catalog SHA-256.
