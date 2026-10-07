"""Portable offline contracts; no live profile or network access."""
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
SOURCE = HERE.parents[1]
spec = importlib.util.spec_from_file_location('installer', HERE / 'install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name) / 'home'
        installer.install(self.home)

    def test_no_source_dependency_and_refuse_overwrite(self):
        with self.assertRaises(FileExistsError):
            installer.install(self.home)
        with self.assertRaises(ValueError):
            installer.install(SOURCE)
        with self.assertRaises(ValueError):
            installer.install(SOURCE / 'unsafe')
        with self.assertRaises(ValueError):
            installer.install(SOURCE.parent)

    def test_symlink_destinations_rejected_before_any_write(self):
        outside = Path(self.tmp.name) / 'outside'
        outside.mkdir()
        for rel in ['skills', 'skills/research', 'skills/education', 'skill-bundles']:
            with self.subTest(rel=rel):
                home = Path(self.tmp.name) / ('safe-' + rel.replace('/', '-'))
                home.mkdir()
                # Only parents used by this package can affect writes.
                if not any(home / rel == t or home / rel in t.parents for t in installer.TARGETS(home)):
                    continue
                link = home / rel
                link.parent.mkdir(parents=True, exist_ok=True)
                link.symlink_to(outside, target_is_directory=True)
                with self.assertRaises(ValueError):
                    installer.install(home)
                self.assertEqual(list(outside.iterdir()), [])
        home = Path(self.tmp.name) / 'dangling-home'
        home.mkdir()
        target = installer.TARGETS(home)[0]
        target.parent.mkdir(parents=True)
        target.symlink_to(outside / 'not-present')
        with self.assertRaises(ValueError):
            installer.install(home)
        self.assertFalse((outside / 'not-present').exists())

    def test_public_templates_have_no_private_machine_paths(self):
        for p in HERE.rglob('*'):
            if p.suffix not in {'.md', '.py'}:
                continue
            if p == Path(__file__):
                continue
            text = p.read_text()
            for forbidden in ['/Users/', '/root/', '/opt/anaconda', 'SOUL.md', 'ghp_', 'gho_']:
                self.assertNotIn(forbidden, text, str(p))


    def test_complete_source_hashes(self):
        suite = self.home / 'skills/research/academic-suite'
        manifest = json.loads((suite / 'HERMES-INSTALL-MANIFEST.json').read_text())
        expected = [p for p in installer.tracked_files() if p.parts[0] not in {'skills', 'integrations', '.git'}]
        self.assertEqual(set(manifest['upstream_files']), {str(p) for p in expected})
        for rel in expected:
            self.assertEqual(installer.digest(SOURCE / rel), installer.digest(suite / rel), str(rel))
        self.assertFalse(manifest['runtime_dependency_on_source_checkout'])
        self.assertFalse((suite / 'integrations').exists())
        self.assertFalse((suite / 'skills').exists())
        self.assertFalse(any(p.is_symlink() for p in suite.rglob('*')))

    def test_unique_discovery_bundle_and_business_reference(self):
        suite = self.home / 'skills/research/academic-suite'
        skills = sorted(suite.rglob('SKILL.md'))
        self.assertEqual(len(skills), 9)
        names = [next(line.split(':', 1)[1].strip() for line in p.read_text().splitlines() if line.startswith('name:')) for p in skills]
        self.assertEqual(len(set(names)), 9)
        bundle = (self.home / 'skill-bundles/academic.yaml').read_text()
        for name in names + ['academic-research-routing']:
            self.assertIn('  - ' + name + '\n', bundle)
        router = self.home / 'skills/research/academic-research-routing'
        rel = 'references/applied-business-materials-audit.md'
        self.assertEqual((router / rel).read_bytes(), (HERE / 'academic-research-routing' / rel).read_bytes())
        self.assertIn(rel, (router / 'SKILL.md').read_text())

    def test_routing_language_independence_and_ledger_guards(self):
        router = self.home / 'skills/research/academic-research-routing'
        text = (router / 'SKILL.md').read_text()
        runtime = (router / 'references/hermes-runtime-contract.md').read_text()
        for expected in ['active Hermes profile', 'Do not use profile `default`', 'Screening is opt-in',
                         'never automatically selects `sr-screener`', 'not OS/process/filesystem/tool isolation',
                         'The main assistant writes substantive research/manuscript text itself']:
            self.assertIn(expected, text)
        for expected in ['only `output_language_pair: zh-tw-en`', 'Never invent or serialize `ru-en`',
                         'omission retains Traditional Chinese/English behavior',
                         'stop and report the unsupported contract', 'checkpoint opens/closes',
                         'not reconstructed success', 'Missing model/worker independence blocks']:
            self.assertIn(expected, runtime)
        result = subprocess.run([sys.executable, 'scripts/run_ledger.py', '--help'],
                                cwd=self.home / 'skills/research/academic-suite', capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        for command in ['append', 'report', 'show']:
            self.assertIn(command, result.stdout)


if __name__ == '__main__':
    unittest.main()
