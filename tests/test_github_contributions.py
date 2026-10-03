import json
import subprocess
import tarfile
from copy import deepcopy
from io import BytesIO

import pytest

from contribution_check import check_package, load
from tools.check_snapshot import prepare, verify


def package(tmp_path):
    rights = {'human_contributor': 'Example Author', 'ai_roles': {'actions': ['drafting']},
              'content_license': {'status': 'authorized', 'identifier': 'CC-BY-4.0', 'scope': 'new text'}}
    (tmp_path / 'rights-and-attribution.json').write_text(json.dumps(rights))
    (tmp_path / 'RESULT.md').write_text('Scoped claim; no general conjecture solution.')
    (tmp_path / 'REVIEW.md').write_text('Retained scope objection.')
    records = [
        {'draft_ref': 'claim', 'reader_label': 'RESULT', 'kind': 'CLAIM', 'problem': 'example',
         'created_at': 1, 'relations': [], 'content': {'artifact': 'RESULT.md',
          'attribution': rights, 'license': 'CC-BY-4.0'}},
        {'draft_ref': 'objection', 'reader_label': 'REVIEW', 'kind': 'CHALLENGE', 'problem': 'example',
         'created_at': 2, 'relations': [{'type': 'challenges', 'target_draft_ref': 'claim'}],
         'content': {'artifact': 'REVIEW.md', 'attribution': rights, 'license': 'CC-BY-4.0'}}]
    data = {'status': 'UNSIGNED CONTENT DRAFTS; NOT CRL WIRE EVENTS',
            'crl_reference_commit': 'a' * 40, 'records': records}
    (tmp_path / 'records.draft.json').write_text(json.dumps(data))
    return data


def test_retries_preserve_one_challenge_and_conflicts_fail(tmp_path):
    data = package(tmp_path)
    data['records'].append(deepcopy(data['records'][1]))
    path = tmp_path / 'records.draft.json'
    path.write_text(json.dumps(data))
    result = check_package(tmp_path)
    assert result['unique_records'] == 2 and result['duplicate_replays'] == 1
    assert result['retained_challenges'] == 1
    data['records'][-1]['content']['objection'] = 'Changed meaning under same ref'
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError, match='Conflicting duplicate'):
        check_package(tmp_path)


@pytest.mark.parametrize('change, message', [
    (lambda d: d['records'][1]['relations'][0].update(target_draft_ref='missing'), 'Missing draft dependency'),
    (lambda d: d['records'][1].update(problem='other'), 'crosses problem'),
    (lambda d: d['records'][0].update(signature='fake'), 'masquerade'),
    (lambda d: d['records'][0].update(kind='QUESTION'), 'kind mismatch'),
    (lambda d: d.update(crl_reference_commit='main'), 'full commit'),
    (lambda d: d['records'][0]['content'].update(artifact='../secret.txt'), 'escapes'),
    (lambda d: d['records'][0]['content']['attribution'].update(human_contributor='Other'), 'differs'),
])
def test_rejects_incomplete_or_misleading_drafts(tmp_path, change, message):
    data = package(tmp_path)
    change(data)
    (tmp_path / 'records.draft.json').write_text(json.dumps(data))
    with pytest.raises(ValueError, match=message):
        check_package(tmp_path)


def test_pending_rights_and_duplicate_json_fail(tmp_path):
    package(tmp_path)
    path = tmp_path / 'rights-and-attribution.json'
    rights = load(path)
    rights['content_license']['status'] = 'pending'
    path.write_text(json.dumps(rights))
    with pytest.raises(ValueError, match='authorized license'):
        check_package(tmp_path)
    path.write_text('{"human_contributor":"A", "human_contributor":"B"}')
    with pytest.raises(ValueError, match='Duplicate JSON'):
        check_package(tmp_path)


def test_commit_snapshot_excludes_dirty_files_and_is_repeatable(tmp_path):
    repo = tmp_path / 'repo'
    repo.mkdir()
    def git(*args):
        return subprocess.check_output(['git', '-C', str(repo), *args], text=True).strip()
    git('init', '-q')
    (repo / 'note.md').write_text('reviewed version')
    git('add', 'note.md')
    git('-c', 'user.name=Example', '-c', 'user.email=example@example.invalid', 'commit', '-qm', 'Example')
    sha = git('rev-parse', 'HEAD')
    (repo / 'note.md').write_text('unreviewed changes')
    (repo / 'private.txt').write_text('excluded untracked local file')
    output = tmp_path / 'artifacts'
    first = prepare(repo, sha, output)
    assert first == prepare(repo, sha, output)
    assert set(first['files']) == {'note.md'}
    archive, manifest = output / (sha + '.tar'), output / (sha + '.manifest.json')
    assert verify(archive, manifest)['file_bytes_match']
    with tarfile.open(archive) as tar:
        assert tar.extractfile('note.md').read() == b'reviewed version'
    archive.write_bytes(archive.read_bytes() + b'tamper')
    with pytest.raises(ValueError, match='Archive SHA256 mismatch'):
        verify(archive, manifest)
    with pytest.raises(ValueError, match='full 40'):
        prepare(repo, 'HEAD', output)


def test_github_container_can_differ_but_file_bytes_cannot(tmp_path):
    archive = tmp_path / 'github.tar.gz'
    def write(payload):
        with tarfile.open(archive, 'w:gz') as tar:
            member = tarfile.TarInfo('owner-repo-123/note.md')
            member.size = len(payload)
            tar.addfile(member, BytesIO(payload))
    import hashlib
    manifest = tmp_path / 'manifest.json'
    manifest.write_text(json.dumps({'format': 'crl-git-snapshot-v1', 'commit': 'a' * 40,
         'archive_sha256': 'b' * 64, 'files': {'note.md': {'size': 4,
         'sha256': hashlib.sha256(b'note').hexdigest()}}}))
    write(b'note')
    assert verify(archive, manifest, github_archive=True)['container_bytes_match'] is False
    write(b'edit')
    with pytest.raises(ValueError, match='inventory/hash mismatch'):
        verify(archive, manifest, github_archive=True)


def test_replication_compares_output_and_retains_runtime_metadata(tmp_path):
    data = package(tmp_path)
    rights = data['records'][0]['content']['attribution']
    rights['code_license'] = {'status': 'authorized', 'identifier': 'Apache-2.0', 'scope': 'new verifier'}
    (tmp_path / 'rights-and-attribution.json').write_text(json.dumps(rights))
    data['records'].append({'draft_ref': 'replication', 'reader_label': 'REVIEW',
        'kind': 'REPLICATION', 'problem': 'example', 'created_at': 3,
        'relations': [{'type': 'reproduces', 'target_draft_ref': 'claim'}],
        'content': {'artifact': 'REVIEW.md', 'verifier': 'reproduce.py', 'output': 'result.json',
                    'license': 'Apache-2.0', 'attribution': rights}})
    (tmp_path / 'records.draft.json').write_text(json.dumps(data))
    (tmp_path / 'reproduce.py').write_text('print(\'{"answer": 4, "python": "runtime-version"}\')')
    output = tmp_path / 'result.json'
    output.write_text('{"answer": 4, "python": "source-version"}')
    result = check_package(tmp_path, reproduce=True)
    assert result['reproductions'][0]['runtime_python'] == 'runtime-version'
    output.write_text('{"answer": 5}')
    with pytest.raises(ValueError, match='Reproduction output mismatch'):
        check_package(tmp_path, reproduce=True)


@pytest.mark.parametrize('case, message', [('tamper', 'hash/size mismatch'),
    ('omitted', 'cover every'), ('license', 'license mismatch'), ('version', 'VERSION')])
def test_package_manifest_detects_real_revision_errors(tmp_path, case, message):
    import hashlib
    package(tmp_path)
    (tmp_path / 'VERSION').write_text('0.1.0-draft.1\n')
    entries = [{'path': p.name, 'bytes': p.stat().st_size,
                'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'license': 'CC-BY-4.0'}
               for p in sorted(tmp_path.iterdir())]
    manifest = {'version': '0.1.0-draft.1', 'crl_reference_commit': 'a' * 40, 'files': entries}
    path = tmp_path / 'package-manifest.json'
    path.write_text(json.dumps(manifest))
    assert check_package(tmp_path)['package_manifest_checked']
    if case == 'tamper':
        (tmp_path / 'RESULT.md').write_text('Changed claim')
    elif case == 'omitted':
        (tmp_path / 'additional.md').write_text('Unlisted file')
    elif case == 'license':
        manifest['files'][0]['license'] = 'Unapproved'
        path.write_text(json.dumps(manifest))
    else:
        (tmp_path / 'VERSION').write_text('0.2.0')
    with pytest.raises(ValueError, match=message):
        check_package(tmp_path)


def test_repository_release_metadata_has_no_invented_doi_or_ai_creator():
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    metadata = load(root / '.zenodo.json')
    # Official GitHub/legacy schema accepts a string license ID; vocabulary IDs
    # were checked read-only at zenodo.org/api/vocabularies/licenses/.
    assert metadata['upload_type'] == 'software' and metadata['access_right'] == 'open'
    assert metadata['license'] == 'apache-2.0'
    assert metadata['creators'] == [{'name': 'Li, Hongmin'}]
    assert not {'doi', 'prereserve_doi', 'version'} & metadata.keys()
    assert not (root / 'CITATION.cff').exists()
    assert 'CC BY 4.0' in metadata['description'] and 'LICENSE.md' in metadata['description']
    assert 'repository-level' in metadata['description']
