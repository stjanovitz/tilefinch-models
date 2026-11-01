# Tilefinch optional components v8

This resource update supports version 13 interface catalogs, including YouTube
channel navigation and updated playback and recovery messages. All thirteen
interface catalogs are available at their new immutable paths; versions 1–12
and earlier component releases remain unchanged.

The revised Hindi and shared Bengali-Assamese packs preserve every previously
published glyph cell exactly and each add two shaped clusters. Every other
language and voice asset pair is carried forward byte-for-byte.

| Pack | Signed sequence | Scalars | Shaped clusters | Bytes | SHA-256 |
|---|---:|---:|---:|---:|---|
| Devanagari | 8 | 161 | 3801 | 292326 | `2244e4a095b272c7035df52fc7546c40d2ef7d5a8e3287ff4c20a753cf607bb4` |
| Bengali-Assamese | 4 | 98 | 3655 | 279752 | `6c39400025efb7cc6143f4cf9361e55d6c24c90b268c536c63e6215848aa4bbe` |

Both manifests use root version 1 and tag `components-v8`. Fixed payload and
metadata filenames identify the package format, not the signed revision.
The producer uses the same pinned source fonts and SIL OFL 1.1 notices as the
previous release. Repeated builds are byte-identical. Native consumer checks
verify signatures, payload hashes, installation, restart identity, rendering,
removal and clean teardown; translated menus are checked in isolated emulator
runs. These are bounded pre-shaped inventories, not general runtime Indic
shaping or independent native-speaker translation review.
