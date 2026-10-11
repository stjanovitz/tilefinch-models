# Tilefinch optional components v4

This release updates the Hindi glyph pack for version 7 interface catalogs,
including native video-player controls, chapters, seek status and rotation
guidance. Compatible browser builds pin `translations/ui/v7/`; all earlier
catalog paths and component releases remain unchanged.

Every other glyph and voice payload/envelope pair is carried forward
byte-for-byte. Fixed asset names identify the package format rather than
the signed component revision.

## Updated Hindi pack

- Signed component sequence: 4; version: `devanagari-4`
- Signed-manifest tag: `components-v4`
- Manifest expiry: 2027-10-11 16:00:00 UTC
- Glyph inventory: 161 scalars and 3,767 shaped clusters
- Two new interface clusters; every previous glyph retains identical pixels
- Source: Noto Sans Devanagari Regular 2.002, SIL Open Font License 1.1
- Source-font SHA-256:
  `385e78e6359a9d88a0f243d53b1209d7548361ba2194e2b9ec779bcaa7e8949d`
- Font-license SHA-256:
  `0dab92d0544f7b233403f14b84a663bdbfa746982eda629e7f4f9ffe1b036feb`
- Shaping dependency-lock SHA-256:
  `9b3eb8b9578a4cb84a38f34d7745ac00b1291d130b63934cf3b6a7aeeb1b1859`

| Asset | Bytes | SHA-256 |
|---|---:|---|
| `tilefinch-glyph-devanagari-v1.tfgf` | 289,878 | `8c4a470cf0618845e8b7f7a2a5e9699df317e2d45bae492f4f3e37f4f47affb4` |
| `tilefinch-glyph-devanagari-v1.tfgm` | 242 | `34ca5e5c0935c4f47f9ef40e9cadc09d0997f39b09ffeec47104ff3ffb55ddd2` |

## Qualification

- Two producer builds are byte-identical. All v7 Hindi interface clusters
  resolve, and previous scalar/cluster pixels are unchanged.
- All ten glyph payload/envelope pairs pass the browser's embedded production
  root verification, representative rendering and Budget teardown proof.
- Native painter checks cover 7,986 frames and 93,916 complete labels across
  supported interface languages, both player orientations and picker states,
  including actual Hindi and Arabic glyph packs.
- Integrated optimized host, visual-fidelity, sanitizer and named PSP build
  gates pass. Physical playback journeys cover chapters, seeking, crop,
  audio/subtitles and returning to the results page.
- The new catalog files match the browser's pinned SHA-256 values exactly.

These checks establish bounded rendering and integrity, not independent
human review of every translation or a new physical locale-menu test.
Source fonts, signing keys, unsigned manifests and captures are not committed.
