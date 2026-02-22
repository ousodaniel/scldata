import os
import subprocess
import sys
from contextlib import redirect_stdout
import unittest
from io import StringIO
from itertools import chain
from pathlib import Path
from unittest.mock import patch

import scldata
from scldata.loader import load
from scldata import main, loader


class TestScldataPkg(unittest.TestCase):

    def test_import_package(self):
        self.assertTrue(hasattr(scldata, '__version__'))

    def test_import_submodule_load(self):
        self.assertTrue(callable(getattr(loader, 'load', None)))

    def test_import_submodule_main(self):
        self.assertTrue(callable(getattr(scldata, 'main', None)))

    def test_load_kfold_input(self):
        self.assertRaises(ValueError, load, 5)
        self.assertRaises(ValueError, load, -5)

    def test_kfold_output_is_train_test(self):
        train_test = load('0')
        self.assertEqual(len(train_test), 2, 'Fold loading not returning train and test sets')

    def test_main_output(self):
        with open('output.txt', 'w') as f:
            with redirect_stdout(f):
                main()
        self.assertGreater(os.path.getsize('output.txt'), 0, 'Output file should not be empty')
        if os.path.exists('output.txt'):
            os.remove('output.txt')

    def tearDown(self):
        pass

class TestScldataCli(unittest.TestCase):

    def setUp(self):
        self.project_root = Path(__file__).resolve().parents[1]
        self.script_path = self.project_root / 'src' / 'scldata' / '__init__.py'
        self.output_file = 'test-scldata-file-saving'

    @patch('sys.argv', ['myscript.py', '--scls'])
    def test_main_with_scls(self):
        self.scls = '\n'.join([
            'Membrane',
            'Cytoplasm',
            'Nucleus',
            'ER',
            'Secreted',
            'Plastid',
            'Cytoplasm;Nucleus',
            'Centrosome;Cytoplasm;Cytoskeleton;Microtubule organizing center',
            'Cytoplasm;Membrane',
            'Mitochondrion',
            'Cell projection',
            'Cytoplasm;Cytoskeleton',
            'Peroxisome'
        ])

        buffer = StringIO()
        with redirect_stdout(buffer):
            main()

        output = buffer.getvalue()
        self.assertIn("SCL2205 Target Classes", output)
        self.assertIn("Membrane", output)
        expected_output = f'SCL2205 Target Classes:\n\n{self.scls}'
        self.assertEqual(expected_output.strip(), output.strip(), f'Expected 13 Classes:\n{expected_output}')

    def test_cli_execution(self):
        result = subprocess.run(
            [sys.executable, self.script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        self.assertEqual(result.returncode, 0, 'The script returned exit code 1, all was not ok')
        self.assertIn('SCL2205 Full (Head):', result.stdout, 'The SCL2205 Full head output failed, should be printed when "scldata" command (script) is run without any arguments')

    @patch('sys.stderr', new_callable=StringIO)  # Silence error messages
    @patch('sys.stdout', new_callable=StringIO)  # Silence standard prints
    @patch('sys.argv', ['myscript.py', '--split', 'dev'])
    def test_invalid_option_arg(self, mock_stdout, mock_stderr):
        with self.assertRaises(SystemExit):
            main()

    def test_piping_broken_pipe_error(self):
        cmd = [sys.executable, '-u', self.script_path, '--info', 'all', '--split', 'heldout']
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        try:
            if process.stdout:
                process.stdout.read(10)
                process.stdout.close()
        finally:
            _, stderr_data = process.communicate()

        self.assertEqual(process.returncode, 0, f"Script failed with stderr: {stderr_data}")
        self.assertNotIn('BrokenPipeError', stderr_data)
        self.assertNotIn('Traceback', stderr_data)

    def test_fasta_output(self):
        cmd = [sys.executable, '-u', self.script_path, '-s', 'heldout', '-f', 'fasta']

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0)

        header_count = result.stdout.count('>')
        self.assertGreater(header_count, 0, 'No FASTA headers found in output')

    def test_fasta_tv_default_output_is_10_seq(self):
        cmd = [sys.executable, '-u', self.script_path, '-s', 'heldout', '-f', 'fasta']

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0)

        header_count = result.stdout.count('>')
        self.assertEqual(header_count, 10, 'Output is not 10 sequences')

    def test_fasta_file_output_written_tv_fasta(self):
        cmd = [sys.executable, '-u', self.script_path, '-s', 'heldout', '-f', 'fasta', '-o', self.output_file]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0)

        self.assertTrue(Path(f'{self.output_file}-heldout-head.fasta').exists(), f'File "{self.output_file}-heldout-head.fasta" was not created.')
        self.assertGreater(Path(f'{self.output_file}-heldout-head.fasta').stat().st_size, 0, f'File "{self.output_file}-heldout-head.fasta" was created but is empty.')

    def test_fasta_file_output_written_cv_fasta(self):
        cmd = [sys.executable, '-u', self.script_path, '-s', '0', '-f', 'fasta', '-o', self.output_file]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0)

        self.assertTrue(Path(f'{self.output_file}-cv-0-train-head.fasta').exists(), f'File "{self.output_file}-cv-0-train-head.fasta" was not created.')
        self.assertTrue(Path(f'{self.output_file}-cv-0-valid-head.fasta').exists(),
                        f'File "{self.output_file}-cv-0-valid-head.fasta" was not created.')
        self.assertGreater(Path(f'{self.output_file}-cv-0-train-head.fasta').stat().st_size, 0, f'File "{self.output_file}-cv-0-train-head.fasta" was created but is empty.')
        self.assertGreater(
            Path(f'{self.output_file}-cv-0-valid-head.fasta').stat().st_size, 0, f'File "{self.output_file}-cv-0-valid-head.fasta" was created but is empty.')

    def test_fasta_file_output_written_tv_tsv(self):
        cmd = [sys.executable, '-u', self.script_path, '-s', 'heldout', '-f', 'tsv', '-o', self.output_file]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0)

        self.assertTrue(Path(f'{self.output_file}-heldout-head.tsv').exists(), f'File "{self.output_file}-heldout-head.tsv" was not created.')
        self.assertGreater(Path(f'{self.output_file}-heldout-head.tsv').stat().st_size, 0, f'File "{self.output_file}-heldout-head.tsv" was created but is empty.')

    def test_fasta_file_output_written_cv_tsv(self):
        cmd = [sys.executable, '-u', self.script_path, '-s', '0', '-f', 'tsv', '-o', self.output_file]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0)

        self.assertTrue(Path(f'{self.output_file}-cv-0-train-head.tsv').exists(), f'File "{self.output_file}-cv-0-train-head.tsv" was not created.')
        self.assertTrue(Path(f'{self.output_file}-cv-0-valid-head.tsv').exists(),
                        f'File "{self.output_file}-cv-0-valid-head.tsv" was not created.')
        self.assertGreater(Path(f'{self.output_file}-cv-0-train-head.tsv').stat().st_size, 0, f'File "{self.output_file}-cv-0-train-head.tsv" was created but is empty.')
        self.assertGreater(
            Path(f'{self.output_file}-cv-0-valid-head.tsv').stat().st_size, 0, f'File "{self.output_file}-cv-0-valid-head.tsv" was created but is empty.')

    def test_fasta_file_output_written_tv_csv(self):
        cmd = [sys.executable, '-u', self.script_path, '-s', 'heldout', '-f', 'csv', '-o', self.output_file]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0)

        self.assertTrue(Path(f'{self.output_file}-heldout-head.csv').exists(), f'File "{self.output_file}-heldout-head.csv" was not created.')
        self.assertGreater(Path(f'{self.output_file}-heldout-head.csv').stat().st_size, 0, f'File "{self.output_file}-heldout-head.csv" was created but is empty.')

    def test_fasta_file_output_written_cv_csv(self):
        cmd = [sys.executable, '-u', self.script_path, '-s', '0', '-f', 'csv', '-o', self.output_file]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0)

        self.assertTrue(Path(f'{self.output_file}-cv-0-train-head.csv').exists(), f'File "{self.output_file}-cv-0-train-head.csv" was not created.')
        self.assertTrue(Path(f'{self.output_file}-cv-0-valid-head.csv').exists(),
                        f'File "{self.output_file}-cv-0-valid-head.csv" was not created.')
        self.assertGreater(Path(f'{self.output_file}-cv-0-train-head.csv').stat().st_size, 0, f'File "{self.output_file}-cv-0-train-head.csv" was created but is empty.')
        self.assertGreater(
            Path(f'{self.output_file}-cv-0-valid-head.csv').stat().st_size, 0, f'File "{self.output_file}-cv-0-valid-head.csv" was created but is empty.')

    def tearDown(self):
        directory = Path('.')
        patterns = [f'{self.output_file}-*', 'test-scldata-saving*']
        for file in chain(*(directory.glob(p) for p in patterns)):
            file.unlink(missing_ok=True)

if __name__ == '__main__':
    unittest.main()
