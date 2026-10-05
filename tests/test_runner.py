"""Runner safeguards, not empirical validation."""
import csv
import importlib.util
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('replicate', ROOT / 'scripts/replicate.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)

class RunnerTests(unittest.TestCase):
    def test_scaffold(self):
        self.assertEqual(len(r.validate(ROOT)), 7)

    def test_unfinished_run_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            shutil.copytree(ROOT / 'config', root / 'config')
            stages = r.validate(root)
            errors = r.readiness(root, stages)
            self.assertTrue(any('Missing input' in e for e in errors))
            self.assertTrue(any('Original code not integrated' in e for e in errors))
            with self.assertRaisesRegex(RuntimeError, 'Preflight blocked'):
                r.run(root, stages)
            self.assertFalse((root / 'logs').exists())

    def test_checksum_mismatch(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            shutil.copytree(ROOT / 'config', root / 'config')
            rows = r.rows(root / 'config/data_manifest.csv')
            p = root / rows[0]['path']
            p.parent.mkdir(parents=True)
            p.write_bytes(b'wrong input')
            rows[0]['sha256'] = '0' * 64
            with (root / 'config/data_manifest.csv').open('w', newline='') as f:
                w = csv.DictWriter(f, fieldnames=list(rows[0]))
                w.writeheader()
                w.writerows(rows)
            self.assertTrue(any('Checksum mismatch' in e for e in r.readiness(root, r.validate(root))))

    def test_missing_or_stale_output(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            stage = dict(id='01_test', inputs=[], outputs=['result.txt'], command=[sys.executable, '-c', 'pass'])
            with self.assertRaisesRegex(RuntimeError, 'not created'):
                r.run_stage(root, stage, root)
            (root / 'result.txt').write_text('stale')
            with self.assertRaisesRegex(RuntimeError, 'already exists'):
                r.run_stage(root, stage, root)

    def test_failed_stage(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            stage = dict(id='01_test', inputs=[], outputs=['result.txt'], command=[sys.executable, '-c', "from pathlib import Path; Path('result.txt').write_text('partial'); raise SystemExit(7)"])
            with self.assertRaisesRegex(RuntimeError, r'failed \(7\)'):
                r.run_stage(root, stage, root)

    def test_successful_stage(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            stage = dict(id='01_test', inputs=[], outputs=['result.txt'], command=[sys.executable, '-c', "from pathlib import Path; Path('result.txt').write_text('created')"])
            r.run_stage(root, stage, root)
            self.assertEqual((root / 'result.txt').read_text(), 'created')

    def test_path_escape(self):
        with self.assertRaises(ValueError):
            r.local(ROOT, '../outside.txt')

if __name__ == '__main__':
    unittest.main()
