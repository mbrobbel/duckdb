#!/usr/bin/env python3

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'merge_vcpkg_deps.py'


class MergeVcpkgOverridesTest(unittest.TestCase):
    def merge(self, overrides, *, openssl_version=None, conflict=None):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / 'build/extension_configuration/vcpkg.json'
            output.parent.mkdir(parents=True)
            manifests = []
            for index, entries in enumerate(overrides):
                manifest = root / f'extension{index}.json'
                manifest.write_text(json.dumps({'dependencies': ['example'], 'overrides': entries}))
                manifests.append(str(manifest))
            env = os.environ.copy()
            env.pop('OPENSSL_VERSION_OVERRIDE', None)
            if openssl_version is not None:
                env['OPENSSL_VERSION_OVERRIDE'] = openssl_version
            result = subprocess.run(
                [sys.executable, str(SCRIPT), *manifests], cwd=root, env=env, capture_output=True, text=True
            )
            if conflict:
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(f"Conflicting vcpkg overrides for '{conflict}'", result.stderr)
                for manifest in manifests:
                    self.assertIn(manifest, result.stderr)
                self.assertFalse(output.exists())
                return
            self.assertEqual(result.returncode, 0, result.stderr)
            return json.loads(output.read_text())['overrides']

    def test_preserves_extension_pins_and_port_revisions(self):
        dlpack = {'name': 'dlpack', 'version': '0.8'}
        flatbuffers = {'name': 'flatbuffers', 'version': '24.3.25', 'port-version': 1}
        self.assertEqual(
            self.merge([[flatbuffers], [dlpack]]),
            [{'name': 'openssl', 'version': '3.6.0'}, dlpack, flatbuffers],
        )

    def test_deduplicates_identical_overrides(self):
        pin = {'name': 'dlpack', 'version': '0.8'}
        self.assertEqual(
            self.merge([[pin], [dict(pin, **{'port-version': 0, '$comment': 'same version'})]]),
            [{'name': 'openssl', 'version': '3.6.0'}, pin],
        )

    def test_rejects_conflicting_versions_and_port_revisions(self):
        first = {'name': 'flatbuffers', 'version': '24.3.25'}
        for second in [dict(first, version='25.12.19'), dict(first, **{'port-version': 1})]:
            with self.subTest(second=second):
                self.merge([[first], [second]], conflict='flatbuffers')

    def test_preserves_other_version_schemes(self):
        pins = [
            {'name': 'a', 'version-semver': '1.2.3'},
            {'name': 'b', 'version-date': '2026-01-01'},
            {'name': 'c', 'version-string': 'release'},
        ]
        self.assertEqual(self.merge([pins])[1:], pins)

    def test_keeps_central_openssl_policy(self):
        pins = [[{'name': 'openssl', 'version': '1.0.0'}], [{'name': 'openssl', 'version': '2.0.0'}]]
        self.assertEqual(self.merge(pins), [{'name': 'openssl', 'version': '3.6.0'}])
        self.assertEqual(self.merge(pins, openssl_version='3.6.1'), [{'name': 'openssl', 'version': '3.6.1'}])

    def test_no_extension_overrides_keeps_existing_output(self):
        self.assertEqual(self.merge([[]]), [{'name': 'openssl', 'version': '3.6.0'}])


if __name__ == '__main__':
    unittest.main()
