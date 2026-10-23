#!/usr/bin/env python3
"""Build a self-contained Claude/OpenCode/shared bundle; never edit host config."""
import argparse
import importlib.util
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
spec = importlib.util.spec_from_file_location('codex_bundle', HERE.parent / 'codex/build.py')
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)
NAMES = ('academic-paper', 'academic-paper-reviewer', 'academic-pipeline',
         'deep-research', 'akademicheskaya-statya', 'akademicheskii-retsenzent',
         'akademicheskii-konveer', 'akademicheskoe-issledovanie')


def entrypoint(name, description, root, host):
    explicit = '\ndisable-model-invocation: true' if host == 'claude' and name in core.PIPELINES else ''
    return f'''---
name: {name}
description: {json.dumps(description, ensure_ascii=False)}{explicit}
---

# {name}

Choose only the academic mode requested by the user. A short lookup, small edit,
or two academic intentions do not authorize a full publication pipeline.
Full publication workflows require an explicit request. Preserve the requested
language, venue and citation style; Russian language does not imply Russia or ГОСТ.

First read [runtime translation](references/runtime.md). Select the relevant mode
from the [canonical methodology](<{root / core.source_path(name) / 'SKILL.md'}>),
starting with headings or targeted search, then load the mode and its applicable
integrity and routing requirements. For an explicitly requested full workflow,
read every required stage. Resolve source-relative references from that source file.

Use [Russian academic context](<{root / 'docs/russian-academic-context.md'}>) when
the request calls for it. Do not invent sources, data, citations or successful checks.
Keep independent-review requirements for a selected workflow; disclose an absent
independent review instead of claiming it happened. For Office/PDF output use the
available format tool and render/inspect the deliverable.

Canonical snapshot: `{root}`. Scientific content, LICENSE and NOTICE.md are
preserved there. Runtime translation overrides foreign tool/API/model examples,
not scientific integrity requirements.
'''


def command(text, root):
    # User commands are not plugin commands: preserve mode content, resolve paths,
    # drop model overrides, and invoke the installed host-neutral skill by name.
    if not text.startswith('---\n'):
        raise ValueError('command lacks frontmatter')
    front, body = text[4:].split('\n---', 1)
    front = '\n'.join(line for line in front.splitlines()
                      if not re.match(r'^(model|effort|allowed-tools|context|agent|disable-model-invocation):', line))
    front += '\ndisable-model-invocation: true'
    body = body.replace('${CLAUDE_PLUGIN_ROOT}', str(root))
    body = re.sub(r'First invoke the Skill tool with `skill: "academic-research-skills:([^"]+)"`\.',
                  lambda m: (f'First load the installed skill `{m[1]}` using this host\'s actual skill tool schema. '
                             f'If this explicit user command cannot invoke that skill because it is user-only, '
                             f'read its scoped adapter at `{root / "host-skills/shared" / m[1] / "SKILL.md"}` directly.'), body)
    preface = (f'\n\nRead `{root / "host-runtime.md"}` before executing this command. '
               'Preserve the explicit mode and user scope; do not infer a full pipeline from multiple intentions. '
               'Use the user-requested output language and citation style; Russian does not imply ГОСТ.\n')
    return '---\n' + front + '\n---' + preface + body


def build(destination):
    destination = Path(destination).expanduser().absolute()
    if any(p.is_symlink() for p in (destination, *destination.parents)):
        raise ValueError('symlink destination refused')
    if destination.exists():
        raise FileExistsError('choose a new destination')
    if destination == REPO or REPO in destination.parents or destination in REPO.parents:
        raise ValueError('destination must be outside checkout')
    commit, files = core.source_files()
    descriptions = json.loads((HERE.parent / 'codex/descriptions.json').read_text())
    runtime = (HERE / 'RUNTIME.md').read_bytes()
    outputs = {'host-runtime.md': runtime}
    for host in ('claude', 'shared'):
        for name in NAMES:
            if str(core.source_path(name) / 'SKILL.md') not in files:
                raise ValueError('missing source skill: ' + name)
            prefix = f'host-skills/{host}/{name}'
            outputs[prefix + '/SKILL.md'] = entrypoint(name, descriptions[name], destination, host).encode()
            outputs[prefix + '/references/runtime.md'] = runtime
    for rel, (raw, _) in files.items():
        if re.fullmatch(r'commands/ars-[^/]+\.md', rel):
            outputs['host-commands/' + Path(rel).name] = command(raw.decode(), destination).encode()
    destination.mkdir(parents=True)
    for rel, (raw, mode) in files.items():
        target = destination / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        target.chmod(0o755 if mode & 0o111 else 0o644)
    for rel, raw in outputs.items():
        target = destination / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    manifest = {'source_commit': commit, 'source_files': {rel: core.sha(raw) for rel, (raw, _) in files.items()},
                'generated_files': {rel: core.sha(raw) for rel, raw in outputs.items()},
                'adapter_files': {name: core.sha((HERE / name).read_bytes()) for name in ('build.py', 'RUNTIME.md')},
                'platforms': ['claude', 'opencode', 'shared'], 'source_checkout_dependency': False}
    (destination / 'HOST-MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', required=True)
    args = parser.parse_args()
    print(json.dumps({'source_commit': build(args.destination)['source_commit'], 'destination': args.destination}))
