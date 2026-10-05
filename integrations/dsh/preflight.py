#!/usr/bin/env python3
"""Read-only baseline dependency/resource checks, NOT a scientific quality gate."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_source(root, records):
    errors = []
    for rel, expected in records.items():
        path = root / rel
        if Path(rel).is_absolute() or '..' in Path(rel).parts:
            errors.append('unsafe recorded path: ' + rel)
            continue
        if not path.resolve().is_relative_to(root.resolve()):
            errors.append('escaping source path: ' + rel)
        elif isinstance(expected, dict):
            if not path.is_symlink() or str(path.readlink()) != expected['symlink']:
                errors.append('changed source symlink: ' + rel)
        elif path.is_symlink() or not path.is_file() or digest(path) != expected:
            errors.append('missing/changed source: ' + rel)
    return errors


def check(skill_dir, mode, output_format=None, module_available=None, which=None):
    module_available = module_available or (lambda name: importlib.util.find_spec(name) is not None)
    which = which or shutil.which
    manifest = json.loads((skill_dir / '.dsh-managed.json').read_text(encoding='utf-8'))
    root = Path(manifest['source_root'])
    errors = []
    if mode not in manifest['modes']:
        errors.append('unsupported mode: ' + mode)
    for rel, expected in manifest['files'].items():
        file = skill_dir / rel
        if file.is_symlink() or not file.is_file() or digest(file) != expected:
            errors.append('missing/changed overlay: ' + rel)
    source_manifest = root / '.dsh-source.json'
    if not source_manifest.is_file() or digest(source_manifest) != manifest['source_manifest_sha256']:
        errors.append('missing/changed source manifest')
    else:
        records = json.loads(source_manifest.read_text(encoding='utf-8'))
        errors.extend(verify_source(root, records))
    # Deliberately conservative baseline for contract-bearing modes. Extension
    # imports/APIs still require the selected script's own preflight.
    requirements = [] if mode in {'quick', 'fact-check', 'socratic', 'abstract', 'outline', 'plan'} else ['jsonschema', 'yaml']
    for module in requirements:
        if not module_available(module):
            errors.append('missing Python module: ' + module)
    if mode == 'format-convert' and output_format is None:
        errors.append('format-convert requires --format markdown|docx|pdf|latex')
    if output_format in {'docx', 'pdf'} and not which('pandoc'):
        errors.append('missing executable: pandoc')
    if output_format == 'pdf' and not any(which(x) for x in ('xelatex', 'pdflatex', 'lualatex')):
        errors.append('missing PDF engine: xelatex/pdflatex/lualatex (select and test actual engine)')
    return {'status': 'blocked' if errors else 'baseline_ready', 'mode': mode,
            'source_commit': manifest['source_commit'], 'errors': errors,
            'quality_gates': 'not_run',
            'remaining_checks': ['selected gate imports and inputs', 'available native tools',
                                 'network/API access when required', 'optional mode extensions',
                                 'actual validators and human checkpoints']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skill-dir', type=Path, required=True)
    parser.add_argument('--mode', required=True)
    parser.add_argument('--format', choices=['markdown', 'docx', 'pdf', 'latex'])
    args = parser.parse_args()
    try:
        report = check(args.skill_dir.resolve(), args.mode, args.format)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        report = {'status': 'blocked', 'errors': [str(exc)], 'quality_gates': 'not_run'}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report['status'] == 'blocked' else 0


if __name__ == '__main__':
    sys.exit(main())
