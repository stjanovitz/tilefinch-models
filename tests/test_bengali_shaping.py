"""Explicit-input Bengali/Assamese producer qualification; no font downloads."""
import importlib.util
from pathlib import Path
import sys

spec = importlib.util.spec_from_file_location(
    "packer", Path(__file__).resolve().parents[1] / "tools/build_glyph_pack.py")
packer = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = packer
spec.loader.exec_module(packer)
font = Path(sys.argv[1])
corpus = ("কি", "কো", "ক্ষি", "জ্ঞ", "র্ক", "ৰ্কি", "ৱা", "ড়ো", "ক্‍ষি", "ক্‌ষি")
supported = packer.font_codepoints(font)
required = {0x0964, 0x0965, 0x09f0, 0x09f1}
assert required <= supported, "shared punctuation or Assamese letters missing from source font"
manifest = packer.read_codepoint_spec(Path(__file__).resolve().parents[1] / "manifests/bengali-assamese.txt")
assert required <= manifest, "pack manifest omits punctuation or Assamese letters"
for language in ("bn", "as"):
    rasterizer = packer.ShapedMonoRasterizer(font, 16, language)
    for text in corpus:
        first = rasterizer.rgba(tuple(map(ord, text)))
        assert first == rasterizer.rgba(tuple(map(ord, text)))
        assert len(first) == 1024 and any(first[3::4]), (language, text)
        assert len(packer.mono_payload(first, 16)) == 32
    assert rasterizer.rgba(tuple(map(ord, "কি"))) != rasterizer.rgba((ord("ক"),))
    assert rasterizer.rgba(tuple(map(ord, "ক্ষি"))) != rasterizer.rgba(tuple(map(ord, "ক্ষ")))
    try:
        rasterizer.rgba((0x10ffff,))
        raise AssertionError("a missing glyph was accepted as shaped ink")
    except ValueError:
        pass
print("Bengali/Assamese shaping: deterministic complete clusters and nonempty cells")
