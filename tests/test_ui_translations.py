#!/usr/bin/env python3
"""Check bounded, inert published interface catalog data without a browser build."""
from pathlib import Path
import unittest


class TranslationTests(unittest.TestCase):
    def test_catalogs_are_bounded_and_ordered(self):
        root = Path(__file__).resolve().parents[1] / "translations" / "ui"
        catalogs = sorted(root.glob("v*/*.tful"))
        self.assertEqual(len(catalogs), 10)
        for path in catalogs:
            with self.subTest(path=path.relative_to(root)):
                data = path.read_bytes()
                self.assertLessEqual(len(data), 32 * 1024)
                self.assertNotIn(b"\0", data)
                text = data.decode("utf-8")
                self.assertTrue(text.endswith("\n"))
                lines = text.splitlines()
                self.assertEqual(lines[0], "TFUI1\t" + path.stem)
                self.assertLessEqual(len(lines) - 1, 256)
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
