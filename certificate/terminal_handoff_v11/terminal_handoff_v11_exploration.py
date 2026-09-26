#!/usr/bin/env python3
"""Replay the bounded terminal-handoff parameter audit.

The exact terminal-row searches were archived in
certificates/bounded_exploration_exact_rows.json.  This verifier checks their
rational ordering and independently recomputes the unchanged near-Jung branch,
its fan margin, and the five requested left-shift samples from the public v1.0.0
proof objects.

The theorem-bearing two-way split is regenerated from first principles by
terminal_handoff_v11_exact.py; the 3/4-way and doubled-grid rows are diagnostic
search records only.
"""
from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

PACKAGE_ROOT = Path(__file__).resolve().parent
CERT_DIR = PACKAGE_ROOT / "certificates"
REFERENCE_DIR = PACKAGE_ROOT / "reference"
sys.path.insert(0, str(PACKAGE_ROOT))

import terminal_handoff_v11_exact as E  # noqa: E402

P = E.P
REFERENCE_CERT = json.loads((REFERENCE_DIR / "universal_contact_bound_certificate.json").read_text())
FAN = np.load(REFERENCE_DIR / "universal_contact_fan.npz", allow_pickle=False)
RADIALS = np.asarray(FAN["Aint"], dtype=np.int64)
DELTAS = np.asarray(FAN["delta_num"], dtype=np.int64)
FAN_TARGET = Fraction(1, 10**12)


def affine_margin_data(q: tuple[int, int, int], radial: int, delta: int) -> tuple[Fraction, Fraction] | None:
    beta = P.beta_numerators(q, radial)
    negative = [x < 0 for x in beta]
    nneg = sum(negative)
    if nneg == 0:
        return None
    mu = [0 if negative[k] else beta[k] + (delta if nneg == 2 else 0) for k in range(4)]
    total = sum(mu)
    rem = total - P.BETA_DEN
    if rem <= 0:
        raise AssertionError("invalid affine remainder")
    z = [beta[k] - mu[k] for k in range(4)]
    c = []
    for i, j in P.PAIRS:
        c.append(
            -Fraction(2 * beta[i] * beta[j], P.BETA_DEN * P.BETA_DEN)
            - Fraction(2 * z[i] * z[j], P.BETA_DEN * rem)
        )
    regular = Fraction(1) - Fraction(total, P.BETA_DEN) - sum(c, Fraction(0)) / 2
    edge = min(Fraction(0), min(c))
    dominant = P.dominant_lower(c, Fraction(1))
    return regular, max(edge, dominant) / 2


class NearJungEvaluator:
    def __init__(self) -> None:
        self.qvec, _faces, _edges, self.index = P.reconstruct_cube_fan()
        self.orbits = P.stabilizer_orbits(self.qvec, self.index)
        self.affine: list[tuple[int, Fraction, Fraction]] = []
        for orbit in self.orbits:
            i = orbit[0]
            data = affine_margin_data(self.qvec[i], int(RADIALS[i]), int(DELTAS[i]))
            if data is not None:
                self.affine.append((i, data[0], data[1]))

        near = REFERENCE_CERT["near_Jung_branch"]
        self.reference_fan_coefficient = Fraction(near["reference_fan_coefficient"])
        self.supports: dict[tuple[int, int], Fraction] = {}
        self.areas: dict[tuple[int, int], Fraction] = {}
        for pair in near["cap_pairs"]:
            axis = int(pair["axis"])
            self.supports[(axis, 1)] = Fraction(pair["support_plus"])
            self.supports[(axis, -1)] = Fraction(pair["support_minus"])
            self.areas[(axis, 1)] = Fraction(pair["section_area_plus"])
            self.areas[(axis, -1)] = Fraction(pair["section_area_minus"])
        self.sqrt2 = P.sqrt_lower(Fraction(2))

    @staticmethod
    def deficiency(R: Fraction) -> Fraction:
        q = R * R
        return (3 - 8 * q) / (4 * q - 1)

    def minimum_margin(self, R: Fraction) -> tuple[Fraction, int]:
        deficiency = self.deficiency(R)
        best: Fraction | None = None
        index = -1
        for i, regular, slope in self.affine:
            margin = regular + slope * deficiency
            if best is None or margin < best:
                best = margin
                index = i
        if best is None:
            raise AssertionError("empty affine margin list")
        return best, index

    def fan_deficiency_limit(self) -> tuple[Fraction, int]:
        limit: Fraction | None = None
        index = -1
        for i, regular, slope in self.affine:
            if slope < 0:
                candidate = (regular - FAN_TARGET) / (-slope)
                if limit is None or candidate < limit:
                    limit = candidate
                    index = i
            elif regular <= FAN_TARGET:
                raise AssertionError("nondecreasing margin already below target")
        if limit is None:
            raise AssertionError("no fan deficiency limit")
        return limit, index

    def evaluate(self, R: Fraction) -> dict[str, Fraction | int]:
        q = R * R
        deficiency = self.deficiency(R)
        margin, margin_index = self.minimum_margin(R)
        if margin <= FAN_TARGET:
            raise AssertionError("unchanged fan no longer clears exact margin target")

        det_sq = 1 - deficiency / 2 - deficiency * deficiency / 2
        det_lo = P.sqrt_lower(det_sq)
        core = self.reference_fan_coefficient * P.sqrt_lower(det_sq / 2)
        width_sq = {0: 1 / (1 + deficiency / 2), 1: 1 / (1 + deficiency / 6), 2: 1 / (1 + deficiency / 6)}
        widths = {axis: P.sqrt_lower(width_sq[axis]) for axis in range(3)}
        cap_total = Fraction(0)
        for axis in range(3):
            sp = self.supports[(axis, 1)]
            sm = self.supports[(axis, -1)]
            excess = widths[axis] - (sp + sm) / (2 * self.sqrt2)
            dp = (sp - P.BASES[(axis, 1)]) / (2 * self.sqrt2)
            dm = (sm - P.BASES[(axis, -1)]) / (2 * self.sqrt2)
            allocation = P.allocation_certificate(
                self.areas[(axis, 1)], dp, self.areas[(axis, -1)], dm, excess, det_lo
            )
            cap_total += allocation["lower"]

        center = 3 - 8 * q
        min_support = min(self.supports.values())
        cross_gap = 2 * (min_support - center) ** 2 - Fraction(3, 1 - deficiency)
        if cross_gap <= 0:
            raise AssertionError("cross-axis cap separation fails")

        return {
            "R": R,
            "deficiency": deficiency,
            "fan_margin": margin,
            "fan_margin_index": margin_index,
            "core": core,
            "caps": cap_total,
            "near": core + cap_total,
            "cross_gap": cross_gap,
        }


def canonical(data: dict[str, Any]) -> bytes:
    return (json.dumps(data, indent=2, sort_keys=True) + "\n").encode("utf-8")


def build_results() -> dict[str, Any]:
    archive = json.loads((CERT_DIR / "bounded_exploration_exact_rows.json").read_text())
    pi_lo, _pi_hi = P.pi_bounds()
    near_eval = NearJungEvaluator()

    current = near_eval.evaluate(E.O3B02_RIGHT)
    reference_near = Fraction(REFERENCE_CERT["near_Jung_branch"]["volume_lower"])
    if current["near"] != reference_near:
        raise AssertionError("near-Jung evaluator does not reproduce public v1.0.0")
    if current["fan_margin"] != Fraction(REFERENCE_CERT["near_Jung_branch"]["minimum_margin"]):
        raise AssertionError("fan-margin replay mismatch")

    old_volume = E.OLD_PI_COEFFICIENT * pi_lo
    local = archive["local_s0_retune"]
    local_volume = Fraction(local["coefficient_of_pi"]) * pi_lo
    if not old_volume < local_volume < reference_near:
        raise AssertionError("unexpected local s0 ordering")

    split_summary: dict[str, Any] = {}
    for parts in ("2", "3", "4"):
        block = archive["splits"][parts]
        row_coeffs = [Fraction(row["coefficient_of_pi"]) for row in block["rows"]]
        minimum = min(row_coeffs)
        if minimum != Fraction(block["minimum_coefficient_of_pi"]):
            raise AssertionError(f"{parts}-way split minimum mismatch")
        minimum_volume = minimum * pi_lo
        if minimum_volume <= reference_near:
            raise AssertionError(f"{parts}-way split did not clear near-Jung branch")
        split_summary[parts] = {
            "minimum_coefficient_of_pi": str(minimum),
            "minimum_volume_lower": E.decimal_string(minimum_volume, 50),
            "margin_over_near_Jung": E.decimal_string(minimum_volume - reference_near, 50),
        }

    doubled = archive["doubled_angular_resolution"]
    doubled_unsplit = Fraction(doubled["unsplit"]["coefficient_of_pi"]) * pi_lo
    doubled_split = Fraction(doubled["split2_minimum_coefficient_of_pi"]) * pi_lo
    if not old_volume < doubled_unsplit < reference_near:
        raise AssertionError("doubled unsplit ordering mismatch")
    if doubled_split <= reference_near:
        raise AssertionError("doubled split should clear near-Jung branch")

    left_samples = []
    previous_near: Fraction | None = None
    for sample in archive["left_shifts"]["samples"]:
        shift = Fraction(sample["shift"])
        R = Fraction(sample["R"])
        if R != E.O3B02_RIGHT - shift:
            raise AssertionError("left-shift R mismatch")
        near = near_eval.evaluate(R)
        lower = Fraction(sample["split_min_coefficient_of_pi"]) * pi_lo
        if lower <= near["near"]:
            raise AssertionError("retuned split lower unexpectedly bottlenecks after left shift")
        if previous_near is not None and near["near"] >= previous_near:
            raise AssertionError("near-Jung lower did not strictly decrease under left shift")
        previous_near = near["near"]
        left_samples.append(
            {
                "shift": str(shift),
                "R": str(R),
                "locally_retuned_s0": sample["s0"],
                "split_terminal_min_coefficient_of_pi": sample["split_min_coefficient_of_pi"],
                "split_terminal_min_volume_lower": E.decimal_string(lower, 50),
                "near_Jung_volume_lower": E.decimal_string(near["near"], 50),
                "fan_margin": str(near["fan_margin"]),
                "fan_margin_decimal": E.decimal_string(near["fan_margin"], 30),
                "universal_minimum": E.decimal_string(min(lower, near["near"]), 50),
            }
        )

    fan_limit, fan_limit_index = near_eval.fan_deficiency_limit()
    q_limit = (3 + fan_limit) / (8 + 4 * fan_limit)
    getcontext().prec = 70
    r_limit = (Decimal(q_limit.numerator) / Decimal(q_limit.denominator)).sqrt()
    current_r = Decimal(E.O3B02_RIGHT.numerator) / Decimal(E.O3B02_RIGHT.denominator)

    return {
        "schema": "minvol-terminal-handoff-bounded-exploration-replay-v1",
        "scope": "parameter optimization only; theorem architecture unchanged",
        "exact_search_archive_sha256": E.sha256(CERT_DIR / "bounded_exploration_exact_rows.json"),
        "baseline": {
            "v1_volume_lower": E.decimal_string(old_volume, 50),
            "R_star": str(E.O3B02_RIGHT),
            "near_Jung_volume_lower": E.decimal_string(reference_near, 50),
        },
        "local_s0_retune": {
            "s0": local["s0"],
            "coefficient_of_pi": local["coefficient_of_pi"],
            "volume_lower": E.decimal_string(local_volume, 50),
            "gain_over_v1": E.decimal_string(local_volume - old_volume, 50),
        },
        "splits": split_summary,
        "doubled_angular_resolution": {
            "unsplit_volume_lower": E.decimal_string(doubled_unsplit, 50),
            "unsplit_gain_over_v1": E.decimal_string(doubled_unsplit - old_volume, 50),
            "split_minimum_volume_lower": E.decimal_string(doubled_split, 50),
            "split_margin_over_near_Jung": E.decimal_string(doubled_split - reference_near, 50),
        },
        "leftward_R_star_perturbations": {
            "samples": left_samples,
            "fan_deficiency_limit": str(fan_limit),
            "fan_limit_active_index": fan_limit_index,
            "approximate_smallest_R_allowed_by_unchanged_fan": format(r_limit, ".45f"),
            "approximate_maximum_left_shift": format(current_r - r_limit, ".45e"),
        },
        "conclusion": {
            "exact_improvement_found": True,
            "two_way_split_is_sufficient": True,
            "best_bounded_branch_value": E.decimal_string(reference_near, 50),
            "three_or_four_splits_do_not_raise_the_universal_minimum": True,
            "doubled_grid_does_not_raise_the_universal_minimum_after_split": True,
            "tested_left_shifts_strictly_lower_the_universal_minimum": True,
            "larger_left_shifts_require_new_fan data and are outside scope": True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = build_results()
    path = CERT_DIR / "terminal_handoff_v11_exploration.json"
    encoded = canonical(result)
    if args.write:
        path.write_bytes(encoded)
    elif path.read_bytes() != encoded:
        raise AssertionError("exploration report is stale or manually divergent")

    print("2-way split minimum:", result["splits"]["2"]["minimum_volume_lower"])
    print("Current near-Jung lower:", result["baseline"]["near_Jung_volume_lower"])
    print("Doubled unsplit:", result["doubled_angular_resolution"]["unsplit_volume_lower"])
    print("Maximum unchanged-fan left shift:", result["leftward_R_star_perturbations"]["approximate_maximum_left_shift"])
    print("MINVOL TERMINAL-HANDOFF BOUNDED EXPLORATION: EXACT REPLAY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
