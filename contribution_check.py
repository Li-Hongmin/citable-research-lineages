"""Check the current manual GitHub contribution format, without signing drafts."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

from crl_events import KINDS, RELATIONS

LABELS = {'QUESTION': {'PROBLEM'}, 'RESULT': {'CLAIM', 'EVIDENCE', 'METHOD'},
          'REVIEW': {'REPLICATION', 'CHALLENGE', 'REVISION'}, 'WORK': {'WORK'}}


def load(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('Duplicate JSON property: ' + key)
            result[key] = value
        return result
    return json.loads(Path(path).read_text(), object_pairs_hook=unique)


def artifact(root, value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError('Expected relative artifact path')
    path = Path(value)
    resolved = (root / path).resolve()
    if path.is_absolute() or '..' in path.parts or not resolved.is_relative_to(root.resolve()):
        raise ValueError('Artifact path escapes contribution')
    if not resolved.is_file():
        raise ValueError('Missing artifact: ' + value)
    return resolved


def check_package(root, *, reproduce=False):
    root = Path(root)
    rights = load(root / 'rights-and-attribution.json')
    if not isinstance(rights.get('human_contributor'), str) or not rights['human_contributor'].strip():
        raise ValueError('Missing human attribution')
    if not (rights.get('ai_roles') or rights.get('new_package_ai_roles')):
        raise ValueError('Missing declared AI roles')
    license_keys = ['content_license'] + (['code_license'] if list(root.rglob('*.py')) else [])
    for key in license_keys:
        license_info = rights.get(key, {})
        if (license_info.get('status') != 'authorized' or not license_info.get('identifier')
                or not license_info.get('scope')):
            raise ValueError('Missing explicit authorized license metadata: ' + key)
    manifest_path = root / 'package-manifest.json'
    if manifest_path.exists():
        manifest = load(manifest_path)
        if re.fullmatch(r'[0-9a-f]{40}', manifest.get('crl_reference_commit', '')) is None:
            raise ValueError('Package reference must be a full commit SHA')
        if artifact(root, 'VERSION').read_text().strip() != manifest.get('version'):
            raise ValueError('Package version differs from VERSION')
        listed = set()
        for entry in manifest['files']:
            name = entry['path']
            if name in listed or name == 'package-manifest.json':
                raise ValueError('Duplicate or self-referencing manifest file')
            listed.add(name)
            path = artifact(root, name)
            with path.open('rb') as stream:
                sha = hashlib.file_digest(stream, 'sha256').hexdigest()
            if sha != entry['sha256'] or path.stat().st_size != entry['bytes']:
                raise ValueError('Package file hash/size mismatch: ' + name)
            license_key = 'code_license' if path.suffix == '.py' else 'content_license'
            if entry.get('license') != rights[license_key]['identifier']:
                raise ValueError('Package file license mismatch: ' + name)
        existing = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()
                    and '__pycache__' not in p.parts and p != manifest_path}
        if listed != existing:
            raise ValueError('Manifest must cover every package file except itself/runtime cache')
    records_path = root / 'records.draft.json'
    records, duplicates = {}, 0
    reproductions = []
    if not records_path.exists():
        artifact(root, 'QUESTION.md')
    if records_path.exists():
        data = load(records_path)
        if data.get('status') != 'UNSIGNED CONTENT DRAFTS; NOT CRL WIRE EVENTS':
            raise ValueError('Drafts must be explicitly marked unsigned')
        if re.fullmatch(r'[0-9a-f]{40}', data.get('crl_reference_commit', '')) is None:
            raise ValueError('CRL reference must be a full commit SHA')
        if not isinstance(data.get('records'), list) or not data['records']:
            raise ValueError('Expected nonempty draft records')
        for record in data['records']:
            ref = record.get('draft_ref')
            if not isinstance(ref, str) or not ref.strip():
                raise ValueError('Missing draft_ref')
            if ref in records:
                if records[ref] != record:
                    raise ValueError('Conflicting duplicate draft_ref: ' + ref)
                duplicates += 1
                continue
            if {'id', 'signature', 'body'} & record.keys():
                raise ValueError('Unsigned drafts must not masquerade as wire events')
            kind = record.get('kind')
            if kind not in KINDS or kind not in LABELS.get(record.get('reader_label'), set()):
                raise ValueError('Reader label/event kind mismatch')
            if not isinstance(record.get('problem'), str) or not record['problem'].strip():
                raise ValueError('Missing problem scope')
            if type(record.get('created_at')) is not int or record['created_at'] < 0:
                raise ValueError('Invalid draft timestamp')
            content = record.get('content', {})
            if content.get('attribution') != rights:
                raise ValueError('Record attribution differs from package rights metadata')
            if not content.get('license'):
                raise ValueError('Missing record license statement')
            for field in ('artifact', 'verifier', 'output'):
                if field in content:
                    artifact(root, content[field])
            if not content.get('artifact'):
                raise ValueError('Missing versioned record artifact')
            records[ref] = record
        for record in records.values():
            if not isinstance(record.get('relations'), list):
                raise ValueError('Expected relation list')
            for relation in record['relations']:
                if (set(relation) != {'type', 'target_draft_ref'} or relation['type'] not in RELATIONS):
                    raise ValueError('Invalid draft relation')
                target = records.get(relation['target_draft_ref'])
                if target is None:
                    raise ValueError('Missing draft dependency: ' + relation['target_draft_ref'])
                if target['problem'] != record['problem']:
                    raise ValueError('Draft dependency crosses problem scope')
    if reproduce:
        for record in records.values():
            content = record['content']
            if record['kind'] != 'REPLICATION' or 'verifier' not in content:
                continue
            verifier = artifact(root, content['verifier'])
            if verifier.suffix != '.py':
                raise ValueError('Pilot reproduction supports Python verifiers only')
            expected = load(artifact(root, content.get('output')))
            completed = subprocess.run([sys.executable, str(verifier)], cwd=root.resolve(),
                                       capture_output=True, text=True, timeout=30, check=True)
            actual = json.loads(completed.stdout)
            # Interpreter patch version is runtime metadata, not mathematical output.
            runtime = actual.pop('python', None)
            expected.pop('python', None)
            if actual != expected:
                raise ValueError('Reproduction output mismatch: ' + record['draft_ref'])
            reproductions.append({'draft_ref': record['draft_ref'], 'output_matches': True,
                                  'runtime_python': runtime})
    challenges = sum(r['kind'] == 'CHALLENGE' for r in records.values())
    return {'path': root.name, 'unique_records': len(records), 'duplicate_replays': duplicates,
            'package_manifest_checked': manifest_path.exists(), 'retained_challenges': challenges, 'reproductions': reproductions,
            'context_status': 'HAS_RETAINED_CHALLENGE' if challenges else 'NO_CHALLENGE_IN_PROVIDED_FILES',
            'scope': 'manual unsigned draft metadata only; no identity/rights/proof verification'}


def check(root, *, reproduce=False):
    root = Path(root)
    if not root.exists():
        return []  # No contributions in the initial protocol snapshot.
    packages = sorted(path for path in root.iterdir() if path.is_dir())
    return [check_package(path, reproduce=reproduce) for path in packages]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path('contributions'))
    parser.add_argument('--reproduce', action='store_true',
                        help='Run reviewed Python verifiers; not a sandbox for untrusted code')
    args = parser.parse_args()
    try:
        result = check(args.root, reproduce=args.reproduce)
    except (ValueError, KeyError, TypeError, AttributeError, OSError, subprocess.SubprocessError) as error:
        parser.exit(1, str(error) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
