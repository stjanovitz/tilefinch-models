"""Optional producer check using an explicit Noto Sans Devanagari input."""
import importlib.util
from pathlib import Path
import sys

spec = importlib.util.spec_from_file_location(
    "packer", Path(__file__).resolve().parents[1] / "tools/build_glyph_pack.py")
packer = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = packer
spec.loader.exec_module(packer)
font = Path(sys.argv[1])
rasterizer = packer.ShapedMonoRasterizer(font, 16)
for text in ("कि", "क्षि", "त्र", "ज्ञ", "श्र", "र्क", "हिन्दी"):
    cps = tuple(map(ord, text))
    first = rasterizer.rgba(cps)
    assert len(first) == 16 * 16 * 4 and any(first[3::4])
    assert first == rasterizer.rgba(cps)
    assert len(packer.mono_payload(first, 16)) == 32
# A reordered vowel+consonant must not be a bare consonant cell.
assert rasterizer.rgba(tuple(map(ord, "कि"))) != rasterizer.rgba((ord("क"),))
print("Hindi cluster shaping: deterministic nonempty bounded cells")
