# Optional downloads for Tilefinch

This repository hosts optional, signed downloads for
[Tilefinch](https://github.com/stjanovitz/tilefinch), the homebrew web browser
for PSP.

You do not need anything here to use the browser. Tilefinch includes compact
CJK and emoji fallbacks out of the box, its normal keyboard is always
available, and it never downloads an optional component automatically.

## Language and emoji packs

Tilefinch includes Western and Central European text support, plus compact CJK
and monochrome emoji fallbacks, without any download. Optional signed packs
add more scripts or improve the shapes and presentation of characters the
browser already knows:

| Pack | What it adds |
|---|---|
| Japanese | Region-appropriate kana and Japanese Han forms |
| Simplified Chinese | Simplified Chinese Han forms and Bopomofo |
| Traditional Chinese | Traditional Chinese Han forms and Bopomofo |
| Korean | Hangul and region-appropriate Hanja |
| Cyrillic | Russian, Ukrainian, Belarusian, Bulgarian, Serbian, Macedonian and related languages |
| Extended Latin | Vietnamese and less-common Latin characters used by additional languages |
| Color emoji | Color presentation for supported emoji and sequences |

Cyrillic is one shared script pack; Russian and Ukrainian do not require
separate downloads. Color emoji is independent of the language packs. If a
pack is missing, damaged, or removed, Tilefinch continues with its bundled
fonts and fallbacks.

To install a pack exposed by your Tilefinch version:

1. Open **Settings → Appearance → Language & emoji**.
2. Choose a language, or turn on **Color emoji**.
3. Select the corresponding pack row and confirm the download.
4. Restart Tilefinch after installation.

The screen shows the exact download progress and installed state. Use Square
on an installed pack row to remove it. Packs are read in small blocks only
when a page needs one of their glyphs; they are not loaded wholesale into the
PSP's memory.

Language packs contain compact 16×16 monochrome glyph cells rather than full
desktop font files. The color emoji pack is larger because every 20×20 cell
stores both RGB color and transparency. Exact sizes are shown on the GitHub
release, and Tilefinch shows bounded progress while downloading.

## Offline English voice input

The optional voice model lets Tilefinch recognize a spoken search or short
text entry directly on the PSP. Microphone audio is not uploaded and no cloud
speech service or account is involved.

Voice input is experimental. It is English-only, slower and less accurate
than modern phone recognition, and limited to words in its search
dictionaries. The normal keyboard remains available.

To install it:

1. Open **Options → Experimental**.
2. Turn on **Voice input**.
3. Select **Voice model** and confirm the download.
4. Wait for verification and installation to finish.

The voice download is about **9.1 MB**. Installation temporarily needs about
**19 MB of free Memory Stick space** because the verified download and the
installation candidate coexist.

## Privacy, updates, and removal

Tilefinch verifies every optional component against its embedded update key
before activation. Browser A/B updates do not duplicate or replace these
downloads. The same Options screen can check for an update, cancel an
in-progress download, remove a component, or install it again later.

Removing a component returns its Memory Stick storage. A durable uninstall
marker prevents an interrupted removal from silently restoring an older
generation.

## Licensing and security

Language and emoji releases are generated from the corresponding Noto fonts
under the SIL Open Font License 1.1; each pack carries the complete upstream
license and source-font digest. The voice package carries the Alpha Cephei
acoustic-model license and complete CMUdict license and attribution notice.
Those upstream terms apply to the packaged data.

The small build and verification tools in this repository are covered by
[LICENSE-CODE.md](LICENSE-CODE.md). That license does not relicense the fonts,
voice model, dictionaries, or generated component payloads. Security issues in
the component format, signing, or installer should be reported through the
[Tilefinch security policy](SECURITY.md), not a public issue.

Maintainers and contributors can read [RELEASING.md](RELEASING.md) for the
release checklist and [PACK_FORMAT.md](PACK_FORMAT.md) for the bounded glyph
format. Source code, controls, and browser limitations live in the
[main Tilefinch repository](https://github.com/stjanovitz/tilefinch).
