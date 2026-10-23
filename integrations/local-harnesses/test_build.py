import importlib.util
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('local_bundle', HERE / 'build.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class AdapterTests(unittest.TestCase):
    def test_host_boundary_and_explicit_pipeline(self):
        claude = builder.entrypoint('academic-pipeline', 'Full explicit cycle', Path('/snapshot'), 'claude')
        shared = builder.entrypoint('academic-pipeline', 'Full explicit cycle', Path('/snapshot'), 'shared')
        self.assertIn('disable-model-invocation: true', claude)
        self.assertNotIn('disable-model-invocation:', shared)
        self.assertIn('/snapshot/academic-pipeline/SKILL.md', claude)
        self.assertIn('Russian language does not imply Russia or ГОСТ', shared)

    def test_commands_preserve_mode_and_resolve_plugin_paths(self):
        text = '''---\ndescription: citation check\nmodel: sonnet\n---\nFirst invoke the Skill tool with `skill: "academic-research-skills:academic-paper"`.\nMode citation-check; `${CLAUDE_PLUGIN_ROOT}/commands/example.md`\n$ARGUMENTS\n'''
        adapted = builder.command(text, Path('/snapshot'))
        self.assertNotIn('model: sonnet', adapted)
        self.assertNotIn('${CLAUDE_PLUGIN_ROOT}', adapted)
        self.assertNotIn('academic-research-skills:academic-paper', adapted)
        self.assertIn('Mode citation-check', adapted)
        self.assertIn('$ARGUMENTS', adapted)

    def test_build_preserves_committed_source_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve() / 'bundle'
            manifest = builder.build(root)
            self.assertEqual((root / 'LICENSE').read_bytes(), builder.core.git('show', 'HEAD:LICENSE'))
            self.assertEqual(len(list((root / 'host-commands').glob('*.md'))), 21)
            self.assertEqual(len(list((root / 'host-skills/claude').glob('*/SKILL.md'))), 8)
            for rel, digest in manifest['generated_files'].items():
                self.assertEqual(builder.core.sha((root / rel).read_bytes()), digest)
            with self.assertRaises(FileExistsError):
                builder.build(root)


if __name__ == '__main__':
    unittest.main()
