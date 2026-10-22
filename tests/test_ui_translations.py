#!/usr/bin/env python3
"""Check bounded, inert published interface catalog data without a browser build."""
from pathlib import Path
import struct
import unittest


class TranslationTests(unittest.TestCase):
    def test_catalogs_are_bounded_and_ordered(self):
        root = Path(__file__).resolve().parents[1] / "translations" / "ui"
        catalogs = sorted(root.glob("v*/*.tful"))
        expected = {
            1: {"es", "fr", "de", "ja"},
            2: {"ru", "uk", "zh-hans", "ko"},
            3: {"hi", "ar"},
            4: {"es", "fr", "de", "ja", "ru", "uk", "zh-hans", "ko", "hi", "ar"},
            5: {"es", "fr", "de", "ja", "ru", "uk", "zh-hans", "ko", "hi", "ar"},
            6: {"es", "fr", "de", "ja", "ru", "uk", "zh-hans", "ko", "hi", "ar"},
            7: {"es", "fr", "de", "ja", "ru", "uk", "zh-hans", "ko", "hi", "ar"},
            8: {"pt"},
            9: {"bn", "as"},
            10: {"es", "fr", "de", "ja", "ru", "uk", "zh-hans", "ko", "hi", "ar", "pt", "bn", "as"},
            11: {"es", "fr", "de", "ja", "ru", "uk", "zh-hans", "ko", "hi", "ar", "pt", "bn", "as"},
            12: {"es", "fr", "de", "ja", "ru", "uk", "zh-hans", "ko", "hi", "ar", "pt", "bn", "as"},
        }
        self.assertEqual({str(path.relative_to(root)) for path in catalogs}, {
            f"v{version}/{language}.tful"
            for version, languages in expected.items() for language in languages
        })
        for path in catalogs:
            with self.subTest(path=path.relative_to(root)):
                data = path.read_bytes()
                if int(path.parent.name[1:]) >= 12:
                    self.assertLessEqual(len(data), 65535)
                    header, body = data.split(b"\n", 1)
                    self.assertEqual(header, b"TFUI2\t" + path.stem.encode("ascii"))
                    self.assertGreaterEqual(len(body), 2)
                    count, = struct.unpack_from(">H", body)
                    self.assertGreater(count, 0)
                    self.assertLessEqual(count, 2048)
                    self.assertGreaterEqual(len(body), 2 + 5 * count)
                    hashes = struct.unpack_from(f">{count}I", body, 2)
                    self.assertEqual(list(hashes), sorted(set(hashes)))
                    lengths = body[2 + 4 * count:2 + 5 * count]
                    self.assertTrue(all(lengths))
                    values = body[2 + 5 * count:].decode("utf-8")
                    self.assertTrue(values.endswith("\n"))
                    rows = values[:-1].split("\n")
                    self.assertEqual(len(rows), count)
                    self.assertTrue(all(row and "\0" not in row and "\t" not in row
                                        and len(row.encode("utf-8")) <= 256 for row in rows))
                    continue
                self.assertLessEqual(len(data), 32 * 1024)
                self.assertNotIn(b"\0", data)
                text = data.decode("utf-8")
                self.assertTrue(text.endswith("\n"))
                lines = text.splitlines()
                self.assertEqual(lines[0], "TFUI1\t" + path.stem)
                version = int(path.parent.name[1:])
                maximum_rows = 385 if version >= 11 else 336 if version >= 7 else 320
                self.assertLessEqual(len(lines) - 1, maximum_rows)
                keys = []
                for line in lines[1:]:
                    parts = line.split("\t")
                    self.assertEqual(len(parts), 2)
                    self.assertTrue(all(parts))
                    self.assertNotIn("%", line)
                    keys.append(parts[0].lower())
                self.assertEqual(keys, sorted(set(keys)))


if __name__ == "__main__":
    unittest.main()
