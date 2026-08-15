#!/usr/bin/env python3
"""Build a deterministic Tilefinch TFGF v1 optional glyph pack.

Font files are release inputs, never repository inputs.  The compiler keeps
only fixed-size raster cells plus the upstream license notice; it does not
embed or subset the source font.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from pathlib import Path
import struct
from typing import Iterable

MAGIC = b"TFGFv1\0\0"
ABI = 1
HEADER_BYTES = 80
PAGE_COUNT = 0x1100
MISSING_PAGE = 0xFFFF
ID_LIMIT = 24
SEQUENCE_LIMIT = 4096
SEQUENCE_CP_LIMIT = 8
GLYPH_LIMIT = 131072
NOTICE_LIMIT = 64 * 1024
FILE_LIMIT = 32 * 1024 * 1024


@dataclass(frozen=True)
class RasterGlyph:
    codepoints: tuple[int, ...]
    payload: bytes


def parse_hex_scalar(text: str) -> int:
    value = int(text, 16)
    if value < 0 or value > 0x10FFFF or 0xD800 <= value <= 0xDFFF:
        raise ValueError(f"invalid Unicode scalar U+{value:04X}")
    return value


def read_codepoint_spec(path: Path) -> set[int]:
    result: set[int] = set()
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        token = line.split(";", 1)[0].strip()
        try:
            if "-" in token:
                first_text, last_text = token.split("-", 1)
                first = parse_hex_scalar(first_text.strip())
                last = parse_hex_scalar(last_text.strip())
                if last < first:
                    raise ValueError("descending range")
                result.update(range(first, last + 1))
            else:
                for item in token.split():
                    result.add(parse_hex_scalar(item))
        except ValueError as error:
            raise ValueError(f"{path}:{number}: {error}") from error
    return result


def read_sequence_spec(path: Path | None) -> list[tuple[int, ...]]:
    if path is None:
        return []
    result: set[tuple[int, ...]] = set()
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        # Accept both a compact local list and Unicode emoji-test.txt lines.
        # The latter repeats minimally/unqualified presentation variants;
        # retain only its canonical fully-qualified spelling.
        if ";" in line:
            token, status = (item.strip() for item in line.split(";", 1))
            if status != "fully-qualified":
                continue
        else:
            token = line
        try:
            sequence = tuple(parse_hex_scalar(item) for item in token.split())
        except ValueError as error:
            raise ValueError(f"{path}:{number}: {error}") from error
        if len(sequence) < 2 or len(sequence) > SEQUENCE_CP_LIMIT:
            continue
        result.add(sequence)
    if len(result) > SEQUENCE_LIMIT:
        raise ValueError(f"sequence catalog exceeds {SEQUENCE_LIMIT} entries")
    return sorted(result)


def font_codepoints(path: Path) -> set[int]:
    try:
        from fontTools.ttLib import TTFont
    except ImportError as error:
        raise SystemExit("install requirements-build.txt (fonttools missing)") from error
    font = TTFont(path, fontNumber=0, lazy=True)
    try:
        return set((font.getBestCmap() or {}).keys())
    finally:
        font.close()


class FontRasterizer:
    def __init__(self, path: Path, color: bool, side: int):
        try:
            from PIL import Image, ImageDraw, ImageFont
        except ImportError as error:
            raise SystemExit("install requirements-build.txt (Pillow missing)") from error
        self.Image = Image
        self.ImageDraw = ImageDraw
        self.ImageFont = ImageFont
        self.path = path
        self.color = color
        self.side = side
        # Color bitmap fonts commonly expose a 109 px strike.  Mono outlines
        # are rendered at 4x then reduced before one-bit quantization.
        self.render_side = 136 if color else side * 4
        requested = 109 if color else side * 4
        self.font = ImageFont.truetype(str(path), requested)

    def rgba(self, codepoints: tuple[int, ...]) -> bytes:
        text = "".join(chr(value) for value in codepoints)
        image = self.Image.new("RGBA", (self.render_side, self.render_side), (0, 0, 0, 0))
        draw = self.ImageDraw.Draw(image)
        try:
            bounds = draw.textbbox((0, 0), text, font=self.font,
                                   embedded_color=self.color)
        except TypeError:
            bounds = draw.textbbox((0, 0), text, font=self.font)
        width = max(1, bounds[2] - bounds[0])
        height = max(1, bounds[3] - bounds[1])
        x = (self.render_side - width) // 2 - bounds[0]
        y = (self.render_side - height) // 2 - bounds[1]
        draw.text((x, y), text, font=self.font, fill=(255, 255, 255, 255),
                  embedded_color=self.color)
        bounds = image.getbbox()
        if bounds is None:
            return bytes(self.side * self.side * 4)
        glyph = image.crop(bounds)
        available = max(1, self.side - 1)
        glyph.thumbnail((available, available), self.Image.Resampling.LANCZOS)
        cell = self.Image.new("RGBA", (self.side, self.side), (0, 0, 0, 0))
        cell.alpha_composite(glyph, ((self.side - glyph.width) // 2,
                                     (self.side - glyph.height) // 2))
        return cell.tobytes()


def mono_payload(rgba: bytes, side: int) -> bytes:
    if side != 16 or len(rgba) != side * side * 4:
        raise ValueError("mono TFGF cells must be 16x16 RGBA")
    output = bytearray(32)
    for y in range(side):
        for x in range(side):
            at = (y * side + x) * 4
            # Preserve faint antialiased strokes before the one-bit pack.
            luminance = (rgba[at] * 77 + rgba[at + 1] * 150
                         + rgba[at + 2] * 29) >> 8
            coverage = luminance * rgba[at + 3] // 255
            if coverage >= 64:
                output[y * 2 + x // 8] |= 0x80 >> (x & 7)
    return bytes(output)


def color_payload(rgba: bytes, side: int) -> bytes:
    if len(rgba) != side * side * 4:
        raise ValueError("invalid RGBA cell")
    colors = bytearray()
    alpha = bytearray()
    for at in range(0, len(rgba), 4):
        red, green, blue, opacity = rgba[at:at + 4]
        rgb565 = (red >> 3) << 11 | (green >> 2) << 5 | (blue >> 3)
        colors += struct.pack(">H", rgb565)
        alpha.append(opacity)
    return bytes(colors + alpha)


def build_pack(component_id: str, kind: int, width: int, height: int,
               singles: list[RasterGlyph], sequences: list[RasterGlyph],
               notice: bytes) -> bytes:
    encoded_id = component_id.encode("ascii")
    if (not encoded_id or len(encoded_id) > ID_LIMIT
            or any(not (chr(value).islower() or chr(value).isdigit()
                       or chr(value) == "-") for value in encoded_id)):
        raise ValueError("component ID must be 1-24 lowercase ASCII characters")
    if kind not in (1, 2) or width < 1 or height < 1 or width > 24 or height > 24:
        raise ValueError("invalid glyph geometry")
    if kind == 1 and (width != 16 or height != 16):
        raise ValueError("mono packs must use 16x16 cells")
    if len(notice) > NOTICE_LIMIT:
        raise ValueError("license notice exceeds 64 KiB")
    singles = sorted(singles, key=lambda glyph: glyph.codepoints)
    sequences = sorted(sequences, key=lambda glyph: glyph.codepoints)
    if any(len(item.codepoints) != 1 for item in singles):
        raise ValueError("single glyph table contains a sequence")
    if any(len(item.codepoints) < 2 or len(item.codepoints) > 8
           for item in sequences):
        raise ValueError("invalid sequence length")
    all_codepoints = [item.codepoints[0] for item in singles]
    if len(all_codepoints) != len(set(all_codepoints)):
        raise ValueError("duplicate codepoint")
    if len(sequences) != len({item.codepoints for item in sequences}):
        raise ValueError("duplicate sequence")
    stride = 32 if kind == 1 else width * height * 3
    if any(len(item.payload) != stride for item in singles + sequences):
        raise ValueError("glyph payload has the wrong stride")
    glyph_count = len(singles) + len(sequences)
    if not singles or glyph_count > GLYPH_LIMIT or len(sequences) > SEQUENCE_LIMIT:
        raise ValueError("glyph or sequence count is outside the format bounds")

    directory = [MISSING_PAGE] * PAGE_COUNT
    pages = bytearray()
    first_glyph = 0
    grouped: dict[int, list[int]] = {}
    for codepoint in all_codepoints:
        grouped.setdefault(codepoint >> 8, []).append(codepoint & 0xFF)
    for record, page in enumerate(sorted(grouped)):
        directory[page] = record
        present = bytearray(32)
        for within in grouped[page]:
            present[within >> 3] |= 1 << (within & 7)
        pages += struct.pack(">I", first_glyph) + present
        first_glyph += len(grouped[page])

    sequence_table = bytearray()
    for index, glyph in enumerate(sequences, len(singles)):
        values = glyph.codepoints + (0,) * (8 - len(glyph.codepoints))
        sequence_table += bytes([len(glyph.codepoints), 0, 0, 0])
        sequence_table += struct.pack(">I8I", index, *values)

    directory_bytes = b"".join(struct.pack(">H", item) for item in directory)
    pages_offset = HEADER_BYTES + len(directory_bytes)
    sequences_offset = pages_offset + len(pages)
    payload_offset = sequences_offset + len(sequence_table)
    payload = b"".join(item.payload for item in singles + sequences)
    file_size = payload_offset + len(payload) + len(notice)
    if file_size > FILE_LIMIT:
        raise ValueError("TFGF exceeds the 32 MiB component ceiling")
    block_glyphs = min(64, max(1, (4 * 24 * 24 * 3) // stride))
    header = bytearray(HEADER_BYTES)
    header[0:8] = MAGIC
    header[8:10] = struct.pack(">H", ABI)
    header[10:15] = bytes([kind, width, height, block_glyphs, len(encoded_id)])
    header[16:24] = struct.pack(">IHH", glyph_count, len(grouped), len(sequences))
    header[24:44] = struct.pack(">IIIII", HEADER_BYTES, pages_offset,
                                sequences_offset, payload_offset, file_size)
    header[44:44 + len(encoded_id)] = encoded_id
    header[44 + len(encoded_id)] = 0
    header[72:76] = struct.pack(">I", len(notice))
    return bytes(header) + directory_bytes + pages + sequence_table + payload + notice


def render_glyphs(rasterizer: FontRasterizer, values: Iterable[tuple[int, ...]],
                  color: bool) -> list[RasterGlyph]:
    result = []
    for codepoints in values:
        rgba = rasterizer.rgba(codepoints)
        payload = (color_payload(rgba, rasterizer.side) if color
                   else mono_payload(rgba, rasterizer.side))
        result.append(RasterGlyph(codepoints, payload))
    return result


def command_build(args: argparse.Namespace) -> None:
    font_path = Path(args.font)
    requested = read_codepoint_spec(Path(args.codepoints))
    supported = font_codepoints(font_path)
    codepoints = sorted(requested & supported)
    if not codepoints:
        raise ValueError("font and codepoint specification have no overlap")
    sequences = read_sequence_spec(Path(args.sequences) if args.sequences else None)
    # Every sequence scalar must be present in the font cmap except joiners,
    # variation selectors and keycap combining marks.
    structural = {0x200D, 0x20E3, 0xFE0E, 0xFE0F}
    sequences = [item for item in sequences
                 if all(value in supported or value in structural for value in item)]
    side = 20 if args.color else 16
    rasterizer = FontRasterizer(font_path, args.color, side)
    singles = render_glyphs(rasterizer, ((value,) for value in codepoints), args.color)
    sequence_glyphs = render_glyphs(rasterizer, sequences, args.color)
    license_bytes = Path(args.license).read_bytes()
    provenance = (
        "Tilefinch optional glyph pack\n"
        f"component={args.component_id}\n"
        f"source-font-sha256={hashlib.sha256(font_path.read_bytes()).hexdigest()}\n"
        "The following upstream license applies to the rasterized font data.\n\n"
    ).encode("utf-8")
    pack = build_pack(args.component_id, 2 if args.color else 1, side, side,
                      singles, sequence_glyphs, provenance + license_bytes)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(pack)
    print(f"{len(pack)} {hashlib.sha256(pack).hexdigest()} "
          f"glyphs={len(singles)} sequences={len(sequence_glyphs)}")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--component-id", required=True)
    result.add_argument("--font", required=True)
    result.add_argument("--license", required=True)
    result.add_argument("--codepoints", required=True)
    result.add_argument("--sequences")
    result.add_argument("--color", action="store_true")
    result.add_argument("--output", required=True)
    return result


if __name__ == "__main__":
    command_build(parser().parse_args())
