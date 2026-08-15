# Tilefinch optional components v1

This first component release provides the downloads shown in Tilefinch's
Language & emoji and Experimental options:

- Japanese language pack — 0.96 MiB
- Simplified Chinese language pack — 0.96 MiB
- Traditional Chinese language pack — 0.96 MiB
- Korean language pack — 1.31 MiB
- Color emoji pack — 4.59 MiB
- Experimental offline English voice model — 8.69 MiB

Tilefinch verifies each download before installing it. Language and emoji
packs are optional; the browser's compact built-in fallback remains available
without them. Voice recognition runs locally on the PSP.

## Qualification record

- Release tag and signed-manifest tag: `components-v1`
- Component sequence: 1
- Manifest expiry: 2027-08-13 00:00:00 UTC
- Compatible browser release: Tilefinch `v0.1.0`
- Producer source release: `components-v1`
- Python dependency lock SHA-256:
  `10d6ed145977df8e2f3b27bb9813b0e46d35b4a477b5781220ed0cb2fdefe868`
- Every glyph payload was rebuilt twice with byte-identical output.
- The voice payload was rebuilt twice with byte-identical output.
- Every final envelope and exact payload passed the Tilefinch consumer using
  the embedded production public root.
- Japanese plus color emoji passed the isolated PPSSPP PSP-target raster gate:
  both provider requests observed, four bounded payload reads, 210 authored
  color pixels, and all existing raster invariants green.

## Glyph provenance

The language packs use Noto Sans CJK Regular at upstream commit
`f8d157532fbfaeda587e826d4cd5b21a49186f7c`. The color pack uses Noto Color
Emoji at upstream commit `8998f5dd683424a73e2314a8c1f1e359c19e8742`
and Unicode Emoji 16.0 sequence data. The source fonts identify the SIL Open
Font License 1.1 in their name tables, and each generated TFGF contains the
complete applicable license and its source-font digest.

Source input SHA-256 values:

| Input | SHA-256 |
|---|---|
| `NotoSansCJKjp-Regular.otf` | `68a3fc98800b2a27b371f2fb79991daf3633bd89309d4ffaa6946fd587f375b5` |
| `NotoSansCJKsc-Regular.otf` | `2c76254f6fc379fddfce0a7e84fb5385bb135d3e399294f6eeb6680d0365b74b` |
| `NotoSansCJKtc-Regular.otf` | `dce08bd4fd91aa8aa76ed8fea4b694c2dfb8550f67871e326843212ddbeb88b4` |
| `NotoSansCJKkr-Regular.otf` | `6bcb2a0703aa137e874fc2dffa85f6c21ba9a67fa329e81b8c801663af7e992a` |
| `NotoColorEmoji.ttf` | `72a635cb3d2f3524c51620cdde406b217204e8a6a06c6a096ff8ed4b5fd6e27b` |
| Unicode `emoji-test.txt` 16.0 | `24f0c534e86cf142e2496953e8f0e46a3e702392911eddcd29c6cced85139697` |

## Published artifact checksums

| Asset | Bytes | SHA-256 |
|---|---:|---|
| `tilefinch-glyph-ja-v1.tfgf` | 1,007,896 | `1b6ec1ad1ea311d90d54c4259ad41ec28664377c714cf21087369be6109851a1` |
| `tilefinch-glyph-ja-v1.tfgm` | 226 | `bb4d4efb43fc9787d35ef0dd85ba89733db3c7251f5649156a2ff92231b27de8` |
| `tilefinch-glyph-zh-hans-v1.tfgf` | 1,003,613 | `5f745094278ec15b1f9bfdbee15ca5088ffdb9d152bca9747e8458090897d7f9` |
| `tilefinch-glyph-zh-hans-v1.tfgm` | 236 | `d2aac55d09e889d72ea0bc52b05c59dfadee88d4cb24afc0c414a366444e623e` |
| `tilefinch-glyph-zh-hant-v1.tfgf` | 1,003,613 | `aad6b7ca86db9e13de02132bd45867a8b687d52a868acd2b1056fe86adda1837` |
| `tilefinch-glyph-zh-hant-v1.tfgm` | 236 | `66eda9e252c2c90e1ca12256daa40245066f7b090be0e53b0a23d1b65c5cb34c` |
| `tilefinch-glyph-ko-v1.tfgf` | 1,371,660 | `d28b0d893af653d9e5d77ab5b915b6a4bfa1286ab26c530d32992efc26417894` |
| `tilefinch-glyph-ko-v1.tfgm` | 226 | `c0f14927a7c4fb0bea08be1d8915e021ed5ea2e905d16c691feab2d9d74b65d9` |
| `tilefinch-glyph-emoji-color-v1.tfgf` | 4,809,825 | `b6727c035e4ece9051f92a1b3f8fb98e2f457e6049ad6f9c5dd4f46c6bfeed2e` |
| `tilefinch-glyph-emoji-color-v1.tfgm` | 244 | `5ee55fc3bc94394bfb189364a9bb6cdfc69ddac468d4a54d0df205a42d791a8b` |
| `tilefinch-voice-en-us-v1.tfvp` | 9,111,300 | `5331c669557cd56ec8ed826608cbd3dd5d0c19a416ce78278389753c7b40af20` |
| `tilefinch-voice-en-us-v1.tfvm` | 232 | `641c89dccfa03dfea28bbde1e88d64bea86d03cf490b6bc7cb1c039620a62115` |
