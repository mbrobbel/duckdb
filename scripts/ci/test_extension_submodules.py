#!/usr/bin/env python3
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

REPO_ROOT = Path(__file__).resolve().parents[2]


@unittest.skipUnless(shutil.which('cmake') and shutil.which('git'), 'requires CMake and Git')
class ExtensionSubmodulesTest(unittest.TestCase):
    def test_quoted_submodule_list_and_explicit_empty_list(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            env = os.environ.copy()
            env['GIT_ALLOW_PROTOCOL'] = 'file'
            for name in (
                'DUCKDB_SUBMODULE_BACKEND_DIRECTORY',
                'DUCKDB_SUBMODULE_LOADER_DIRECTORY',
                'DUCKDB_NEW_EXTENSION_BUILD',
            ):
                env.pop(name, None)

            def run(*args, cwd):
                result = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                return result.stdout.strip()

            def init(path):
                path.mkdir()
                run('git', 'init', cwd=path)
                run('git', 'config', 'user.name', 'Test', cwd=path)
                run('git', 'config', 'user.email', 'test@example.com', cwd=path)
                (path / 'CMakeLists.txt').write_text('# Extension fixture\n')
                run('git', 'add', '.', cwd=path)
                run('git', 'commit', '-m', 'Initial fixture', cwd=path)

            child = root / 'child'
            extension = root / 'extension'
            init(child)
            init(extension)
            names = ['duckdb', 'cucascade', 'substrait']
            for name in names:
                run('git', 'submodule', 'add', str(child), name, cwd=extension)
            run('git', 'commit', '-am', 'Add submodules', cwd=extension)
            revision = run('git', 'rev-parse', 'HEAD', cwd=extension)
            config = root / 'extension_config.cmake'
            config.write_text(
                f'duckdb_extension_load(submodule_backend GIT_URL "{extension.as_posix()}" '
                f'GIT_TAG {revision} SUBMODULES "duckdb;cucascade;substrait")\n'
                f'duckdb_extension_load(submodule_loader GIT_URL "{extension.as_posix()}" '
                f'GIT_TAG {revision} SUBMODULES "")\n'
            )
            build = root / 'build'
            run(
                'cmake',
                '-S',
                str(REPO_ROOT),
                '-B',
                str(build),
                '-DEXTENSION_CONFIG_BUILD=ON',
                '-DBUILD_SHELL=OFF',
                '-DBUILD_UNITTESTS=OFF',
                f'-DDUCKDB_EXTENSION_CONFIGS={config}',
                cwd=root,
            )
            for name in names:
                self.assertTrue(
                    (build / '_deps/submodule_backend_extension_fc-src' / name / 'CMakeLists.txt').is_file()
                )
                self.assertFalse((build / '_deps/submodule_loader_extension_fc-src' / name / 'CMakeLists.txt').exists())


if __name__ == '__main__':
    unittest.main()
