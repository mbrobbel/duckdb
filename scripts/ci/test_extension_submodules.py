#!/usr/bin/env python3
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

REPO_ROOT = Path(__file__).resolve().parents[2]


@unittest.skipUnless(shutil.which('cmake'), 'requires CMake')
class ExtensionSubmodulesTest(unittest.TestCase):
    def test_quoted_submodule_list_and_explicit_empty_list(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = root / 'extensions.cmake'
            config.write_text('''
# Record the SUBMODULES argument instead of fetching a repository.
function(register_external_extension)
    file(WRITE "${CMAKE_BINARY_DIR}/${ARGV0}.submodules" "${ARGV10}")
endfunction()
duckdb_extension_load(example_list GIT_URL unused GIT_TAG unused SUBMODULES "first;second")
duckdb_extension_load(example_empty GIT_URL unused GIT_TAG unused SUBMODULES "")
''')
            result = subprocess.run(
                [
                    'cmake',
                    '-S',
                    str(REPO_ROOT),
                    '-B',
                    str(root / 'build'),
                    '-DEXTENSION_CONFIG_BUILD=ON',
                    f'-DDUCKDB_EXTENSION_CONFIGS={config}',
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual((root / 'build/example_list.submodules').read_text(), 'first;second')
            self.assertEqual((root / 'build/example_empty.submodules').read_text(), '')


if __name__ == '__main__':
    unittest.main()
