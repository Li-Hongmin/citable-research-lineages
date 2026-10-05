# Byte-only certificate reassembly

Download all five sibling package directories at the same fixed public commit. Run reassemble.py with --manifest REASSEMBLY-MANIFEST.json, --packages the parent containing those five slug directories, and --out a new mutable directory. It concatenates exact raw parts by offset and verifies each part and whole-original SHA before exclusive creation; it does not decompress or verify proof logic. Do not execute original generators to manufacture missing historical files.
