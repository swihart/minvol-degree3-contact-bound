#!/usr/bin/env python3
"""Adversarial rejection tests for the standalone exact certificate.

Each test mutates a temporary copy of one theorem-critical object.  Repository
files are never rewritten.  The suite exercises production verification helpers
and confirms that every requested corruption class is rejected.
"""
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable

import numpy as np

HERE = Path(__file__).resolve().parent
CERTIFIER = HERE / "certify_universal_bound.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def read_npz(path: Path) -> dict[str, np.ndarray]:
    with np.load(path, allow_pickle=False) as data:
        return {key: np.asarray(data[key]).copy() for key in data.files}


def write_npz(path: Path, payload: dict[str, np.ndarray]) -> None:
    np.savez(path, **payload)


class AdversarialMutationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.c = load_module(CERTIFIER, "universal_contact_bound_mutation_certifier")
        cls.canonical_certificate = cls.c.CERT_PATH.read_bytes()
        cls.canonical_hulls = cls.c.HULL_AUDIT.read_bytes()

    def temporary_path(self, name: str):
        directory = tempfile.TemporaryDirectory(prefix="minvol-mutation-")
        self.addCleanup(directory.cleanup)
        return Path(directory.name) / name

    def write_mutated_certificate(self, mutate: Callable[[dict[str, Any]], None]) -> Path:
        document = json.loads(self.c.CERT_PATH.read_text())
        mutate(document)
        path = self.temporary_path("universal_contact_bound_certificate.json")
        path.write_bytes((json.dumps(document, indent=2, sort_keys=True) + "\n").encode("ascii"))
        return path

    def test_rejects_lower_row_endpoint_mutation(self) -> None:
        payload = read_npz(self.c.ROW_FILES[0])
        payload["rhi_num"] = payload["rhi_num"] + np.int64(1)
        path = self.temporary_path("refined_lower_cell_1.npz")
        write_npz(path, payload)

        with self.assertRaisesRegex(AssertionError, "interval or tangency mismatch"):
            self.c.replay_refined_row(path, self.c.ROW_EXPECTED[0])

    def test_rejects_fan_radial_numerator_mutation(self) -> None:
        payload = read_npz(self.c.FAN_DATA)
        radial = payload["Aint"].copy()
        radial[1] -= 1
        payload["Aint"] = radial
        path = self.temporary_path("universal_contact_fan_radial_mutation.npz")
        write_npz(path, payload)

        with self.assertRaisesRegex(AssertionError, "edge-stabilizer invariant"):
            self.c.verify_fan_input_structure(self.c.REFERENCE_FAN, path)

    def test_rejects_s_procedure_multiplier_mutation(self) -> None:
        payload = read_npz(self.c.FAN_DATA)
        delta = payload["delta_num"].copy()
        delta[1] += 1
        payload["delta_num"] = delta
        path = self.temporary_path("universal_contact_fan_multiplier_mutation.npz")
        write_npz(path, payload)

        with self.assertRaisesRegex(AssertionError, "inherited S-procedure multipliers"):
            self.c.verify_fan_input_structure(self.c.REFERENCE_FAN, path)

    def test_rejects_section_hull_vertex_mutation(self) -> None:
        lines = self.canonical_hulls.decode("ascii").splitlines()
        fields = lines[1].split("\t")
        fields[3] = str(int(fields[3]) + 1)
        lines[1] = "\t".join(fields)
        path = self.temporary_path("all_axis_pair_section_hulls.tsv")
        path.write_text("\n".join(lines) + "\n", encoding="ascii")

        with self.assertRaisesRegex(RuntimeError, "section hull audit"):
            self.c.require_byte_identical(
                path,
                self.canonical_hulls,
                "all-axis section hull audit is not byte-identical",
            )

    def test_rejects_cap_allocation_bracket_mutation(self) -> None:
        def mutate(document: dict[str, Any]) -> None:
            bracket = document["near_Jung_branch"]["cap_pairs"][0]["allocation_bracket"]
            bracket[0] = bracket[1]

        path = self.write_mutated_certificate(mutate)
        mutated = json.loads(path.read_text())
        left, right = map(
            Fraction,
            mutated["near_Jung_branch"]["cap_pairs"][0]["allocation_bracket"],
        )
        self.assertFalse(left < right)

        with self.assertRaisesRegex(RuntimeError, "certificate JSON"):
            self.c.require_byte_identical(
                path,
                self.canonical_certificate,
                "certificate JSON is not byte-identical",
            )

    def test_rejects_disjointness_threshold_mutation(self) -> None:
        def mutate(document: dict[str, Any]) -> None:
            disjoint = document["near_Jung_branch"]["cross_axis_disjointness"]
            disjoint["ellipsoid_radius_squared_upper"] = disjoint[
                "overlap_norm_squared_lower"
            ]

        path = self.write_mutated_certificate(mutate)
        mutated = json.loads(path.read_text())
        disjoint = mutated["near_Jung_branch"]["cross_axis_disjointness"]
        self.assertFalse(
            Fraction(disjoint["overlap_norm_squared_lower"])
            > Fraction(disjoint["ellipsoid_radius_squared_upper"])
        )

        with self.assertRaisesRegex(RuntimeError, "certificate JSON"):
            self.c.require_byte_identical(
                path,
                self.canonical_certificate,
                "certificate JSON is not byte-identical",
            )

    def test_rejects_theorem_coefficient_digit_mutation(self) -> None:
        def mutate(document: dict[str, Any]) -> None:
            value = Fraction(document["theorem"]["coefficient_of_pi"])
            document["theorem"]["coefficient_of_pi"] = (
                f"{value.numerator + 1}/{value.denominator}"
            )

        path = self.write_mutated_certificate(mutate)
        mutated = json.loads(path.read_text())
        self.assertNotEqual(
            mutated["theorem"]["coefficient_of_pi"],
            "26220940089713/200000000000000",
        )

        with self.assertRaisesRegex(RuntimeError, "certificate JSON"):
            self.c.require_byte_identical(
                path,
                self.canonical_certificate,
                "certificate JSON is not byte-identical",
            )


if __name__ == "__main__":
    program = unittest.main(verbosity=2, exit=False)
    if not program.result.wasSuccessful():
        raise SystemExit("adversarial mutation suite failed")
    print("MINVOL ADVERSARIAL MUTATION SUITE: PASS")
