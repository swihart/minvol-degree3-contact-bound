#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import unittest
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
CERTIFIER = HERE / "certify_universal_bound.py"
AUDITOR = HERE / "audit_universal_bound.py"
CERT = HERE / "certificates" / "universal_contact_bound_certificate.json"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class UniversalContactBoundTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.c = load_module(CERTIFIER, "universal_contact_bound_certifier_test")
        cls.a = load_module(AUDITOR, "universal_contact_bound_auditor_test")
        cls.cert = json.loads(CERT.read_text())
        cls.rebuilt = cls.c.build_certificate(write=False)

    def test_certificate_claims(self) -> None:
        self.assertEqual(self.cert["schema"], "minvol.universal_contact_bound.v1")
        self.assertEqual(self.cert["lower_branch"]["weakest_row"], "O3B02B")
        self.assertEqual(
            self.cert["theorem"]["coefficient_of_pi"],
            "26221074253/200000000000",
        )
        self.assertTrue(self.cert["circumradius_partition"]["gap_free"])
        self.assertEqual(self.cert["lower_branch"]["replaced_reference_row"], "O3A1")
        self.assertEqual(self.cert["lower_branch"]["refined_angular_grid"]["cells"], 4)
        self.assertEqual(len(self.cert["near_Jung_branch"]["cap_pairs"]), 3)
        self.assertGreater(
            Fraction(self.cert["near_Jung_branch"]["volume_lower"]),
            Fraction(self.cert["theorem"]["coefficient_of_pi"])
            * Fraction(self.cert["pi_bounds"]["upper"]),
        )


    def test_standalone_public_paths(self) -> None:
        source = CERTIFIER.read_text()
        self.assertNotIn("o3b05-refined-angular-handoff", source)
        self.assertNotIn("o3b06-three-axis-cap-handoff", source)
        self.assertFalse(hasattr(self.c, "PARENT"))
        self.assertEqual(self.c.REFERENCE_CERT.parent, HERE / "certificates")
        self.assertEqual(self.c.REFERENCE_FAN.parent, HERE / "certificates")

    def test_reference_fan_fingerprint(self) -> None:
        reference = json.loads(self.c.REFERENCE_CERT.read_text())
        digest = hashlib.sha256(self.c.REFERENCE_FAN.read_bytes()).hexdigest()
        self.assertEqual(reference["near_jung_reference_fan"]["fan_sha256"], digest)
        self.assertEqual(digest, self.c.REFERENCE_FAN_SHA256)

    def test_exact_rebuild_is_byte_identical(self) -> None:
        blob = (json.dumps(self.rebuilt, indent=2, sort_keys=True) + "\n").encode("ascii")
        self.assertEqual(blob, CERT.read_bytes())

    def test_refined_o3a1_rows_are_gap_free_and_clear_theorem(self) -> None:
        rows = [
            row
            for row in self.cert["lower_branch"]["rows"]
            if row["case"].startswith("O3A1R")
        ]
        self.assertEqual(len(rows), 4)
        previous = Fraction(30_549, 50_000)
        target = Fraction(self.cert["theorem"]["coefficient_of_pi"])
        for row in rows:
            left, right = map(Fraction, row["interval"])
            self.assertEqual(left, previous)
            self.assertGreater(Fraction(row["coefficient_of_pi"]), target)
            self.assertEqual(row["angle_grid_N"], 76_800)
            self.assertEqual(row["radial_grid"], 40_000_000_000)
            previous = right
        self.assertEqual(previous, Fraction(6_113, 10_000))
        self.assertGreater(
            Fraction(self.cert["lower_branch"]["refined_angular_grid"]["minimum_margin_over_theorem"]),
            0,
        )

    def test_terminal_split_rows_are_gap_free_and_clear_theorem(self) -> None:
        rows = [row for row in self.cert["lower_branch"]["rows"] if row["case"] in {"O3B02A", "O3B02B"}]
        self.assertEqual([row["case"] for row in rows], ["O3B02A", "O3B02B"])
        target = Fraction(self.cert["theorem"]["coefficient_of_pi"])
        previous = Fraction(76_421_809, 125_000_000)
        for row in rows:
            left, right = map(Fraction, row["interval"])
            self.assertEqual(left, previous)
            self.assertGreater(Fraction(row["coefficient_of_pi"]), target)
            previous = right
        self.assertEqual(previous, self.c.R_SPLIT)
        self.assertEqual(self.cert["lower_branch"]["theorem_bottleneck"], "near_Jung_branch")

    def test_coordinate_width_sharpening(self) -> None:
        lemma = self.c.verify_coordinate_width_lemma()
        self.assertEqual(lemma["dominant_edge"], "e01")
        self.assertEqual(lemma["axis0_upper"], "H00 <= 1 + S/2")
        self.assertEqual(lemma["axis1_upper"], "H11 <= 1 + S/6")
        self.assertEqual(lemma["axis2_upper"], "H22 <= 1 + S/6")

        # Independent coefficient check for the two dominance decompositions.
        d1 = (-1, 1, -1, -1, 1, -1)
        d2 = (-1, -1, 1, 1, -1, -1)
        self.assertEqual(tuple(1 - 3 * c for c in d1), (4, -2, 4, 4, -2, 4))
        self.assertEqual(tuple(1 - 3 * c for c in d2), (4, 4, -2, -2, 4, 4))

        pairs = self.cert["near_Jung_branch"]["cap_pairs"]
        widths = [Fraction(pair["coordinate_width_lower"]) for pair in pairs]
        self.assertGreater(widths[0], Fraction(995, 1000))
        self.assertGreater(widths[1], widths[0])
        self.assertEqual(widths[1], widths[2])

    def test_fan_reconstruction_and_reference_regression(self) -> None:
        near = self.cert["near_Jung_branch"]
        fan = near["fan_reconstruction"]
        self.assertEqual(fan["vertices"], 98_306)
        self.assertEqual(fan["edges"], 294_912)
        self.assertEqual(fan["faces"], 196_608)
        self.assertEqual(fan["orbits"], 24_833)
        self.assertEqual(near["reference_margin_regression_index"], 19_510)
        self.assertEqual(near["changed_vertices_from_reference"], 18_229)
        self.assertGreater(Fraction(near["minimum_margin"]), Fraction(1, 10**12))

    def test_cap_allocations_and_cross_axis_disjointness(self) -> None:
        near = self.cert["near_Jung_branch"]
        for pair in near["cap_pairs"]:
            left, right = map(Fraction, pair["allocation_bracket"])
            self.assertLess(left, right)
            self.assertLess(Fraction(pair["derivative_left"]), 0)
            self.assertGreater(Fraction(pair["derivative_right"]), 0)
            self.assertGreater(Fraction(pair["pair_cap_lower"]), 0)
        self.assertGreater(Fraction(near["total_cap_lower"]), Fraction(14, 100_000))
        disjoint = near["cross_axis_disjointness"]
        self.assertGreater(Fraction(disjoint["strict_gap"]), Fraction(3, 5))
        self.assertGreater(
            Fraction(disjoint["overlap_norm_squared_lower"]),
            Fraction(disjoint["ellipsoid_radius_squared_upper"]),
        )

    def test_sharp_determinant_census(self) -> None:
        census = self.c.P.determinant_sharp_census()
        self.assertEqual(census["difference_quadratic_count"], 15)
        self.assertEqual(census["minimum_quadratic_pair_coefficient"], "1")
        self.assertEqual(census["negative_cubic_count"], 12)
        self.assertEqual(census["maximum_negative_cubic_pair_incidence"], 4)

    def test_binary64_audit(self) -> None:
        out = self.a.run_audit()
        self.assertEqual(out["refined_rows"], 4)
        self.assertGreater(out["minimum_refined_row_margin"], 1.0e-5)
        self.assertEqual(out["fan_vertices"], 98_306)
        self.assertEqual(out["changed_vertices"], 18_229)
        self.assertGreater(out["minimum_fan_margin"], 2.8e-10)
        self.assertGreater(out["axis0_coordinate_width"], 0.995)
        self.assertGreater(out["axis1_coordinate_width"], out["axis0_coordinate_width"])
        self.assertGreater(out["total_cap_lower"], 1.4e-4)
        self.assertGreater(out["cross_axis_gap"], 0.6)
        self.assertGreater(out["near_jung_lower"], out["universal_coefficient"])
        self.assertGreater(out["gain_over_previous"], 2.0e-6)


if __name__ == "__main__":
    unittest.main(verbosity=2)
