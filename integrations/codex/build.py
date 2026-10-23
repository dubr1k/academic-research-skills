#!/usr/bin/env python3
"""Build a Codex bundle in a new directory, without changing host configuration."""
import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import subprocess
import tarfile

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PIPELINES = {'academic-pipeline', 'akademicheskii-konveer'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.check_output(['git', '-C', str(REPO), *args])


def source_path(name):
    return (Path('russian-academic-skills') / name
            if name.startswith('akadem') else Path(name))


def source_files():
    """Use committed bytes, never dirty worktree files or executable hooks."""
    commit = git('rev-parse', 'HEAD').decode().strip()
    entries = {}
    with tarfile.open(fileobj=io.BytesIO(git('archive', '--format=tar', commit))) as archive:
        for member in archive:
            rel = PurePosixPath(member.name)
            if rel.is_absolute() or '..' in rel.parts:
                raise ValueError('unsafe source path')
            # Discovery symlinks and other host integrations are not source resources.
            if rel.parts[0] in {'skills', 'integrations'} or member.isdir():
                continue
            if not member.isfile():
                raise ValueError('unsupported source entry: ' + str(rel))
            entries[str(rel)] = (archive.extractfile(member).read(), member.mode)
    return commit, entries


def entrypoint(name, description, source):
    methodology = source / source_path(name) / 'SKILL.md'
    return f'''---
name: {name}
description: {json.dumps(description, ensure_ascii=False)}
---

# {name} — Codex

Use only the academic mode requested. Preserve the user's language, venue, citation style and scope. A short lookup or an isolated edit does not require the full publication workflow.

Read [Codex runtime](references/codex-runtime.md) for platform translation, delegation and project instructions. Then select the relevant mode from the [canonical methodology](<{methodology}>): start with headings or targeted search, and load the mode plus all applicable integrity and routing requirements. For a full workflow read every required stage. Resolve its relative links from that source document's directory.

Do not invent sources, identifiers, data or verification results. Preserve limitations and distinguish evidence from interpretation. Report missing independent review rather than simulating it. For an Office/PDF deliverable, use the available format-specific skill for rendering and visual checks.

Source snapshot root: `{source}`. Scientific content and attribution remain in that snapshot, including LICENSE and NOTICE.md. Other runtimes' APIs, hooks and model names in source documents are translated by the Codex runtime reference; scientific gates remain applicable.
'''


def build(destination, explicit_pipelines=False):
    destination = Path(destination).expanduser().absolute()
    for p in (destination, *destination.parents):
        if p.is_symlink():
            raise ValueError('symlink destination component refused')
    destination = destination.resolve()
    if (destination == REPO or destination in REPO.parents
            or REPO in destination.parents):
        raise ValueError('destination must be outside the source checkout')
    if destination.exists():
        raise FileExistsError('destination already exists; choose a new bundle directory')
    commit, entries = source_files()
    descriptions = json.loads((HERE / 'descriptions.json').read_text())
    for name in descriptions:
        if str(source_path(name) / 'SKILL.md') not in entries:
            raise ValueError('missing source skill: ' + name)
    for required in ('LICENSE', 'NOTICE.md', 'shared/handoff_schemas.md'):
        if required not in entries:
            raise ValueError('missing source resource: ' + required)
    source = destination / 'source'
    runtime = (HERE / 'RUNTIME.md').read_bytes()
    outputs = {}
    for name, description in descriptions.items():
        outputs[f'skills/{name}/SKILL.md'] = entrypoint(name, description, source).encode()
        outputs[f'skills/{name}/references/codex-runtime.md'] = runtime
        # This opt-in preserves the host default unless the operator selects it.
        if explicit_pipelines and name in PIPELINES:
            outputs[f'skills/{name}/agents/openai.yaml'] = (
                b'policy:\n  allow_implicit_invocation: false\n')
    manifest = {
        'source_repository': 'https://github.com/dubr1k/academic-research-skills',
        'source_commit': commit,
        'source_files': {rel: sha(data) for rel, (data, _) in entries.items()},
        'generated_files': {rel: sha(data) for rel, data in outputs.items()},
        'adapter_files': {name: sha((HERE / name).read_bytes())
                          for name in ('build.py', 'descriptions.json', 'RUNTIME.md')},
        'explicit_pipelines': explicit_pipelines,
        'runtime_dependency_on_source_checkout': False,
    }
    # All inputs have been checked. Exclusive mkdir refuses existing destinations.
    destination.mkdir(parents=True, exist_ok=False)
    for rel, (data, mode) in entries.items():
        target = source / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        target.chmod(0o755 if mode & 0o111 else 0o644)
    for rel, data in outputs.items():
        target = destination / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    (destination / 'MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', required=True)
    parser.add_argument('--explicit-pipelines', action='store_true',
                        help='make both full-cycle skills explicit-only')
    args = parser.parse_args()
    try:
        manifest = build(args.destination, args.explicit_pipelines)
    except (ValueError, FileExistsError, subprocess.CalledProcessError) as error:
        parser.exit(2, str(error) + '\n')
    print(json.dumps({'source_commit': manifest['source_commit'],
                      'skills': sum(p.endswith('/SKILL.md') for p in manifest['generated_files']),
                      'destination': str(Path(args.destination).expanduser().absolute())}))


if __name__ == '__main__':
    main()
