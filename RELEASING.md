# Releasing Tilefinch optional components

This document is for Tilefinch maintainers. User-facing information belongs
in [README.md](README.md).

The canonical security rationale and ceremony live in the main repository:

- [Release process](https://github.com/stjanovitz/tilefinch/blob/main/docs/RELEASE_PROCESS.md)
- [Secure-update design](https://github.com/stjanovitz/tilefinch/blob/main/docs/SECURE_UPDATES.md)

## Published artifacts

Release assets are credential-free and use fixed names. Do not commit the
binary payloads to this repository.

Voice:

- `tilefinch-voice-en-us-v1.tfvp` — deterministic model package
- `tilefinch-voice-en-us-v1.tfvm` — signed voice-component envelope

Glyph packs, each consisting of one directly addressable TFGF payload and one
signed TFGM envelope:

- `tilefinch-glyph-ja-v1.{tfgf,tfgm}`
- `tilefinch-glyph-zh-hans-v1.{tfgf,tfgm}`
- `tilefinch-glyph-zh-hant-v1.{tfgf,tfgm}`
- `tilefinch-glyph-ko-v1.{tfgf,tfgm}`
- `tilefinch-glyph-emoji-color-v1.{tfgf,tfgm}`

Browser, voice, and glyph metadata use separate package-format identifiers,
envelope magics, and signature domains. One artifact class cannot authorize
another.

## Build the voice component

From the exact Tilefinch source revision being released:

```sh
cmake --build build-preset-psp --target tilefinch-voice-component-package
```

The unsigned package is written to
`build-preset-psp/voice-component/tilefinch-voice-en-us-v1.tfvp`.

## Build glyph packs

Create a clean Python environment and install the pinned producer versions:

```sh
python3 -m pip install -r requirements-build.txt
```

Use the regional Noto Sans CJK Regular OTF for each language and
NotoColorEmoji.ttf for emoji. Never substitute one regional font for another:
the same Han codepoint can have deliberately different shapes. The following
is the Japanese form; the other three language commands differ only in the
component ID, font, manifest and output name:

```sh
python3 tools/build_glyph_pack.py \
  --component-id glyph-ja \
  --font inputs/NotoSansCJKjp-Regular.otf \
  --license inputs/OFL.txt \
  --codepoints manifests/japanese.txt \
  --output dist/tilefinch-glyph-ja-v1.tfgf
```

Build color emoji using the canonical fully-qualified sequences from the
Unicode Consortium's `emoji-test.txt` for the chosen Unicode version:

```sh
python3 tools/build_glyph_pack.py \
  --component-id glyph-emoji-color \
  --font inputs/NotoColorEmoji.ttf \
  --license inputs/OFL.txt \
  --codepoints manifests/emoji.txt \
  --sequences inputs/emoji-test.txt \
  --color \
  --output dist/tilefinch-glyph-emoji-color-v1.tfgf
```

The producer writes a size, SHA-256, glyph count, and sequence count. Capture
those values in the release work record. Rebuilding with identical inputs and
the pinned dependencies must produce the same SHA-256.

## Sign a glyph pack

Use `tools/tilefinch_update_tool.py` from the exact main-repository revision
being released. Signing happens on the offline machine:

```sh
python3 tools/tilefinch_update_tool.py manifest \
  --glyph-component \
  --package tilefinch-glyph-ja-v1.tfgf \
  --root-version ROOT_VERSION \
  --sequence COMPONENT_SEQUENCE \
  --expires UNIX_EXPIRY \
  --launcher-protocol 1 \
  --version ja-1 \
  --tag glyph-ja-v1 \
  --asset tilefinch-glyph-ja-v1.tfgf \
  --output glyph-ja.manifest

python3 tools/tilefinch_update_tool.py envelope \
  --glyph-component \
  --manifest glyph-ja.manifest \
  --release-key RELEASE_PRIVATE_KEY.pem \
  --output tilefinch-glyph-ja-v1.tfgm
```

Each pack has its own monotonic component sequence. A new payload must never
reuse an earlier sequence. The tool normalizes ECDSA signatures to low-S.

## License and provenance gate

Every TFGF carries:

- its exact source-font SHA-256;
- the complete applicable upstream font license;
- a component ID matching the fixed release asset.

Record the upstream font release/tag, font filename and digest, Unicode emoji
data version where applicable, Python version, and dependency-lock digest.
Do not add an umbrella repository license that could be mistaken for
relicensing packaged third-party data.

The staged voice TFVP must still contain:

- `LICENSES/ALPHA_CEPHEI_LICENSE.txt`
- `LICENSES/CMUDICT_LICENSE.txt`
- `LICENSES/CMUDICT_NOTICE.md`

## Publish and qualify

1. Run `python3 tests/test_build_glyph_pack.py` and the main repository's
   update, glyph-component, font, and PSP cross-build gates.
2. Verify every final payload and envelope with the exact embedded public
   root before uploading.
3. Upload the fixed-name asset pairs to one GitHub release.
4. Fetch them through unauthenticated HTTPS and compare size and SHA-256.
5. On a PSP, install, restart, render representative regional text/emoji,
   remove, restart, and confirm the embedded fallback remains available.
6. Interrupt one install and one removal to exercise candidate rollback and
   the durable uninstall marker.
7. Keep private keys and ceremony work products outside both repositories.

The immutable work record for the first release is
[`releases/components-v1.md`](releases/components-v1.md). Add one equivalent
record for every later release; do not rewrite an older record after its tag
is public.
