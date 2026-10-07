#!/usr/bin/env python3
"""Install eight DSH-only wrappers backed by a complete, pinned local git tree.

No network, package installation, host configuration, or deletion. Python 3.9+.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import shlex
import subprocess
import sys
import tarfile
import uuid

from preflight import digest, verify_source

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
OWNER = 'academic-research-skills/dsh-v1'
FAMILIES = {
    'research': {
        'names': ('deep-research', 'akademicheskoe-issledovanie'),
        'modes': 'full quick review lit-review fact-check three-way-scan socratic systematic-review',
        'description': 'Research, literature review, source verification and fact-check; lightweight by default for simple questions.',
        'instructions': 'Select quick/fact-check for a bounded question; socratic for an unclear research question. For full/systematic-review, preserve search strategy, inclusion/exclusion log, evidence grading, source verification, uncertainty and methodology/bias review. Meta-analysis requires actual data and separately checked statistical dependencies. Do not write a publication pipeline unless asked.',
    },
    'paper': {
        'names': ('academic-paper', 'akademicheskaya-statya'),
        'modes': 'full plan outline revision revision-coach abstract lit-review format-convert citation-check disclosure rebuttal-audit',
        'description': 'Plan, draft, revise, cite and format academic papers with verified evidence and human checkpoints.',
        'instructions': 'Select only the requested writing mode. Establish audience, journal, language, evidence and citation style. Keep unsupported claims marked; user approval and disclosure remain required. For revision read academic-paper/references/revision_patch_protocol.md and the current roadmap/authorization contracts before modifying the draft. Produce and validate patch/evidence artifacts; never fabricate author approval or bypass a refused patch.',
    },
    'reviewer': {
        'names': ('academic-paper-reviewer', 'akademicheskii-retsenzent'),
        'modes': 'full re-review quick methodology-focus guided calibration',
        'description': 'Academic peer review, methodology checks and re-review; fresh bounded reviewers when independent perspectives are requested.',
        'instructions': 'Choose quick for a bounded assessment. For full review, use the source reviewer roles and scoring contracts with separate fresh NONfork review packets; preserve stage ordering and precommitment. Report severity, exact location, evidence, remedy and uncertainties. Re-review verifies changes against prior authorized findings without silently broadening scope. Calibration needs supplied gold data with evaluator/subject separation; never expose gold answers to a subject.',
    },
    'pipeline': {
        'names': ('academic-pipeline', 'akademicheskii-konveer'),
        'modes': 'full',
        'description': 'Explicit full research-to-paper cycle only; coordinates research, writing, integrity, review, revision and finalization.',
        'instructions': 'Require an explicit full-cycle request; otherwise route to the requested component skill. Preserve the source state machine: research -> write -> integrity (2.5) -> review -> revise -> re-review -> re-revise if needed -> final integrity (4.5) -> finalize -> process summary. Retain user checkpoints and gate carryover; no finalization with unresolved blockers. Load corresponding same-language component overlays. Keep source_verification_state, profile bindings and bilingual handoff fields intact.',
    },
}


def git(*args):
    return subprocess.check_output(['git', '-C', str(REPO), *args], stderr=subprocess.PIPE)


def source_archive(revision):
    if revision.startswith('-'):
        raise ValueError('revision must not be an option')
    commit = git('rev-parse', '--verify', revision + '^{commit}').decode().strip()
    archive = tarfile.open(fileobj=io.BytesIO(git('archive', '--format=tar', commit)))
    files, records = {}, {}
    for member in archive:
        rel = PurePosixPath(member.name)
        if rel.is_absolute() or '..' in rel.parts:
            raise ValueError('unsafe archive path: ' + member.name)
        if member.isdir():
            continue
        if member.issym():
            link = PurePosixPath(member.linkname)
            # Validate against a synthetic root, without touching the filesystem.
            resolved = (Path('/snapshot') / str(rel.parent) / str(link)).resolve()
            if link.is_absolute() or not resolved.is_relative_to(Path('/snapshot')):
                raise ValueError('unsafe source symlink: ' + member.name)
            records[str(rel)] = {'symlink': member.linkname}
            files[str(rel)] = (member, None)
        elif member.isfile():
            content = archive.extractfile(member).read()
            records[str(rel)] = hashlib.sha256(content).hexdigest()
            files[str(rel)] = (member, content)
        else:
            raise ValueError('unsupported archive entry: ' + member.name)
    # No regular archive path may descend through a symlink.
    links = {key for key, value in records.items() if isinstance(value, dict)}
    for rel in files:
        if any(str(p) in links for p in PurePosixPath(rel).parents):
            raise ValueError('archive entry descends through symlink: ' + rel)
    required = ['LICENSE', 'NOTICE.md', 'THIRD_PARTY.md', 'shared/handoff_schemas.md',
                'scripts/ars_apply_revision_patch.py', 'shared/contracts/patch/revision_patch.schema.json']
    for family in FAMILIES.values():
        for name in family['names']:
            required.append(str(source_path(name) / 'SKILL.md'))
    for rel in required:
        if rel not in records:
            raise ValueError('incomplete source commit: ' + rel)
    return commit, files, records


def source_path(name):
    return Path('russian-academic-skills') / name if name.startswith('akadem') else Path(name)


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode()


def overlay(name, family, source, commit, source_manifest, target):
    ru = name.startswith('akadem')
    skill_source = source / source_path(name)
    description = ('Русскоязычная научная работа в DSH; выберите эту версию для русскоязычной рукописи/контекста, не загружайте EN-дубль. ' if ru else 'English/international academic work in DSH; use the Russian counterpart instead for Russian-language manuscript/context. ') + family['description']
    preflight_cmd = ' '.join(shlex.quote(str(p)) for p in ['python3', target / 'preflight.py', '--skill-dir', target, '--mode'])
    text = (f'---\nname: {name}\ndescription: {json.dumps(description, ensure_ascii=False)}\n---\n\n'
            f'# {name} — DSH\n\n'
            + ('Отвечайте по-русски, если пользователь не выбрал другой язык.\n\n' if ru else '')
            + HERE.joinpath('HOST.md').read_text(encoding='utf-8')
            + f'\n## Selected skill\n\n{family["instructions"]}\n\n'
            + f'Modes: {family["modes"]}.\n\n'
            + f'Pinned repository root: `{source}`\n\n'
            + f'Source skill directory: `{skill_source}`\n\n'
            + f'Read domain mode/protocols from: [{name} source](<{skill_source / "SKILL.md"}>). '
            + 'Foreign runtime instructions there are reference only under the translation contract above.\n\n'
            + f'Baseline preflight (replace MODE with selected mode):\n\n```sh\n{preflight_cmd} MODE\n```\n\n'
            + 'For format-convert also supply `--format markdown|docx|pdf|latex`.\n\n'
            + f'## Provenance\n\nSource commit: `{commit}` from the local fork of '
            + 'https://github.com/Imbad0202/academic-research-skills. '
            + 'Copyright (c) 2026 Cheng-I Wu; CC BY-NC 4.0. '
            + 'Russian adaptations retained unmodified. DSH changes: host routing, native dispatch and installation layer only. '
            + f'Full attribution: [LICENSE](<{source / "LICENSE"}>), [NOTICE](<{source / "NOTICE.md"}>), '
            + f'[THIRD_PARTY](<{source / "THIRD_PARTY.md"}>).\n')
    files = {'SKILL.md': text.encode(), 'preflight.py': HERE.joinpath('preflight.py').read_bytes()}
    manifest = {'owner': OWNER, 'skill': name, 'source_commit': commit, 'source_root': str(source),
                'source_manifest_sha256': hashlib.sha256(source_manifest).hexdigest(),
                'modes': family['modes'].split(),
                'files': {key: hashlib.sha256(value).hexdigest() for key, value in files.items()}}
    files['.dsh-managed.json'] = json_bytes(manifest)
    return files


def same_files(path, files):
    return (path.is_dir() and not path.is_symlink()
            and {p.name for p in path.iterdir()} == set(files)
            and all(not (path / rel).is_symlink() and (path / rel).is_file()
                    and (path / rel).read_bytes() == content for rel, content in files.items()))


def reject_symlinks(path):
    for part in [path, *path.parents]:
        if part.is_symlink():
            raise ValueError('symlink destination component refused: ' + str(part))


def install(skills_dir, revision='HEAD', dry_run=False, backup=False):
    # Resolve only after checking the explicitly supplied destination for links.
    raw = skills_dir.expanduser().absolute()
    reject_symlinks(raw)
    root = raw.resolve()
    test_root = REPO / '.context' / 'dsh-installer-tests'
    if (root in {Path('/'), Path.home().resolve(), REPO} or root in REPO.parents
            or (root.is_relative_to(REPO) and not root.is_relative_to(test_root))
            or root == test_root):
        raise ValueError('unsafe skills directory: ' + str(root))
    if root.exists() and not root.is_dir():
        raise ValueError('skills directory must be a directory')
    commit, archive, records = source_archive(revision)
    source = root / '.ars-dsh' / 'sources' / commit
    reject_symlinks(source)
    source_manifest = json_bytes(records)
    if (root / '.ars-dsh').exists():
        marker = root / '.ars-dsh' / '.owner'
        if marker.is_symlink() or not marker.is_file() or marker.read_text() != OWNER:
            raise ValueError('unmanaged .ars-dsh directory')
    reject_symlinks(root / '.ars-dsh' / 'backups')
    if source.exists():
        marker = source / '.dsh-source.json'
        if marker.is_symlink() or not marker.is_file() or marker.read_bytes() != source_manifest:
            raise ValueError('unmanaged/changed source snapshot; choose another skills directory')
        errors = verify_source(source, records)
        if errors:
            raise ValueError(errors[0])
    plans = []
    for family in FAMILIES.values():
        for name in family['names']:
            target = root / name
            reject_symlinks(target)
            files = overlay(name, family, source, commit, source_manifest, target)
            if target.exists() and not same_files(target, files):
                # Never discard user additions, even in a formerly managed target.
                if not backup:
                    raise ValueError('existing target differs; inspect and use --backup: ' + str(target))
                action = 'backup and replace'
            else:
                action = 'unchanged' if target.exists() else 'create'
            plans.append((target, files, action))
    print(json.dumps({'dry_run': dry_run, 'source_commit': commit, 'source_root': str(source),
                      'plan': {str(t): a for t, _, a in plans}}, indent=2))
    if dry_run:
        return
    if not source.exists():
        source.parent.mkdir(parents=True, exist_ok=True)
        (root / '.ars-dsh' / '.owner').write_text(OWNER)
        source.mkdir()
        # Paths and symlink destinations were validated above; no extractall.
        for rel, (member, content) in archive.items():
            path = source / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            if member.issym():
                path.symlink_to(member.linkname)
            else:
                path.write_bytes(content)
                path.chmod(0o755 if member.mode & 0o111 else 0o644)
        (source / '.dsh-source.json').write_bytes(source_manifest)
    for target, files, action in plans:
        if action == 'unchanged':
            continue
        if target.exists():
            backup_root = root / '.ars-dsh' / 'backups'
            reject_symlinks(backup_root)
            backup_root.mkdir(parents=True, exist_ok=True)
            saved = backup_root / (target.name + '.backup-' + uuid.uuid4().hex)
            # Resolved endpoints are checked immediately before the only move.
            if target.parent.resolve() != root or saved.parent.resolve() != backup_root or saved.exists():
                raise ValueError('unsafe backup endpoints')
            reject_symlinks(target)
            target.rename(saved)
            print('preserved backup: ' + str(saved))
        target.mkdir()
        for rel, content in files.items():
            (target / rel).write_bytes(content)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    dsh_home = Path(os.environ.get('DSH_HOME') or (Path.home() / '.dsh'))
    parser.add_argument('--skills-dir', type=Path, default=dsh_home / 'skills')
    parser.add_argument('--revision', default='HEAD', help='local commit/ref resolved once to a full SHA; default HEAD')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--backup', action='store_true', help='preserve differing targets by rename; never overwrite/delete them')
    args = parser.parse_args()
    try:
        install(args.skills_dir, args.revision, args.dry_run, args.backup)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print('DSH install refused: ' + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
