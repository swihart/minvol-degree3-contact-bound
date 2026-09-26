#!/usr/bin/env python3
"""Independent binary64 audit of the terminal-handoff v1.1 candidate."""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CERT = json.loads((ROOT / "certificates/terminal_handoff_v11_certificate.json").read_text())
EXP = json.loads((ROOT / "certificates/terminal_handoff_v11_exploration.json").read_text())


def read_constants() -> dict[str, float]:
    out: dict[str, float] = {}
    with (ROOT / "certificates/audit_constants.csv").open(newline="") as f:
        for row in csv.DictReader(f):
            out[row["name"]] = float(row["value"])
    return out


def main() -> int:
    c = read_constants()
    old = c["old_v1_volume"]
    candidate_lo = c["candidate_v11_volume_lower"]
    candidate_hi = c["candidate_v11_volume_upper"]
    near = c["near_jung_volume_lower"]
    split = c["split_terminal_min_volume_lower"]

    assert math.isfinite(old + candidate_lo + candidate_hi + near + split)
    assert candidate_lo > old
    assert candidate_hi < near
    assert near < split
    assert c["gain_over_v1"] > 2.1074e-6
    assert 2.5e-12 < c["near_margin"] < 2.6e-12
    assert c["split_margin"] > 6.3e-7

    theorem = CERT["candidate_theorem"]
    assert abs(float(theorem["decimal_lower"]) - candidate_lo) < 5e-16
    assert CERT["terminal_split"]["rows"][0]["positive_steps"] == 6308
    assert CERT["terminal_split"]["rows"][1]["negative_steps"] == 18566

    assert EXP["conclusion"]["exact_improvement_found"] is True
    assert EXP["conclusion"]["two_way_split_is_sufficient"] is True
    assert EXP["conclusion"]["tested_left_shifts_strictly_lower_the_universal_minimum"] is True
    left = EXP["leftward_R_star_perturbations"]["samples"]
    near_values = [float(x["near_Jung_volume_lower"]) for x in left]
    assert all(near_values[i + 1] < near_values[i] for i in range(len(near_values) - 1))
    assert float(EXP["doubled_angular_resolution"]["unsplit_volume_lower"]) > old
    assert float(EXP["doubled_angular_resolution"]["unsplit_volume_lower"]) < near

    print(f"v1.0.0 lower:             {old:.16f}")
    print(f"v1.1 candidate lower:     {candidate_lo:.16f}")
    print(f"unchanged near-Jung lower:{near:.16f}")
    print(f"split terminal minimum:   {split:.16f}")
    print(f"gain over v1.0.0:         {candidate_lo-old:.16e}")
    print(f"near-Jung safety margin:  {near-candidate_hi:.16e}")
    print("MINVOL TERMINAL-HANDOFF V1.1 BINARY64 AUDIT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
