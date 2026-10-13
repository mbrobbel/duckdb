#!/usr/bin/env python3

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'merge_vcpkg_deps.py'


class MergeVcpkgDependenciesTest(unittest.TestCase):
    def test_merges_overlays_from_both_configuration_spellings(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / 'build' / 'extension_configuration' / 'vcpkg.json'
            output.parent.mkdir(parents=True)
            manifests = []
            expected_ports = []
            expected_triplets = []
            for name, key in [('legacy', 'vcpkg-configuration'), ('current', 'configuration')]:
                extension = root / name / 'wrapper'
                extension.mkdir(parents=True)
                manifest = extension / 'vcpkg.json'
                manifest.write_text(
                    json.dumps(
                        {
                            'dependencies': [name],
                            key: {'overlay-ports': ['ports'], 'overlay-triplets': ['triplets']},
                        }
                    )
                )
                manifests.append(str(manifest))
                expected_ports.append(str(extension / 'ports'))
                expected_triplets.append(str(extension / 'triplets'))

            subprocess.run([sys.executable, str(SCRIPT), *manifests], cwd=root, check=True)
            merged = json.loads(output.read_text())
            self.assertEqual(merged['dependencies'], ['legacy', 'current'])
            self.assertEqual(merged['vcpkg-configuration']['overlay-ports'], expected_ports)
            self.assertEqual(merged['vcpkg-configuration']['overlay-triplets'], expected_triplets)


if __name__ == '__main__':
    unittest.main()
