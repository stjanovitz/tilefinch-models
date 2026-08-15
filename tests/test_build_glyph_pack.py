#!/usr/bin/env python3

import importlib.util
from pathlib import Path
import struct
import sys
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "build_glyph_pack.py"
SPEC = importlib.util.spec_from_file_location("build_glyph_pack", MODULE_PATH)
PACKER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = PACKER
SPEC.loader.exec_module(PACKER)


class GlyphPackTests(unittest.TestCase):
    def test_mono_pack_is_deterministic_and_indexed(self):
        zero = bytes(32)
        full = bytes([0xFF]) * 32
        singles = [
            PACKER.RasterGlyph((0x4E01,), full),
            PACKER.RasterGlyph((0x3042,), zero),
            PACKER.RasterGlyph((0x4E00,), zero),
        ]
        sequence = PACKER.RasterGlyph((0x1F469, 0x200D, 0x1F4BB), full)
        first = PACKER.build_pack(
            "glyph-ja", 1, 16, 16, singles, [sequence], b"OFL notice")
        second = PACKER.build_pack(
            "glyph-ja", 1, 16, 16, singles, [sequence], b"OFL notice")
        self.assertEqual(first, second)
        self.assertEqual(first[:8], b"TFGFv1\0\0")
        self.assertEqual(struct.unpack(">H", first[8:10])[0], 1)
        self.assertEqual(first[10:15], bytes([1, 16, 16, 64, 8]))
        glyphs, pages, sequences = struct.unpack(">IHH", first[16:24])
        self.assertEqual((glyphs, pages, sequences), (4, 2, 1))
        directory_offset, pages_offset, sequences_offset, payload_offset, size = (
            struct.unpack(">IIIII", first[24:44]))
        self.assertEqual(directory_offset, 80)
        self.assertEqual(size, len(first))
        self.assertEqual(first[44:53], b"glyph-ja\0")
        self.assertEqual(struct.unpack(">I", first[72:76])[0], 10)
        page_30 = struct.unpack(">H", first[80 + 0x30 * 2:82 + 0x30 * 2])[0]
        page_4e = struct.unpack(">H", first[80 + 0x4E * 2:82 + 0x4E * 2])[0]
        self.assertEqual((page_30, page_4e), (0, 1))
        self.assertEqual(pages_offset, 80 + 0x1100 * 2)
        self.assertEqual(sequences_offset, pages_offset + 72)
        self.assertEqual(payload_offset, sequences_offset + 40)
        self.assertTrue(first.endswith(b"OFL notice"))

    def test_color_layout_is_rgb565_then_alpha(self):
        rgba = bytes([255, 0, 0, 128])
        payload = PACKER.color_payload(rgba, 1)
        self.assertEqual(payload, b"\xF8\x00\x80")

    def test_rejects_duplicate_codepoint(self):
        glyph = PACKER.RasterGlyph((0x4E00,), bytes(32))
        with self.assertRaises(ValueError):
            PACKER.build_pack(
                "glyph-ja", 1, 16, 16, [glyph, glyph], [], b"notice")


if __name__ == "__main__":
    unittest.main()
