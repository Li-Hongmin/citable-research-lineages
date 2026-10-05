# SPDX-License-Identifier: Apache-2.0
"""Reassemble original compressed bytes. Does not verify mathematical proofs."""
from pathlib import Path
import argparse, hashlib, json
parser=argparse.ArgumentParser()
parser.add_argument('--manifest',required=True,type=Path)
parser.add_argument('--packages',required=True,type=Path)
parser.add_argument('--out',required=True,type=Path)
args=parser.parse_args()
manifest=json.loads(args.manifest.read_text())
def digest(raw):return hashlib.sha256(raw).hexdigest()
def safe(root,relative):
    rel=Path(relative)
    if rel.is_absolute() or '..' in rel.parts:raise ValueError('Unsafe relative path')
    path=root/rel
    if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):raise ValueError('Escaping path')
    return path
for source in manifest['sources']:
    parts=sorted(source['parts'],key=lambda row:row['offset_bytes'])
    payload=bytearray();offset=0
    for part in parts:
        if part['offset_bytes']!=offset:raise ValueError('Part offset mismatch')
        raw=safe(args.packages,part['package_relative_path']).read_bytes()
        if len(raw)!=part['bytes'] or digest(raw)!=part['sha256']:raise ValueError('Part mismatch')
        payload.extend(raw);offset+=len(raw)
    if offset!=source['bytes'] or digest(payload)!=source['sha256']:raise ValueError('Original mismatch')
    target=safe(args.out,source['relative_path'])
    target.parent.mkdir(parents=True,exist_ok=True)
    if target.exists():
        if not target.is_file() or digest(target.read_bytes())!=source['sha256']:raise ValueError('Refusing overwrite')
    else:
        with target.open('xb') as handle:handle.write(payload)
print('Compressed original byte reassembly complete; mathematical proof validity not assessed.')

