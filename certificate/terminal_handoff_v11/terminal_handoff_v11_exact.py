#!/usr/bin/env python3
"""Exact bounded terminal-handoff audit for the public MinVol v1.0.0 certificate.

This script does not redesign the theorem.  It replaces the terminal O3B02
radial row by two exact subrows, keeps every earlier lower-branch row and the
near-Jung certificate unchanged, and proves a slightly larger presentable
universal coefficient.

Floating point is used only to propose neighboring radial-grid integers during
row generation.  Every accepted step, extremal grid choice, cap-disjointness
condition, tangent-gap sum, theorem comparison, and pi comparison is replayed
with Python integers and fractions.Fraction.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

PACKAGE_ROOT = Path(__file__).resolve().parent
REFERENCE_DIR = PACKAGE_ROOT / "reference"
CERT_DIR = PACKAGE_ROOT / "certificates"

ANGLE_N = 38_400
RADIAL_G = 10**9
ROUND_DELTA = 10**18
ROUND_COEFFICIENT = 10**15

O3B02_LEFT = Fraction(76_421_809, 125_000_000)
O3B02_MID = Fraction(611_382_837, 1_000_000_000)
O3B02_RIGHT = Fraction(305_695_601, 500_000_000)

CELL_SPECS = (
    {
        "case": "O3B02A",
        "rlo": O3B02_LEFT,
        "rhi": O3B02_MID,
        "s0": Fraction(12_450_083, 25_000_000),
        "expected_coefficient": Fraction(131_107_875_849_897, 10**15),
        "expected_positive_steps": 6_308,
        "expected_negative_steps": 18_564,
    },
    {
        "case": "O3B02B",
        "rlo": O3B02_MID,
        "rhi": O3B02_RIGHT,
        "s0": Fraction(49_802_043, 100_000_000),
        "expected_coefficient": Fraction(131_105_572_993_743, 10**15),
        "expected_positive_steps": 6_307,
        "expected_negative_steps": 18_566,
    },
)

# A readable coefficient with a conservative exact margin beneath the unchanged
# near-Jung rational lower bound.  It reduces to 26221074253/200000000000.
CANDIDATE_PI_COEFFICIENT = Fraction(131_105_371_265, 10**12)
OLD_PI_COEFFICIENT = Fraction(26_220_940_089_713, 200_000_000_000_000)


def load_exact_geometry() -> Any:
    path = REFERENCE_DIR / "exact_geometry.py"
    spec = importlib.util.spec_from_file_location("minvol_v11_exact_geometry", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


P = load_exact_geometry()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def frac(value: str | int | Fraction) -> Fraction:
    return value if isinstance(value, Fraction) else Fraction(value)


def decimal_string(value: Fraction, digits: int = 60) -> str:
    getcontext().prec = digits + 20
    d = Decimal(value.numerator) / Decimal(value.denominator)
    return format(d, f".{digits}f")


def floor_grid(value: Fraction, denominator: int) -> Fraction:
    return Fraction((value.numerator * denominator) // value.denominator, denominator)


def angle(k: int, n: int) -> tuple[Fraction, Fraction]:
    return Fraction(n * n - k * k, n * n + k * k), Fraction(2 * k * n, n * n + k * k)


def delta_angle(k: int, n: int) -> tuple[Fraction, Fraction]:
    c, s = angle(k, n)
    c0, s0 = angle(k - 1, n)
    return c * c0 + s * s0, s * c0 - c * s0


def step_ok_num(xn: int, yn: int, m: Fraction, k: int, n: int, g: int) -> bool:
    x = Fraction(xn, g)
    y = Fraction(yn, g)
    cd, sd = delta_angle(k, n)
    t = x * x + m
    disc = 4 * x * x - t * t
    return (
        disc >= 0
        and t * (y * cd - x) > 0
        and y * y * disc * sd * sd <= t * t * (y * cd - x) ** 2
    )


def next_w_num(yn: int, m: Fraction, k: int, n: int, g: int, s0_floor: int) -> int:
    """Return the largest radial-grid integer x<y satisfying the exact step test."""
    y = yn / g
    t = k / n
    t0 = (k - 1) / n
    c = (1 - t * t) / (1 + t * t)
    s = 2 * t / (1 + t * t)
    c0 = (1 - t0 * t0) / (1 + t0 * t0)
    s0 = 2 * t0 / (1 + t0 * t0)
    cd = c * c0 + s * s0
    sd = s * c0 - c * s0
    mf = float(m)

    lo = max((s0_floor + 1) / g, y - 0.001)
    hi = y - 1 / g

    def valid_float(x: float) -> bool:
        tt = x * x + mf
        disc = 4 * x * x - tt * tt
        if disc < 0:
            return False
        v = tt * (y * cd - x)
        return v > 0 and y * y * disc * sd * sd <= v * v

    while lo > 0 and not valid_float(lo):
        lo = max(0.0, lo - 0.001)
    if not valid_float(lo):
        return -1

    if valid_float(hi):
        guess = yn - 1
    else:
        for _ in range(72):
            mid = (lo + hi) / 2
            if valid_float(mid):
                lo = mid
            else:
                hi = mid
        guess = int(math.floor(lo * g + 1e-7))

    guess = min(guess, yn - 1)
    while guess > 0 and not step_ok_num(guess, yn, m, k, n, g):
        guess -= 1
    if guess <= 0:
        return -1
    while guess + 1 < yn and step_ok_num(guess + 1, yn, m, k, n, g):
        guess += 1
    return guess


def z_ok_num(zn: int, rlo: Fraction, k: int, n: int, g: int) -> bool:
    z = Fraction(zn, g)
    c, s = angle(k, n)
    return z + rlo * c >= 0 and (z + rlo * c) ** 2 >= 1 - rlo * rlo * s * s


def next_z_num(rlo: Fraction, k: int, n: int, g: int) -> int:
    c, s = angle(k, n)
    rf = float(rlo)
    cf = float(c)
    sf = float(s)
    root = -rf * cf + math.sqrt(max(0.0, 1 - rf * rf * sf * sf))
    guess = int(math.ceil(root * g - 1e-7))
    while guess > 0 and z_ok_num(guess - 1, rlo, k, n, g):
        guess -= 1
    while not z_ok_num(guess, rlo, k, n, g):
        guess += 1
    return guess


def tangent_data(s0: Fraction, m: Fraction) -> tuple[Fraction, Fraction]:
    a = 2 * (s0 * s0 + 3 * m) / (3 * (s0 * s0 + m) ** 2)
    b = 2 * s0**3 / (s0 * s0 + m) - a * s0**3
    if 3 * a - 2 <= 0:
        raise AssertionError("nonpositive master denominator")
    return a, b


def tangent_gap(s: Fraction, a: Fraction, b: Fraction, m: Fraction) -> Fraction:
    return a * s**3 + b - 2 * s**3 / (s * s + m)


def compute_coefficient(
    w: np.ndarray,
    z: np.ndarray,
    s0: Fraction,
    m: Fraction,
    n: int,
    g: int,
) -> tuple[Fraction, Fraction]:
    a, b = tangent_data(s0, m)
    acc = Fraction(0)
    for k in range(1, len(w)):
        c0, _ = angle(k - 1, n)
        c1, _ = angle(k, n)
        acc = floor_grid(
            acc + (c0 - c1) * tangent_gap(Fraction(int(w[k]), g), a, b, m),
            ROUND_DELTA,
        )
    for k, zn in enumerate(z, 1):
        c0, _ = angle(k - 1, n)
        c1, _ = angle(k, n)
        acc = floor_grid(
            acc + (c0 - c1) * tangent_gap(Fraction(int(zn), g), a, b, m),
            ROUND_DELTA,
        )
    coefficient = floor_grid((Fraction(2, 3) - 4 * b + 8 * acc) / (3 * a - 2), ROUND_COEFFICIENT)
    return coefficient, acc


def generate_row(spec: dict[str, Any]) -> dict[str, Any]:
    rlo = frac(spec["rlo"])
    rhi = frac(spec["rhi"])
    s0 = frac(spec["s0"])
    n = int(spec.get("N", ANGLE_N))
    g = int(spec.get("G", RADIAL_G))
    if (rlo * g).denominator != 1:
        raise AssertionError("left endpoint is not on the radial grid")

    m = 1 - rhi * rhi
    s0_floor = (s0.numerator * g) // s0.denominator
    w = [int(rlo * g)]
    k = 1
    while True:
        xn = next_w_num(w[-1], m, k, n, g, s0_floor)
        if xn < 0 or Fraction(xn, g) <= s0:
            next_w = xn
            break
        w.append(xn)
        k += 1
        if k >= n:
            raise AssertionError("positive chain reached angular-grid limit")

    z: list[int] = []
    k = 1
    while True:
        zn = next_z_num(rlo, k, n, g)
        if Fraction(zn, g) > s0:
            next_z = zn
            break
        z.append(zn)
        k += 1
        if k >= n:
            raise AssertionError("negative chain reached angular-grid limit")

    warr = np.asarray(w, dtype=np.int64)
    zarr = np.asarray(z, dtype=np.int64)
    coefficient, acc = compute_coefficient(warr, zarr, s0, m, n, g)
    return {
        "case": spec["case"],
        "rlo": rlo,
        "rhi": rhi,
        "s0": s0,
        "N": n,
        "G": g,
        "m": m,
        "w": warr,
        "z": zarr,
        "next_w": next_w,
        "next_z": next_z,
        "positive_steps": len(warr) - 1,
        "negative_steps": len(zarr),
        "gap_sum": acc,
        "coefficient": coefficient,
    }


def verify_row(row: dict[str, Any]) -> None:
    case = str(row["case"])
    rlo = frac(row["rlo"])
    rhi = frac(row["rhi"])
    s0 = frac(row["s0"])
    n = int(row["N"])
    g = int(row["G"])
    m = 1 - rhi * rhi
    w = np.asarray(row["w"], dtype=np.int64)
    z = np.asarray(row["z"], dtype=np.int64)

    if len(w) < 2 or int(w[0]) != int(rlo * g):
        raise AssertionError(f"{case}: invalid starting radius")
    if not np.all(w[:-1] > w[1:]):
        raise AssertionError(f"{case}: positive chain not strictly decreasing")
    if len(z) and not np.all(z[:-1] <= z[1:]):
        raise AssertionError(f"{case}: antipodal chain not nondecreasing")

    for k in range(1, len(w)):
        xn = int(w[k])
        yn = int(w[k - 1])
        if not step_ok_num(xn, yn, m, k, n, g):
            raise AssertionError(f"{case}: positive step {k} fails")
        if xn + 1 < yn and step_ok_num(xn + 1, yn, m, k, n, g):
            raise AssertionError(f"{case}: positive step {k} is not grid-maximal")
        if Fraction(xn, g) <= s0:
            raise AssertionError(f"{case}: retained positive step crosses s0")

    next_k = len(w)
    next_x = int(row["next_w"])
    if next_x >= 0 and Fraction(next_x, g) > s0:
        raise AssertionError(f"{case}: positive chain stopped too early")

    for k, zn64 in enumerate(z, 1):
        zn = int(zn64)
        if not z_ok_num(zn, rlo, k, n, g):
            raise AssertionError(f"{case}: antipodal step {k} fails")
        if zn > 0 and z_ok_num(zn - 1, rlo, k, n, g):
            raise AssertionError(f"{case}: antipodal step {k} is not grid-minimal")
        if Fraction(zn, g) > s0:
            raise AssertionError(f"{case}: retained antipodal step crosses s0")

    if Fraction(int(row["next_z"]), g) <= s0:
        raise AssertionError(f"{case}: antipodal chain stopped too early")

    eta = 1 / (2 * rlo * rlo) - 1
    tstar = 4 * eta * eta / (1 - eta) - 1
    for terminal in (len(w) - 1, len(z)):
        c, s = angle(terminal, n)
        if c * c - s * s <= tstar:
            raise AssertionError(f"{case}: cap disjointness fails")

    coefficient, acc = compute_coefficient(w, z, s0, m, n, g)
    if coefficient != row["coefficient"] or acc != row["gap_sum"]:
        raise AssertionError(f"{case}: coefficient replay mismatch")


def row_npz_path(case: str) -> Path:
    return CERT_DIR / f"{case.lower()}_exact.npz"


def write_row_npz(row: dict[str, Any]) -> None:
    path = row_npz_path(str(row["case"]))
    np.savez(
        path,
        case=np.asarray(str(row["case"])),
        rlo_num=np.int64(row["rlo"].numerator),
        rlo_den=np.int64(row["rlo"].denominator),
        rhi_num=np.int64(row["rhi"].numerator),
        rhi_den=np.int64(row["rhi"].denominator),
        s0_num=np.int64(row["s0"].numerator),
        s0_den=np.int64(row["s0"].denominator),
        angle_grid=np.int64(row["N"]),
        radial_grid=np.int64(row["G"]),
        coefficient_num=np.int64(row["coefficient"].numerator),
        coefficient_den=np.int64(row["coefficient"].denominator),
        gap_sum_num=np.asarray(str(row["gap_sum"].numerator)),
        gap_sum_den=np.asarray(str(row["gap_sum"].denominator)),
        next_w=np.int64(row["next_w"]),
        next_z=np.int64(row["next_z"]),
        w_num=row["w"],
        z_num=row["z"],
    )


def read_row_npz(case: str) -> dict[str, Any]:
    p = np.load(row_npz_path(case), allow_pickle=False)
    scalar = lambda key: int(np.asarray(p[key]).item())
    text = lambda key: str(np.asarray(p[key]).item())
    row = {
        "case": text("case"),
        "rlo": Fraction(scalar("rlo_num"), scalar("rlo_den")),
        "rhi": Fraction(scalar("rhi_num"), scalar("rhi_den")),
        "s0": Fraction(scalar("s0_num"), scalar("s0_den")),
        "N": scalar("angle_grid"),
        "G": scalar("radial_grid"),
        "coefficient": Fraction(scalar("coefficient_num"), scalar("coefficient_den")),
        "gap_sum": Fraction(int(text("gap_sum_num")), int(text("gap_sum_den"))),
        "next_w": scalar("next_w"),
        "next_z": scalar("next_z"),
        "w": np.asarray(p["w_num"], dtype=np.int64),
        "z": np.asarray(p["z_num"], dtype=np.int64),
    }
    row["m"] = 1 - row["rhi"] * row["rhi"]
    row["positive_steps"] = len(row["w"]) - 1
    row["negative_steps"] = len(row["z"])
    return row


def load_reference_certificate() -> dict[str, Any]:
    return json.loads((REFERENCE_DIR / "universal_contact_bound_certificate.json").read_text())


def canonical_json(data: dict[str, Any]) -> bytes:
    return (json.dumps(data, indent=2, sort_keys=True) + "\n").encode("utf-8")


def build_certificate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    reference = load_reference_certificate()
    pi_lo, pi_hi = P.pi_bounds()
    near = Fraction(reference["near_Jung_branch"]["volume_lower"])
    old = Fraction(reference["theorem"]["coefficient_of_pi"])
    if old != OLD_PI_COEFFICIENT:
        raise AssertionError("unexpected v1.0.0 theorem coefficient")

    if rows[0]["rlo"] != O3B02_LEFT or rows[0]["rhi"] != rows[1]["rlo"] or rows[1]["rhi"] != O3B02_RIGHT:
        raise AssertionError("split rows are not gap-free")

    for row, spec in zip(rows, CELL_SPECS, strict=True):
        if row["coefficient"] != spec["expected_coefficient"]:
            raise AssertionError(f"{row['case']}: unexpected exact coefficient")
        if row["positive_steps"] != spec["expected_positive_steps"]:
            raise AssertionError(f"{row['case']}: unexpected positive-step count")
        if row["negative_steps"] != spec["expected_negative_steps"]:
            raise AssertionError(f"{row['case']}: unexpected negative-step count")
        if row["coefficient"] <= CANDIDATE_PI_COEFFICIENT:
            raise AssertionError(f"{row['case']}: does not clear candidate theorem")

    inherited_rows = []
    for item in reference["lower_branch"]["rows"]:
        if item["case"] == "O3B02":
            continue
        coeff = Fraction(item["coefficient_of_pi"])
        if coeff <= CANDIDATE_PI_COEFFICIENT:
            raise AssertionError(f"inherited row {item['case']} does not clear candidate")
        inherited_rows.append(item)

    near_margin = near - CANDIDATE_PI_COEFFICIENT * pi_hi
    gain = CANDIDATE_PI_COEFFICIENT * pi_lo - old * pi_hi
    if near_margin <= 0:
        raise AssertionError("unchanged near-Jung branch does not clear candidate")
    if gain <= 0:
        raise AssertionError("candidate does not strictly improve v1.0.0")

    theorem_lower = CANDIDATE_PI_COEFFICIENT * pi_lo
    theorem_upper = CANDIDATE_PI_COEFFICIENT * pi_hi
    split_min = min(row["coefficient"] for row in rows)
    split_margin = (split_min - CANDIDATE_PI_COEFFICIENT) * pi_lo

    row_records = []
    for row in rows:
        row_records.append(
            {
                "case": row["case"],
                "interval": [str(row["rlo"]), str(row["rhi"])],
                "s0": str(row["s0"]),
                "angle_grid": row["N"],
                "radial_grid": row["G"],
                "positive_steps": row["positive_steps"],
                "negative_steps": row["negative_steps"],
                "coefficient_of_pi": str(row["coefficient"]),
                "coefficient_times_pi_lower": decimal_string(row["coefficient"] * pi_lo, 55),
                "npz_sha256": sha256(row_npz_path(row["case"])),
            }
        )

    return {
        "schema": "minvol-terminal-handoff-v1.1-candidate-v1",
        "status": "PROPOSED EXACT CANDIDATE; pending public-repository integration and independent R replay",
        "scope": {
            "theorem_architecture_changed": False,
            "tests_performed": [
                "split O3B02 into two through four subintervals",
                "local rational retuning of terminal tangent radii",
                "doubled angular resolution",
                "small leftward handoff perturbations with unchanged near-Jung fan",
            ],
        },
        "dependencies": {
            "v1_certificate_sha256": sha256(REFERENCE_DIR / "universal_contact_bound_certificate.json"),
            "v1_adjusted_fan_sha256": sha256(REFERENCE_DIR / "universal_contact_fan.npz"),
            "v1_exact_geometry_sha256": sha256(REFERENCE_DIR / "exact_geometry.py"),
            "reference_handoff_sha256": sha256(REFERENCE_DIR / "reference_handoff_certificate.json"),
        },
        "old_theorem": {
            "coefficient_of_pi": str(old),
            "coefficient_lower": decimal_string(old * pi_lo, 55),
        },
        "terminal_split": {
            "original_interval": [str(O3B02_LEFT), str(O3B02_RIGHT)],
            "split_point": str(O3B02_MID),
            "rows": row_records,
            "minimum_coefficient_of_pi": str(split_min),
            "minimum_times_pi_lower": decimal_string(split_min * pi_lo, 55),
        },
        "unchanged_near_Jung_branch": {
            "exact_rational_lower": str(near),
            "decimal_lower": reference["near_Jung_branch"]["volume_lower_decimal"],
        },
        "candidate_theorem": {
            "coefficient_of_pi": str(CANDIDATE_PI_COEFFICIENT),
            "statement": (
                "Every convex body K in R^3 of constant width d>0 satisfies "
                f"Vol(K) >= ({CANDIDATE_PI_COEFFICIENT}*pi)d^3."
            ),
            "decimal_lower": decimal_string(theorem_lower, 55),
            "decimal_upper": decimal_string(theorem_upper, 55),
            "strict_gain_over_v1_upper": decimal_string(gain, 55),
            "near_Jung_margin_over_candidate_upper": decimal_string(near_margin, 55),
            "split_row_margin_over_candidate_lower": decimal_string(split_margin, 55),
        },
        "claim_boundary": {
            "exactly_established_inside_audit": [
                "the two split O3B02 row certificates",
                "the strict comparison of every unchanged lower row with the candidate coefficient",
                "the strict comparison of the unchanged near-Jung rational lower with the candidate coefficient",
                "the strict improvement over public v1.0.0",
            ],
            "not_yet_established": [
                "public v1.1.0 integration",
                "independent base-R replay in the construction environment",
                "new mutation/reconstruction tests against the integrated v1.1.0 certificate",
                "hosted continuous-integration replay",
            ],
        },
    }


def write_rows_tsv(rows: list[dict[str, Any]], pi_lo: Fraction) -> None:
    path = CERT_DIR / "terminal_handoff_v11_rows.tsv"
    with path.open("w", newline="") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow(
            [
                "case",
                "rlo",
                "rhi",
                "s0",
                "angle_grid",
                "radial_grid",
                "positive_steps",
                "negative_steps",
                "coefficient_of_pi",
                "coefficient_times_pi_lower",
            ]
        )
        for row in rows:
            writer.writerow(
                [
                    row["case"],
                    row["rlo"],
                    row["rhi"],
                    row["s0"],
                    row["N"],
                    row["G"],
                    row["positive_steps"],
                    row["negative_steps"],
                    row["coefficient"],
                    decimal_string(row["coefficient"] * pi_lo, 30),
                ]
            )


def write_audit_csv(certificate: dict[str, Any]) -> None:
    c = certificate["candidate_theorem"]
    old = certificate["old_theorem"]
    split = certificate["terminal_split"]
    near = certificate["unchanged_near_Jung_branch"]
    path = CERT_DIR / "audit_constants.csv"
    rows = [
        ("old_v1_volume", old["coefficient_lower"]),
        ("candidate_v11_volume_lower", c["decimal_lower"]),
        ("candidate_v11_volume_upper", c["decimal_upper"]),
        ("near_jung_volume_lower", near["decimal_lower"]),
        ("split_terminal_min_volume_lower", split["minimum_times_pi_lower"]),
        ("gain_over_v1", c["strict_gain_over_v1_upper"]),
        ("near_margin", c["near_Jung_margin_over_candidate_upper"]),
        ("split_margin", c["split_row_margin_over_candidate_lower"]),
    ]
    with path.open("w", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["name", "value"])
        writer.writerows(rows)


def write_or_verify(write: bool) -> dict[str, Any]:
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    generated_rows = [generate_row(spec) for spec in CELL_SPECS]
    for row in generated_rows:
        verify_row(row)

    if write:
        for row in generated_rows:
            write_row_npz(row)
    else:
        for generated in generated_rows:
            stored = read_row_npz(generated["case"])
            verify_row(stored)
            for key in ("rlo", "rhi", "s0", "N", "G", "coefficient", "gap_sum", "next_w", "next_z"):
                if stored[key] != generated[key]:
                    raise AssertionError(f"{generated['case']}: stored {key} differs from regeneration")
            if not np.array_equal(stored["w"], generated["w"]):
                raise AssertionError(f"{generated['case']}: stored positive chain differs")
            if not np.array_equal(stored["z"], generated["z"]):
                raise AssertionError(f"{generated['case']}: stored antipodal chain differs")

    # NPZ hashes enter the candidate JSON, so build it only after files exist.
    certificate = build_certificate(generated_rows)
    cert_path = CERT_DIR / "terminal_handoff_v11_certificate.json"
    encoded = canonical_json(certificate)
    if write:
        cert_path.write_bytes(encoded)
        pi_lo, _ = P.pi_bounds()
        write_rows_tsv(generated_rows, pi_lo)
        write_audit_csv(certificate)
    else:
        if cert_path.read_bytes() != encoded:
            raise AssertionError("candidate certificate JSON is stale or manually divergent")

    return certificate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write canonical proof objects")
    args = parser.parse_args()

    certificate = write_or_verify(args.write)
    c = certificate["candidate_theorem"]
    split = certificate["terminal_split"]
    print(f"Candidate coefficient of pi: {c['coefficient_of_pi']}")
    print(f"Candidate decimal lower:      {c['decimal_lower']}")
    print(f"Strict gain over v1.0.0:      {c['strict_gain_over_v1_upper']}")
    print(f"Near-Jung strict margin:      {c['near_Jung_margin_over_candidate_upper']}")
    print(f"Split-row strict margin:      {c['split_row_margin_over_candidate_lower']}")
    for row in split["rows"]:
        print(
            f"{row['case']}: {row['interval'][0]} to {row['interval'][1]}, "
            f"s0={row['s0']}, pi coefficient={row['coefficient_of_pi']}"
        )
    print("MINVOL TERMINAL-HANDOFF V1.1 CANDIDATE: EXACT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
