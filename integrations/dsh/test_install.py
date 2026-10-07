"""Offline installer contract; run with python3 -m unittest discover -s integrations/dsh."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
spec = importlib.util.spec_from_file_location('dsh_preflight', HERE / 'preflight.py')
preflight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preflight)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        staging = REPO / '.context' / 'dsh-installer-tests'
        staging.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix='test-', dir=staging)
        self.root = Path(self.temp.name)
        self.skills = self.root / 'skills with spaces'

    def tearDown(self):
        self.temp.cleanup()

    def run_install(self, *args, ok=True):
        p = subprocess.run([sys.executable, str(HERE / 'install.py'), '--skills-dir', str(self.skills), *args], capture_output=True, text=True)
        self.assertEqual(p.returncode == 0, ok, p.stdout + p.stderr)
        return p

    def test_dry_run_is_read_only(self):
        self.run_install('--dry-run')
        self.assertFalse(self.skills.exists())

    def test_dsh_home_and_explicit_override(self):
        import os
        env = dict(os.environ, DSH_HOME=str(self.root / 'profile home'))
        for args, expected in [([], self.root / 'profile home' / 'skills'),
                               (['--skills-dir', str(self.skills)], self.skills)]:
            p = subprocess.run([sys.executable, str(HERE / 'install.py'), '--dry-run', *args], env=env, capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            self.assertEqual(Path(json.loads(p.stdout)['source_root']).parents[2], expected)
            self.assertFalse(expected.exists())
        # Empty DSH_HOME must fall back to HOME/.dsh, without touching real HOME.
        env.update(DSH_HOME='', HOME=str(self.root / 'fake home'))
        p = subprocess.run([sys.executable, str(HERE / 'install.py'), '--dry-run'], env=env, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertEqual(Path(json.loads(p.stdout)['source_root']).parents[2], self.root / 'fake home' / '.dsh' / 'skills')
        self.assertFalse((self.root / 'fake home').exists())

    def test_install_pinned_resources_and_idempotence(self):
        self.run_install()
        overlays = list(self.skills.glob('*/SKILL.md'))
        self.assertEqual(len(overlays), 8)
        self.assertFalse((self.skills / '.ars-dsh' / 'SKILL.md').exists())
        manifest = json.loads((self.skills / 'academic-paper' / '.dsh-managed.json').read_text())
        source = Path(manifest['source_root'])
        for rel in ['shared/handoff_schemas.md', 'scripts/ars_apply_revision_patch.py', 'LICENSE',
                    'shared/agents/compliance_agent.md', 'shared/compliance_checkpoint_protocol.md',
                    'russian-academic-skills/akademicheskaya-statya/SKILL.md']:
            self.assertTrue((source / rel).is_file(), rel)
        self.run_install()
        self.assertFalse((self.skills / '.ars-dsh' / 'backups').exists())
        for path in overlays:
            text = path.read_text()
            for phrase in ['subagent', 'subagent_fork', 'send_message', 'fresh', 'prompt-only', 'workflow', 'preflight', 'reference only']:
                self.assertIn(phrase, text)
            self.assertNotIn('\nmodel:', text)
            self.assertNotIn('\ntools:', text)
        # Run representative existing validators from the INSTALLED snapshot,
        # not the working checkout; their relative imports/resources must work.
        for script in ['check_role_scoped_contract.py', 'check_390_revision_patch_discipline.py']:
            p = subprocess.run([sys.executable, '-B', str(source / 'scripts' / script)], cwd=self.root, capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        p = subprocess.run([sys.executable, str(self.skills / 'academic-paper' / 'preflight.py'), '--skill-dir', str(self.skills / 'academic-paper'), '--mode', 'revision'], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertEqual(json.loads(p.stdout)['quality_gates'], 'not_run')
        (source / 'shared/agents/compliance_agent.md').write_text('tampered')
        p = subprocess.run([sys.executable, str(self.skills / 'academic-paper' / 'preflight.py'), '--skill-dir', str(self.skills / 'academic-paper'), '--mode', 'revision'], capture_output=True, text=True)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('compliance_agent.md', p.stdout)
        self.run_install(ok=False)

    def test_conflicts_are_checked_before_any_install(self):
        conflict = self.skills / 'deep-research'
        conflict.mkdir(parents=True)
        (conflict / 'SKILL.md').write_text('user content')
        self.run_install(ok=False)
        self.assertEqual((conflict / 'SKILL.md').read_text(), 'user content')
        self.assertFalse((self.skills / '.ars-dsh').exists())
        self.run_install('--backup', '--dry-run')
        self.assertFalse((self.skills / '.ars-dsh').exists())
        self.run_install('--backup')
        backups = list((self.skills / '.ars-dsh' / 'backups').glob('deep-research.backup-*'))
        self.assertEqual(len(backups), 1)
        self.assertEqual((backups[0] / 'SKILL.md').read_text(), 'user content')
        self.assertEqual(len(list(self.skills.glob('*/SKILL.md'))), 8)

    def test_symlink_target_refused_even_with_backup(self):
        self.skills.mkdir()
        (self.skills / 'academic-paper').symlink_to(self.root / 'elsewhere', target_is_directory=True)
        self.run_install('--backup', ok=False)
        self.assertFalse((self.root / 'elsewhere').exists())

    def test_unsafe_destination_and_invalid_revision(self):
        for path in [REPO, Path.home(), Path('/'), REPO / 'russian-academic-skills', REPO / 'integrations' / 'dsh', REPO / '.context' / 'dsh-installer-tests']:
            for flags in [[], ['--dry-run']]:
                p = subprocess.run([sys.executable, str(HERE / 'install.py'), '--skills-dir', str(path), '--backup', *flags], capture_output=True, text=True)
                self.assertNotEqual(p.returncode, 0)
                self.assertIn('unsafe skills directory', p.stderr)
        self.assertFalse((REPO / 'russian-academic-skills' / '.ars-dsh').exists())
        self.run_install('--revision', '--help', ok=False)
        self.run_install('--revision', 'not-a-commit', ok=False)

    def test_local_overlay_edits_require_backup(self):
        self.run_install()
        (self.skills / 'academic-paper' / 'notes.txt').write_text('keep me')
        self.run_install(ok=False)
        self.run_install('--backup')
        backups = list((self.skills / '.ars-dsh' / 'backups').glob('academic-paper.backup-*'))
        self.assertEqual((backups[0] / 'notes.txt').read_text(), 'keep me')

    def test_unmanaged_cache_and_symlink_cache_refused(self):
        cache = self.skills / '.ars-dsh'
        cache.mkdir(parents=True)
        (cache / 'user-data').write_text('keep')
        self.run_install('--backup', ok=False)
        self.assertEqual((cache / 'user-data').read_text(), 'keep')
        (cache / '.owner').write_text('academic-research-skills/dsh-v1')
        (cache / 'sources').symlink_to(self.root / 'escape', target_is_directory=True)
        self.run_install('--backup', ok=False)
        self.assertFalse((self.root / 'escape').exists())

    def test_preflight_missing_dependencies_invalid_mode_export_and_hashes(self):
        self.run_install()
        skill = self.skills / 'academic-paper'
        result = preflight.check(skill, 'revision', module_available=lambda _: False)
        self.assertEqual(result['status'], 'blocked')
        self.assertIn('missing Python module: jsonschema', result['errors'])
        self.assertIn('missing Python module: yaml', result['errors'])
        self.assertEqual(preflight.check(skill, 'quick')['status'], 'blocked')
        self.assertEqual(preflight.check(self.skills / 'deep-research', 'fact-check', module_available=lambda _: False)['status'], 'baseline_ready')
        self.assertEqual(preflight.check(skill, 'format-convert')['status'], 'blocked')
        result = preflight.check(skill, 'format-convert', 'pdf', which=lambda _: None)
        self.assertEqual(result['status'], 'blocked')
        self.assertTrue(any('pandoc' in e for e in result['errors']))
        (skill / 'SKILL.md').write_text('changed overlay')
        self.assertEqual(preflight.check(skill, 'revision')['status'], 'blocked')


if __name__ == '__main__':
    unittest.main()
