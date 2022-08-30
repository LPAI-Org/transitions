import unittest
import pycodestyle
from os.path import exists

try:
    import mypy
except ImportError:
    mypy = None  # type: ignore


class TestCodeFormat(unittest.TestCase):
    def test_conformance(self):
        """Test that we conform to PEP-8."""
        style = pycodestyle.StyleGuide(quiet=False, ignore=['E501', 'W605'])
        if exists('transitions'):  # when run from root directory (e.g. tox)
            style.input_dir('transitions')
            style.input_dir('tests')
        else:  # when run from test directory (e.g. pycharm)
            style.input_dir('../transitions')
            style.input_dir('.')
        result = style.check_files()
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    @unittest.skipIf(mypy is None, "mypy not found")
    def test_mypy(self):
        import subprocess
        call = ['mypy', '--config-file', 'mypy.ini', 'transitions']

        # when run from root directory (e.g. tox) else when run from test directory (e.g. pycharm)
        project_root = '.' if exists('transitions') else '..'
        subprocess.check_call(call, cwd=project_root)
