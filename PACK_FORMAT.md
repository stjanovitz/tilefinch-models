# TFGF v1 glyph-pack format

TFGF is a bounded, memory-mappable-in-spirit raster format for the PSP. It is
not a general font format and contains no bytecode, OpenType tables, shaping
programs, or parser-controlled allocation sizes.

All integers are big-endian. A file contains:

1. an 80-byte fixed header;
2. a 4,352-entry Unicode-page directory (`uint16_t` records);
3. one 36-byte record per populated 256-codepoint page;
4. zero or more 40-byte, lexicographically sorted emoji sequence records;
5. fixed-stride glyph cells in index order;
6. a bounded UTF-8 provenance and license notice.

The page directory maps a Unicode scalar's high bits to a page record. Each
page record stores the first glyph index and a 256-bit presence map, so a
single-codepoint lookup is bounded and allocation-free. Sequence records hold
two to eight codepoints and a glyph index. Tilefinch narrows sequence matching
to the first-codepoint run and keeps the table capped at 4,096 entries.

Monochrome packs use 16×16 one-bit, MSB-first rows: 32 bytes per glyph. Color
packs use a fixed square cell whose payload is all RGB565 pixels followed by
one alpha byte per pixel. The current color emoji pack uses 20×20 cells, or
1,200 bytes per glyph.

The browser opens only the bounded index at attachment. A cache miss queues
one block; a later provider pump reads that fixed-size block from the Memory
Stick. Measurement, layout, rasterization, and ordinary frames never perform
file I/O directly. Four blocks are retained, and the request queue is capped
at 32 unique blocks.

Current hard bounds enforced by both producer and consumer:

- 32 MiB file size (signed component ceiling)
- 131,072 glyphs
- 4,352 Unicode pages
- 4,096 sequences, at most eight codepoints each
- 24×24 maximum source cell
- 64 KiB license/provenance notice
- three simultaneously attached packs

The signed TFGM manifest authorizes the exact TFGF size and SHA-256. Installed
metadata and the READY digest are reverified before a pack is attached.
