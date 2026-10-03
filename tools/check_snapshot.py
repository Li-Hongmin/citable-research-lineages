"""Offline Git snapshot manifest. No keys, server, DOI, or publishing action."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import tarfile


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def inventory(archive, *, strip_root=False):
    files = {}
    roots = set()
    with tarfile.open(archive) as tar:
        for member in tar:
            if member.isdir():
                continue
            path = PurePosixPath(member.name)
            if not member.isfile() or path.is_absolute() or '..' in path.parts:
                raise ValueError('Snapshot must contain only safe regular files')
            if strip_root:
                if len(path.parts) < 2:
                    raise ValueError('Expected archive root directory')
                roots.add(path.parts[0])
                path = PurePosixPath(*path.parts[1:])
            name = str(path)
            if name in files:
                raise ValueError('Duplicate archive path')
            with tar.extractfile(member) as stream:
                files[name] = {'size': member.size,
                               'sha256': hashlib.file_digest(stream, 'sha256').hexdigest()}
    if not files or (strip_root and len(roots) != 1):
        raise ValueError('Expected one nonempty snapshot')
    return dict(sorted(files.items()))


def prepare(repo, commit, output):
    if re.fullmatch(r'[0-9a-f]{40}', commit) is None:
        raise ValueError('Use a full 40-character commit SHA, not a movable ref')
    actual = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', '--verify',
                                      commit + '^{commit}'], text=True).strip()
    if actual != commit:
        raise ValueError('Commit mismatch')
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    archive = output / (commit + '.tar')
    temporary = output / (commit + '.tmp.tar')
    try:
        subprocess.run(['git', '-C', str(repo), 'archive', '--format=tar',
                        '--output=' + str(temporary.resolve()), commit], check=True)
        files = inventory(temporary)
        payload = {'format': 'crl-git-snapshot-v1', 'commit': commit,
                   'archive_sha256': digest(temporary), 'files': files,
                   'scope': 'git-tracked-files-only; no PR discussion; no permanent archive'}
        manifest = output / (commit + '.manifest.json')
        text = json.dumps(payload, indent=2, sort_keys=True) + '\n'
        if archive.exists() and digest(archive) != payload['archive_sha256']:
            raise ValueError('Refusing to replace different existing archive')
        if manifest.exists() and manifest.read_text() != text:
            raise ValueError('Refusing to replace different existing manifest')
        temporary.replace(archive)
        manifest.write_text(text)
        return payload
    finally:
        temporary.unlink(missing_ok=True)


def verify(archive, manifest, *, github_archive=False):
    expected = json.loads(Path(manifest).read_text())
    if expected.get('format') != 'crl-git-snapshot-v1' or re.fullmatch(
            r'[0-9a-f]{40}', expected.get('commit', '')) is None:
        raise ValueError('Invalid snapshot manifest')
    # GitHub may compress/repackage a commit archive differently. File bytes must match.
    if not github_archive and digest(archive) != expected['archive_sha256']:
        raise ValueError('Archive SHA256 mismatch')
    if inventory(archive, strip_root=github_archive) != expected['files']:
        raise ValueError('Snapshot file inventory/hash mismatch')
    return {'commit': expected['commit'], 'files': len(expected['files']),
            'archive_sha256': digest(archive), 'file_bytes_match': True,
            'container_bytes_match': digest(archive) == expected['archive_sha256'],
            'identity_or_scientific_verdict': 'not-checked'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    build = commands.add_parser('prepare')
    build.add_argument('--repo', type=Path, default=Path('.'))
    build.add_argument('--commit', required=True)
    build.add_argument('--output', type=Path, required=True)
    check = commands.add_parser('verify')
    check.add_argument('--archive', type=Path, required=True)
    check.add_argument('--manifest', type=Path, required=True)
    check.add_argument('--github-archive', action='store_true')
    args = parser.parse_args()
    try:
        result = (prepare(args.repo, args.commit, args.output) if args.command == 'prepare'
                  else verify(args.archive, args.manifest, github_archive=args.github_archive))
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError, tarfile.TarError) as error:
        parser.exit(1, str(error) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
