import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('codex_bundle', HERE / 'build.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class BundleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.bundle = Path(cls.tmp.name).resolve() / 'bundle with spaces'
        cls.manifest = builder.build(cls.bundle, explicit_pipelines=True)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_all_committed_resources_preserved_byte_for_byte(self):
        commit, entries = builder.source_files()
        self.assertEqual(self.manifest['source_commit'], commit)
        self.assertEqual(set(entries), set(self.manifest['source_files']))
        for rel, (expected, mode) in entries.items():
            actual = self.bundle / 'source' / rel
            self.assertEqual(actual.read_bytes(), expected, rel)
            self.assertEqual(builder.sha(expected), self.manifest['source_files'][rel])
            self.assertEqual(bool(actual.stat().st_mode & 0o111), bool(mode & 0o111))
        self.assertFalse(self.manifest['runtime_dependency_on_source_checkout'])

    def test_nine_short_entrypoints_and_resolved_resources(self):
        skills = list((self.bundle / 'skills').glob('*/SKILL.md'))
        self.assertEqual(len(skills), 9)
        for skill in skills:
            text = skill.read_text()
            self.assertLess(len(text), 2500)
            self.assertTrue((skill.parent / 'references/codex-runtime.md').is_file())
            methodology = self.bundle / 'source' / builder.source_path(skill.parent.name) / 'SKILL.md'
            self.assertIn(f'(<{methodology}>)', text)
            self.assertTrue(methodology.is_file())
        for rel, digest in self.manifest['generated_files'].items():
            self.assertEqual(builder.sha((self.bundle / rel).read_bytes()), digest)

    def test_explicit_pipeline_opt_in_only(self):
        metadata = list((self.bundle / 'skills').glob('*/agents/openai.yaml'))
        self.assertEqual({p.parents[1].name for p in metadata}, builder.PIPELINES)
        for p in metadata:
            self.assertEqual(p.read_text(), 'policy:\n  allow_implicit_invocation: false\n')
        other = Path(self.tmp.name).resolve() / 'default'
        try:
            builder.build(other)
            self.assertEqual(list((other / 'skills').glob('*/agents/openai.yaml')), [])
        finally:
            import shutil
            shutil.rmtree(other, ignore_errors=True)

    def test_existing_destination_preserved(self):
        marker = self.bundle / 'user-note.txt'
        marker.write_text('keep this')
        with self.assertRaises(FileExistsError):
            builder.build(self.bundle)
        self.assertEqual(marker.read_text(), 'keep this')

    def test_symlink_and_source_overlap_rejected(self):
        outside = Path(self.tmp.name).resolve() / 'outside'
        outside.mkdir(exist_ok=True)
        link = Path(self.tmp.name).resolve() / 'link'
        link.symlink_to(outside, target_is_directory=True)
        for dest in (link / 'child', builder.REPO / 'bad-bundle', builder.REPO.parent):
            with self.subTest(destination=dest), self.assertRaises(ValueError):
                builder.build(dest)
        self.assertEqual(list(outside.iterdir()), [])

    def test_runtime_keeps_review_limits_and_project_instructions(self):
        runtime = (HERE / 'RUNTIME.md').read_text()
        for phrase in ('CLAUDE.md', 'fresh context', 'Stage 2.5 and 4.5',
                       'run-ledger', 'source-risk', 'Screening starts only'):
            self.assertIn(phrase, runtime)
        self.assertNotIn('../../instructions/', runtime)


if __name__ == '__main__':
    unittest.main()
