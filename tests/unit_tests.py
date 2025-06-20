import os
import subprocess
import sys
from contextlib import redirect_stdout
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from scldata.loader import load
from scldata.__init__ import main

class TestScldataPkg(unittest.TestCase):

    def test_import_package(self):
        import scldata
        self.assertTrue(hasattr(scldata, '__version__'))

    def test_import_submodule_load(self):
        from scldata import loader
        self.assertTrue(callable(getattr(loader, 'load', None)))

    def test_import_submodule_main(self):
        from scldata import __init__
        self.assertTrue(callable(getattr(__init__, 'main', None)))

    def test_load_kfold_input(self):
        self.assertRaises(ValueError, load, 5)
        self.assertRaises(ValueError, load, -5)

    def test_kfold_output_is_train_test(self):
        train_test = load('0')
        self.assertEqual(len(train_test), 2, 'Fold loading not returning train and test sets')

    def test_main_returns_none(self):
        from scldata.__init__ import  main
        self.assertIsNone(main(), 'Main function should return None')

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
        script_path = self.project_root / 'scldata' / '__init__.py'
        result = subprocess.run(
            [sys.executable, script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        self.assertEqual(result.returncode, 0, 'The script returned exit code 1, all was not ok')
        self.assertIn('SCL2205 Full (Head):', result.stdout, 'The SCL2205 Full head output should be printed when "scldata" command (script) is run without any arguments')

    @patch('sys.argv', ['myscript.py', '--split', 'test'])
    def test_invalid_option_arg(self):
        with self.assertRaises(SystemExit):
            main()

if __name__ == '__main__':
    unittest.main()
