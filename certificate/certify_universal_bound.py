#!/usr/bin/env python3
"""Standalone exact certificate for the universal MinVol contact bound.

The verifier proves the proposed universal coefficient

    Vol(K) >= (26220940089713*pi/200000000000000) d^3

from immutable local proof objects. All theorem-supporting comparisons use
Python integers and ``fractions.Fraction``. NumPy is used only to read the
integer NPZ proof objects. The verifier imports no private repository package
and requires no network access.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import exact_geometry as P

DATA = HERE / "certificates"
REFERENCE_CERT = DATA / "reference_handoff_certificate.json"
REFERENCE_FAN = DATA / "reference_near_jung_fan.npz"
FAN_DATA = DATA / "universal_contact_fan.npz"
ROW_FILES = tuple(DATA / f"refined_lower_cell_{i}.npz" for i in range(1, 5))
FAN_AUDIT = DATA / "fan_orbit_margin_audit.tsv"
HULL_AUDIT = DATA / "all_axis_pair_section_hulls.tsv"
ROW_AUDIT = DATA / "refined_lower_rows.tsv"
AUDIT_CONSTANTS = DATA / "audit_constants.csv"
CERT_PATH = DATA / "universal_contact_bound_certificate.json"

SCHEMA = "minvol.universal_contact_bound.v1"
REFERENCE_CERT_SHA256 = "36a6d5cc145fdda500b3cfa8f77a784e6e29860efc44196b05684ee4c348b7af"
REFERENCE_FAN_SHA256 = "dcd9c4945cad4960f0a1a933d34b272190bb21d351e03eec3c2d4a708ed26200"
FAN_DATA_SHA256 = "7ad091a639b46f55e87672d38687840d8e1196df9700224816743974334a1ed7"
ROW_SHA256 = (
    "e1d81d7b836056eb6c9c6ac79fc702dd2ff505fffa21e811c3c2ece43277e2db",
    "dc477ef8ecee76fbd0988a3b4bd6c37bd5de2d7d7de4d83ce3dc5e6cbf240cb9",
    "9a80061496c001e86e4941a35544bba93031c51b0f3b1a22113dcf9b1b261385",
    "e7eefac1c402ee489abed18f377ae4fdb0d39a4bcd1c91e144acc7d7719d02ea",
)

R_SPLIT = Fraction(305_695_601, 500_000_000)
Q_SPLIT = R_SPLIT * R_SPLIT
Q_JUNG = Fraction(3, 8)
THEOREM_PI_COEFFICIENT = Fraction(26_220_940_089_713, 200_000_000_000_000)
PREVIOUS_PI_COEFFICIENT = Fraction(131_098_268_771_713, 10**15)
HYRA_PI_COEFFICIENT = Fraction(130_838_246_407_123, 10**15)
FAN_MARGIN_TARGET = Fraction(1, 10**12)

ROW_ANGLE_N = 76_800
ROW_GRID = 40_000_000_000
ROUND_DELTA = 10**18
ROUND_COEF = 10**15
ROW_EXPECTED = (
    {
        "case": "O3A1R1",
        "interval": (Fraction(30_549, 50_000), Fraction(30_553, 50_000)),
        "s0": Fraction(4_970_516, 10_000_000),
    },
    {
        "case": "O3A1R2",
        "interval": (Fraction(30_553, 50_000), Fraction(30_557, 50_000)),
        "s0": Fraction(4_972_048, 10_000_000),
    },
    {
        "case": "O3A1R3",
        "interval": (Fraction(30_557, 50_000), Fraction(30_561, 50_000)),
        "s0": Fraction(4_973_598, 10_000_000),
    },
    {
        "case": "O3A1R4",
        "interval": (Fraction(30_561, 50_000), Fraction(6_113, 10_000)),
        "s0": Fraction(4_975_169, 10_000_000),
    },
)

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def fs(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def dec(x: Fraction, digits: int = 60) -> str:
    getcontext().prec = digits + 100
    return format(Decimal(x.numerator) / Decimal(x.denominator), f".{digits}f")


def floor_grid(x: Fraction, denominator: int) -> Fraction:
    return Fraction((x.numerator * denominator) // x.denominator, denominator)


def angle(k: int) -> tuple[Fraction, Fraction]:
    t = Fraction(k, ROW_ANGLE_N)
    return (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)


def delta_angle(k: int) -> tuple[Fraction, Fraction]:
    c0, s0 = angle(k - 1)
    c1, s1 = angle(k)
    return c1 * c0 + s1 * s0, s1 * c0 - c1 * s0


def step_ok(X: Fraction, Y: Fraction, m: Fraction, cd: Fraction, sd: Fraction) -> bool:
    T = X * X + m
    D = 4 * X * X - T * T
    return (
        D >= 0
        and T * (Y * cd - X) > 0
        and Y * Y * D * sd * sd <= T * T * (Y * cd - X) ** 2
    )


def tangent_gap(s: Fraction, a: Fraction, b: Fraction, m: Fraction) -> Fraction:
    return a * s**3 + b - 2 * s**3 / (s * s + m)


def stored_fraction(data: np.lib.npyio.NpzFile, key: str) -> Fraction:
    return Fraction(int(data[f"{key}_num"]), int(data[f"{key}_den"]))


def replay_refined_row(path: Path, expected: dict[str, Any]) -> dict[str, Any]:
    data = np.load(path, allow_pickle=False)
    rlo = stored_fraction(data, "rlo")
    rhi = stored_fraction(data, "rhi")
    s0 = stored_fraction(data, "s0")
    coefficient = stored_fraction(data, "coef")
    if (rlo, rhi) != expected["interval"] or s0 != expected["s0"]:
        raise AssertionError(f"{expected['case']} interval or tangency mismatch")
    if int(data["N"]) != ROW_ANGLE_N or int(data["grid"]) != ROW_GRID:
        raise AssertionError(f"{expected['case']} grid metadata mismatch")

    ws = [Fraction(int(v), ROW_GRID) for v in np.asarray(data["w_num"], dtype=np.int64)]
    zs = [Fraction(int(v), ROW_GRID) for v in np.asarray(data["z_num"], dtype=np.int64)]
    if not ws or ws[0] != rlo:
        raise AssertionError(f"{expected['case']} positive chain start mismatch")

    m = 1 - rhi * rhi
    a = 2 * (s0 * s0 + 3 * m) / (3 * (s0 * s0 + m) ** 2)
    b = 2 * s0**3 / (s0 * s0 + m) - a * s0**3
    if 3 * a - 2 <= 0:
        raise AssertionError(f"{expected['case']} nonpositive master denominator")

    for k in range(1, len(ws)):
        cd, sd = delta_angle(k)
        if not (ws[k - 1] > ws[k] > s0 and step_ok(ws[k], ws[k - 1], m, cd, sd)):
            raise AssertionError(f"{expected['case']} positive step {k} failed")

    for k, z in enumerate(zs, 1):
        c, s = angle(k)
        if z > s0 or z + rlo * c < 0 or (z + rlo * c) ** 2 < 1 - rlo * rlo * s * s:
            raise AssertionError(f"{expected['case']} antipodal step {k} failed")

    eta = 1 / (2 * rlo * rlo) - 1
    tstar = 4 * eta * eta / (1 - eta) - 1
    for terminal in (len(ws) - 1, len(zs)):
        c, s = angle(terminal)
        if c * c - s * s <= tstar:
            raise AssertionError(f"{expected['case']} cap disjointness failed")

    acc = Fraction(0)
    for k in range(1, len(ws)):
        c0, _ = angle(k - 1)
        c1, _ = angle(k)
        acc = floor_grid(acc + (c0 - c1) * tangent_gap(ws[k], a, b, m), ROUND_DELTA)
    for k, z in enumerate(zs, 1):
        c0, _ = angle(k - 1)
        c1, _ = angle(k)
        acc = floor_grid(acc + (c0 - c1) * tangent_gap(z, a, b, m), ROUND_DELTA)
    rebuilt = floor_grid((Fraction(2, 3) - 4 * b + 8 * acc) / (3 * a - 2), ROUND_COEF)
    if rebuilt != coefficient:
        raise AssertionError(f"{expected['case']} coefficient reconstruction failed")
    if coefficient <= THEOREM_PI_COEFFICIENT:
        raise AssertionError(f"{expected['case']} does not clear O3B02")

    return {
        "case": expected["case"],
        "interval": [fs(rlo), fs(rhi)],
        "s0": fs(s0),
        "angle_grid_N": ROW_ANGLE_N,
        "radial_grid": ROW_GRID,
        "positive_steps": len(ws) - 1,
        "negative_steps": len(zs),
        "coefficient_of_pi": fs(coefficient),
        "coefficient_decimal": dec(coefficient, 18),
        "margin_over_O3B02_coefficient": fs(coefficient - THEOREM_PI_COEFFICIENT),
    }


def verify_refined_rows(write: bool) -> list[dict[str, Any]]:
    for path, digest in zip(ROW_FILES, ROW_SHA256):
        if not path.exists() or sha256(path) != digest:
            raise RuntimeError(f"refined-row proof-object fingerprint mismatch: {path}")
    rows = [replay_refined_row(path, expected) for path, expected in zip(ROW_FILES, ROW_EXPECTED)]
    lines = [
        "case\tleft\tright\ts0\tangle_N\tradial_grid\tpositive_steps\tnegative_steps\tcoefficient_of_pi\tmargin_over_O3B02\n"
    ]
    for row in rows:
        lines.append(
            f"{row['case']}\t{row['interval'][0]}\t{row['interval'][1]}\t{row['s0']}\t"
            f"{row['angle_grid_N']}\t{row['radial_grid']}\t{row['positive_steps']}\t"
            f"{row['negative_steps']}\t{row['coefficient_of_pi']}\t"
            f"{row['margin_over_O3B02_coefficient']}\n"
        )
    blob = "".join(lines).encode("ascii")
    if write:
        ROW_AUDIT.write_bytes(blob)
    elif not ROW_AUDIT.exists() or ROW_AUDIT.read_bytes() != blob:
        raise RuntimeError("refined O3A1 row audit is not byte-identical")
    return rows


def verify_coordinate_width_lemma() -> dict[str, Any]:
    """Replay the exact linear decompositions behind the width sharpening.

    Deficiencies are ordered as e01,e02,e03,e12,e13,e23, with e01 dominant.
    If x=L(y-c), set A=2*sqrt(2)*L and H=A^T A, so H=I for the
    regular unit-edge tetrahedron.  Direct edge-length algebra gives the
    diagonal formulas stored below.  The displayed remainders prove
    H00 <= 1+S/2 and
    H11,H22 <= 1+S/6 under e01 >= every other deficiency.
    """
    # Coefficients of 2(H_jj-1), in the fixed edge order.
    diag = (
        (1, -1, -1, -1, -1, 1),
        (-1, 1, -1, -1, 1, -1),
        (-1, -1, 1, 1, -1, -1),
    )
    # 2[(1+S/2)-H00] = S - 2(H00-1).
    rem0 = tuple(1 - c for c in diag[0])
    if rem0 != (0, 2, 2, 2, 2, 0):
        raise AssertionError("axis-0 diagonal remainder identity failed")

    # 6[(1+S/6)-H11] = S - 3*2(H11-1).
    rem1 = tuple(1 - 3 * c for c in diag[1])
    rem2 = tuple(1 - 3 * c for c in diag[2])
    # Dominance decompositions:
    # rem1 = 2(e01-e02)+2(e01-e13)+4(e03+e12+e23).
    if rem1 != (4, -2, 4, 4, -2, 4):
        raise AssertionError("axis-1 diagonal remainder identity failed")
    # rem2 = 2(e01-e03)+2(e01-e12)+4(e02+e13+e23).
    if rem2 != (4, 4, -2, -2, 4, 4):
        raise AssertionError("axis-2 diagonal remainder identity failed")

    return {
        "edge_order": ["e01", "e02", "e03", "e12", "e13", "e23"],
        "dominant_edge": "e01",
        "normalized_gram_diagonal_twice_offsets": [list(x) for x in diag],
        "axis0_upper": "H00 <= 1 + S/2",
        "axis1_upper": "H11 <= 1 + S/6",
        "axis2_upper": "H22 <= 1 + S/6",
        "inverse_diagonal_argument": (
            "For positive-definite H, Cauchy-Schwarz gives "
            "1 <= Hjj*(H^{-1})jj."
        ),
    }


def verify_fan_and_caps(write: bool) -> dict[str, Any]:
    expected = {
        REFERENCE_CERT: REFERENCE_CERT_SHA256,
        REFERENCE_FAN: REFERENCE_FAN_SHA256,
        FAN_DATA: FAN_DATA_SHA256,
    }
    for path, digest in expected.items():
        if not path.exists() or sha256(path) != digest:
            raise RuntimeError(f"proof-object fingerprint mismatch: {path}")

    reference_cert = json.loads(REFERENCE_CERT.read_text())
    reference = np.load(REFERENCE_FAN, allow_pickle=False)
    data = np.load(FAN_DATA, allow_pickle=False)
    reference_radial = np.asarray(reference["Aint"], dtype=np.int64)
    reference_delta = np.asarray(reference["delta_num"], dtype=np.int64)
    radial = np.asarray(data["Aint"], dtype=np.int64)
    delta = np.asarray(data["delta_num"], dtype=np.int64)
    if radial.shape != (98_306,) or delta.shape != (98_306,):
        raise AssertionError("new fan data shape mismatch")
    if np.any(radial <= 0) or np.any(radial > reference_radial):
        raise AssertionError("new fan is not nested in the reference fan")
    if not np.array_equal(delta, reference_delta):
        raise AssertionError("new fan changed inherited S-procedure multipliers")
    if int(data["R_num"]) != R_SPLIT.numerator or int(data["R_den"]) != R_SPLIT.denominator:
        raise AssertionError("new fan split metadata mismatch")
    if int(data["DBITS"]) != P.DBITS:
        raise AssertionError("new fan multiplier-bit metadata mismatch")

    qvec, faces, edges, index = P.reconstruct_cube_fan()
    orbits = P.stabilizer_orbits(qvec, index)
    for orbit in orbits:
        if len({int(radial[i]) for i in orbit}) != 1 or len({int(delta[i]) for i in orbit}) != 1:
            raise AssertionError("new fan is not edge-stabilizer invariant")

    reference_R = Fraction(int(reference["R_num"]), int(reference["R_den"]))
    reference_E = (3 - 8 * reference_R * reference_R) / (4 * reference_R * reference_R - 1)
    expected_reference_min = Fraction(reference_cert["near_jung_reference_fan"]["minimum_margin"])
    expected_reference_index = int(reference_cert["near_jung_reference_fan"]["minimum_margin_index"])
    reference_min: Fraction | None = None
    reference_min_index = -1
    for i, q in enumerate(qvec):
        margin, _, _ = P.exact_margin(q, int(reference_radial[i]), int(reference_delta[i]), reference_E)
        if margin is not None and (reference_min is None or margin < reference_min):
            reference_min, reference_min_index = margin, i
    if reference_min != expected_reference_min or reference_min_index != expected_reference_index:
        raise AssertionError("reference exact-margin regression failed")

    E = (3 - 8 * Q_SPLIT) / (4 * Q_SPLIT - 1)
    census = [0, 0, 0]
    active_census = {"edge": 0, "dominant": 0, "tie": 0, "convex": 0}
    minimum: Fraction | None = None
    minimum_index = -1
    audit_lines = [
        "representative\torbit_size\tradial_numerator\tdelta_numerator\tnegative_count\tactive_bound\tmargin_decimal\n"
    ]
    # Traverse one stabilizer orbit at a time.  This still recomputes and checks
    # every one of the 98,306 vertices exactly, but does not retain 98,306 huge
    # Fraction objects in memory after the check.
    for orbit in orbits:
        rep = orbit[0]
        rep_margin, rep_active, rep_nneg = P.exact_margin(
            qvec[rep], int(radial[rep]), int(delta[rep]), E
        )
        for i in orbit:
            margin, which, nneg = P.exact_margin(qvec[i], int(radial[i]), int(delta[i]), E)
            if margin != rep_margin or which != rep_active or nneg != rep_nneg:
                raise AssertionError("orbit margin is not exactly invariant")
            census[nneg] += 1
            active_census[which] += 1
            if margin is not None:
                if margin <= FAN_MARGIN_TARGET:
                    raise AssertionError(f"new fan vertex {i} fails exact margin")
                if minimum is None or margin < minimum:
                    minimum, minimum_index = margin, i
        margin_text = (
            "1.000000000000000000000000"
            if rep_margin is None
            else dec(rep_margin, 24)
        )
        audit_lines.append(
            f"{rep}\t{len(orbit)}\t{int(radial[rep])}\t{int(delta[rep])}\t"
            f"{rep_nneg}\t{rep_active}\t{margin_text}\n"
        )
    if minimum is None or census != [4, 83_616, 14_686]:
        raise AssertionError("new fan active-set census mismatch")
    audit_blob = "".join(audit_lines).encode("ascii")
    if write:
        FAN_AUDIT.write_bytes(audit_blob)
    elif not FAN_AUDIT.exists() or FAN_AUDIT.read_bytes() != audit_blob:
        raise RuntimeError("fan orbit audit is not byte-identical")

    raw_den = 6 * P.N**3 * (1 << P.BITS) ** 3
    reference_raw_num = 0
    raw_num = 0
    minimum_cone_det: int | None = None
    for i, j, k in faces:
        determinant = P.det3_int(qvec[i], qvec[j], qvec[k])
        minimum_cone_det = determinant if minimum_cone_det is None else min(minimum_cone_det, determinant)
        reference_raw_num += int(reference_radial[i]) * int(reference_radial[j]) * int(reference_radial[k]) * determinant
        raw_num += int(radial[i]) * int(radial[j]) * int(radial[k]) * determinant
    if reference_raw_num != int(str(reference["volnum"].item())) or raw_den != int(str(reference["volden"].item())):
        raise AssertionError("reconstructed reference fan volume mismatch")
    if raw_num != int(str(data["volnum"].item())) or raw_den != int(str(data["volden"].item())):
        raise AssertionError("stored new fan volume mismatch")
    C = Fraction(raw_num, 2 * raw_den)

    coord_den = (1 << 51) * P.N
    coords = [
        tuple(Fraction(int(radial[i]) * qvec[i][j], coord_den) for j in range(3))
        for i in range(len(qvec))
    ]
    supports: dict[tuple[int, int], Fraction] = {}
    hulls: dict[tuple[int, int], list[tuple[Fraction, Fraction]]] = {}
    areas: dict[tuple[int, int], Fraction] = {}
    for axis in range(3):
        supports[(axis, 1)] = max(v[axis] for v in coords)
        supports[(axis, -1)] = max(-v[axis] for v in coords)
        for sign in (1, -1):
            base = P.BASES[(axis, sign)]
            if not base < supports[(axis, sign)]:
                raise AssertionError("section plane is not below fan support")
            hull = P.section_hull(coords, edges, axis, sign, base)
            hulls[(axis, sign)] = hull
            areas[(axis, sign)] = P.polygon_area(hull)

    hull_lines = ["axis\tsign\tindex\tu_num\tu_den\tv_num\tv_den\n"]
    for axis, sign in sorted(hulls):
        for i, (u, v) in enumerate(hulls[(axis, sign)]):
            hull_lines.append(
                f"{axis}\t{sign}\t{i}\t{u.numerator}\t{u.denominator}\t"
                f"{v.numerator}\t{v.denominator}\n"
            )
    hull_blob = "".join(hull_lines).encode("ascii")
    if write:
        HULL_AUDIT.write_bytes(hull_blob)
    elif not HULL_AUDIT.exists() or HULL_AUDIT.read_bytes() != hull_blob:
        raise RuntimeError("all-axis section hull audit is not byte-identical")

    # The full coordinate list contains nearly 300,000 exact fractions.  The
    # six small hulls, areas, and supports are now independent of it.
    del coords

    sharp_census = P.determinant_sharp_census()
    det_sq = 1 - E / 2 - E * E / 2
    det_lower = P.sqrt_lower(det_sq)
    core_lower = C * P.sqrt_lower(det_sq / 2)

    width_squared_lower = {
        0: Fraction(1, 1) / (1 + E / 2),
        1: Fraction(1, 1) / (1 + E / 6),
        2: Fraction(1, 1) / (1 + E / 6),
    }
    coordinate_width_lower = {axis: P.sqrt_lower(width_squared_lower[axis]) for axis in range(3)}
    sqrt2_lower = P.sqrt_lower(Fraction(2))

    allocations: dict[int, dict[str, Any]] = {}
    total_cap_lower = Fraction(0)
    for axis in range(3):
        support_plus = supports[(axis, 1)]
        support_minus = supports[(axis, -1)]
        total_excess = coordinate_width_lower[axis] - (support_plus + support_minus) / (2 * sqrt2_lower)
        depth_plus = (support_plus - P.BASES[(axis, 1)]) / (2 * sqrt2_lower)
        depth_minus = (support_minus - P.BASES[(axis, -1)]) / (2 * sqrt2_lower)
        if min(total_excess, depth_plus, depth_minus) <= 0:
            raise AssertionError("nonpositive cap geometry parameter")
        allocation = P.allocation_certificate(
            areas[(axis, 1)], depth_plus, areas[(axis, -1)], depth_minus, total_excess, det_lower
        )
        allocations[axis] = {
            "coordinate_width_squared_lower": width_squared_lower[axis],
            "coordinate_width_lower": coordinate_width_lower[axis],
            "total_excess": total_excess,
            "depth_plus": depth_plus,
            "depth_minus": depth_minus,
            **allocation,
        }
        total_cap_lower += allocation["lower"]

    center_coordinate_upper = 3 - 8 * Q_SPLIT
    minimum_signed_support = min(supports.values())
    overlap_norm_squared_lower = 2 * (minimum_signed_support - center_coordinate_upper) ** 2
    ellipsoid_radius_squared_upper = Fraction(3, 1) / (1 - E)
    if minimum_signed_support <= center_coordinate_upper:
        raise AssertionError("support threshold does not dominate center uncertainty")
    if overlap_norm_squared_lower <= ellipsoid_radius_squared_upper:
        raise AssertionError("cross-axis cap disjointness failed")

    near_lower = core_lower + total_cap_lower
    return {
        "vertex_count": len(qvec),
        "face_count": len(faces),
        "edge_count": len(edges),
        "orbit_count": len(orbits),
        "E": E,
        "C": C,
        "determinant_census": sharp_census,
        "determinant_squared_lower": det_sq,
        "determinant_lower": det_lower,
        "core_volume_lower": core_lower,
        "near_volume_lower": near_lower,
        "total_cap_lower": total_cap_lower,
        "supports": supports,
        "hulls": hulls,
        "areas": areas,
        "allocations": allocations,
        "coordinate_width_squared_lower": width_squared_lower,
        "coordinate_width_lower": coordinate_width_lower,
        "center_coordinate_upper": center_coordinate_upper,
        "minimum_signed_support": minimum_signed_support,
        "overlap_norm_squared_lower": overlap_norm_squared_lower,
        "ellipsoid_radius_squared_upper": ellipsoid_radius_squared_upper,
        "cross_axis_gap": overlap_norm_squared_lower - ellipsoid_radius_squared_upper,
        "active_set_census": census,
        "active_bound_census": active_census,
        "changed_vertices": int(np.sum(radial < reference_radial)),
        "minimum_radial_ratio": min(
            Fraction(int(radial[i]), int(reference_radial[i])) for i in range(len(radial))
        ),
        "minimum_margin": minimum,
        "minimum_margin_index": minimum_index,
        "minimum_cone_determinant": minimum_cone_det,
        "reference_margin_regression": reference_min,
        "reference_margin_regression_index": reference_min_index,
    }


def write_audit_constants(values: dict[str, Fraction], write: bool) -> None:
    lines = ["name,numerator,denominator,decimal\n"]
    for name in sorted(values):
        value = values[name]
        lines.append(f"{name},{value.numerator},{value.denominator},{dec(value, 25)}\n")
    blob = "".join(lines).encode("ascii")
    if write:
        AUDIT_CONSTANTS.write_bytes(blob)
    elif not AUDIT_CONSTANTS.exists() or AUDIT_CONSTANTS.read_bytes() != blob:
        raise RuntimeError("audit constants are not byte-identical")


def build_certificate(write: bool = False) -> dict[str, Any]:
    reference_cert = json.loads(REFERENCE_CERT.read_text())
    if reference_cert.get("schema") != "minvol.reference_handoff.v1":
        raise RuntimeError("unexpected reference certificate schema")

    width_lemma = verify_coordinate_width_lemma()
    refined_rows = verify_refined_rows(write)
    rows: list[dict[str, Any]] = []
    inserted = False
    for row in reference_cert["lower_branch"]["rows_through_handoff"]:
        case = row["case"]
        if case == "O3A1":
            rows.extend(refined_rows)
            inserted = True
            continue
        rows.append(row)
        if case == "O3B02":
            break
    if not inserted or rows[-1]["case"] != "O3B02":
        raise AssertionError("lower-row replacement assembly failed")

    weakest_name = ""
    weakest: Fraction | None = None
    previous = Fraction(1, 2)
    for row in rows:
        left, right = map(Fraction, row["interval"])
        if left != previous:
            raise AssertionError(f"lower partition gap before {row['case']}")
        previous = right
        coefficient = Fraction(row["coefficient_of_pi"])
        if weakest is None or coefficient < weakest:
            weakest, weakest_name = coefficient, row["case"]
    if previous != R_SPLIT or weakest != THEOREM_PI_COEFFICIENT or weakest_name != "O3B02":
        raise AssertionError("new lower-branch bottleneck mismatch")

    fan = verify_fan_and_caps(write)
    pi_lo, pi_hi = P.pi_bounds()
    theorem_lo = THEOREM_PI_COEFFICIENT * pi_lo
    theorem_hi = THEOREM_PI_COEFFICIENT * pi_hi
    previous_hi = PREVIOUS_PI_COEFFICIENT * pi_hi
    hyra_hi = HYRA_PI_COEFFICIENT * pi_hi
    near_margin = fan["near_volume_lower"] - theorem_hi
    gain = theorem_lo - previous_hi
    refined_min = min(Fraction(row["coefficient_of_pi"]) for row in refined_rows)
    refined_margin = refined_min - THEOREM_PI_COEFFICIENT
    if near_margin <= 0 or gain <= 0 or theorem_lo <= hyra_hi or refined_margin <= 0:
        raise AssertionError("universal assembly ordering failed")

    values: dict[str, Fraction] = {
        "split_radius": R_SPLIT,
        "sharp_total_deficiency_upper": fan["E"],
        "reference_fan_coefficient": fan["C"],
        "determinant_squared_lower": fan["determinant_squared_lower"],
        "core_volume_lower": fan["core_volume_lower"],
        "axis0_coordinate_width_squared_lower": fan["coordinate_width_squared_lower"][0],
        "axis1_coordinate_width_squared_lower": fan["coordinate_width_squared_lower"][1],
        "axis2_coordinate_width_squared_lower": fan["coordinate_width_squared_lower"][2],
        "axis0_coordinate_width_lower": fan["coordinate_width_lower"][0],
        "axis1_coordinate_width_lower": fan["coordinate_width_lower"][1],
        "axis2_coordinate_width_lower": fan["coordinate_width_lower"][2],
        "total_cap_lower": fan["total_cap_lower"],
        "near_jung_volume_lower": fan["near_volume_lower"],
        "near_jung_margin": near_margin,
        "cross_axis_gap": fan["cross_axis_gap"],
        "minimum_fan_margin": fan["minimum_margin"],
        "theorem_pi_coefficient": THEOREM_PI_COEFFICIENT,
        "theorem_volume_lower": theorem_lo,
        "theorem_volume_upper": theorem_hi,
        "strict_gain_over_previous": gain,
        "minimum_refined_row_pi_coefficient": refined_min,
        "minimum_refined_row_margin": refined_margin,
    }
    for i, row in enumerate(refined_rows, 1):
        values[f"refined_row{i}_pi_coefficient"] = Fraction(row["coefficient_of_pi"])
        values[f"refined_row{i}_margin"] = Fraction(row["margin_over_O3B02_coefficient"])
    for axis in range(3):
        values[f"axis{axis}_support_plus"] = fan["supports"][(axis, 1)]
        values[f"axis{axis}_support_minus"] = fan["supports"][(axis, -1)]
        values[f"axis{axis}_area_plus"] = fan["areas"][(axis, 1)]
        values[f"axis{axis}_area_minus"] = fan["areas"][(axis, -1)]
        values[f"axis{axis}_total_excess"] = fan["allocations"][axis]["total_excess"]
        values[f"axis{axis}_depth_plus"] = fan["allocations"][axis]["depth_plus"]
        values[f"axis{axis}_depth_minus"] = fan["allocations"][axis]["depth_minus"]
        values[f"axis{axis}_allocation_left"] = fan["allocations"][axis]["left"]
        values[f"axis{axis}_allocation_right"] = fan["allocations"][axis]["right"]
        values[f"axis{axis}_cap_lower"] = fan["allocations"][axis]["lower"]
    write_audit_constants(values, write)

    cap_pairs: list[dict[str, Any]] = []
    for axis in range(3):
        allocation = fan["allocations"][axis]
        cap_pairs.append(
            {
                "axis": axis,
                "coordinate_width_squared_lower": fs(allocation["coordinate_width_squared_lower"]),
                "coordinate_width_lower": fs(allocation["coordinate_width_lower"]),
                "support_plus": fs(fan["supports"][(axis, 1)]),
                "support_minus": fs(fan["supports"][(axis, -1)]),
                "base_plus": fs(P.BASES[(axis, 1)]),
                "base_minus": fs(P.BASES[(axis, -1)]),
                "section_hull_sizes": [
                    len(fan["hulls"][(axis, 1)]),
                    len(fan["hulls"][(axis, -1)]),
                ],
                "section_area_plus": fs(fan["areas"][(axis, 1)]),
                "section_area_minus": fs(fan["areas"][(axis, -1)]),
                "depth_plus_upper": fs(allocation["depth_plus"]),
                "depth_minus_upper": fs(allocation["depth_minus"]),
                "total_excess_lower": fs(allocation["total_excess"]),
                "allocation_bracket": [fs(allocation["left"]), fs(allocation["right"])],
                "derivative_left": fs(allocation["derivative_left"]),
                "derivative_right": fs(allocation["derivative_right"]),
                "pair_cap_lower": fs(allocation["lower"]),
                "pair_cap_lower_decimal": dec(allocation["lower"], 55),
            }
        )

    cert: dict[str, Any] = {
        "schema": SCHEMA,
        "status": "PROPOSED_EXACT_UNIVERSAL_CERTIFICATE_STANDALONE_REPLAY",
        "theorem": {
            "statement": (
                "Every convex body K in R^3 of constant width d>0 satisfies "
                "Vol(K) >= (26220940089713*pi/200000000000000)d^3."
            ),
            "coefficient_of_pi": fs(THEOREM_PI_COEFFICIENT),
            "coefficient_decimal_lower": dec(theorem_lo, 55),
            "coefficient_decimal_upper": dec(theorem_hi, 55),
            "strict_gain_over_previous_lower": dec(gain, 55),
        },
        "circumradius_partition": {
            "split": fs(R_SPLIT),
            "split_decimal": dec(R_SPLIT, 20),
            "lower_branch": ["1/2", fs(R_SPLIT)],
            "near_Jung_branch": [fs(R_SPLIT), "sqrt(6)/4"],
            "gap_free": True,
        },
        "lower_branch": {
            "reference_handoff_certificate_sha256": REFERENCE_CERT_SHA256,
            "rows": rows,
            "replaced_reference_row": "O3A1",
            "refined_angular_grid": {
                "angle_N": ROW_ANGLE_N,
                "radial_grid": ROW_GRID,
                "cells": len(refined_rows),
                "minimum_margin_over_O3B02": fs(refined_margin),
            },
            "weakest_row": "O3B02",
            "weakest_coefficient_of_pi": fs(THEOREM_PI_COEFFICIENT),
        },
        "near_Jung_branch": {
            "reference_fan_sha256": REFERENCE_FAN_SHA256,
            "adjusted_fan_sha256": FAN_DATA_SHA256,
            "fan_reconstruction": {
                "vertices": fan["vertex_count"],
                "faces": fan["face_count"],
                "edges": fan["edge_count"],
                "orbits": fan["orbit_count"],
                "minimum_cone_determinant": fan["minimum_cone_determinant"],
            },
            "changed_vertices_from_reference": fan["changed_vertices"],
            "minimum_radial_ratio": fs(fan["minimum_radial_ratio"]),
            "minimum_margin": fs(fan["minimum_margin"]),
            "minimum_margin_decimal": dec(fan["minimum_margin"], 55),
            "minimum_margin_index": fan["minimum_margin_index"],
            "reference_margin_regression": fs(fan["reference_margin_regression"]),
            "reference_margin_regression_index": fan["reference_margin_regression_index"],
            "active_set_census": fan["active_set_census"],
            "active_bound_census": fan["active_bound_census"],
            "sharp_total_deficiency_upper": fs(fan["E"]),
            "sharp_total_deficiency_upper_decimal": dec(fan["E"], 55),
            "determinant_sharpness": fan["determinant_census"],
            "determinant_squared_lower": fs(fan["determinant_squared_lower"]),
            "determinant_squared_lower_decimal": dec(fan["determinant_squared_lower"], 55),
            "reference_fan_coefficient": fs(fan["C"]),
            "reference_fan_coefficient_decimal": dec(fan["C"], 55),
            "core_volume_lower": fs(fan["core_volume_lower"]),
            "core_volume_lower_decimal": dec(fan["core_volume_lower"], 55),
            "coordinate_width_lemma": width_lemma,
            "cap_pairs": cap_pairs,
            "total_cap_lower": fs(fan["total_cap_lower"]),
            "total_cap_lower_decimal": dec(fan["total_cap_lower"], 55),
            "cross_axis_disjointness": {
                "center_coordinate_upper": fs(fan["center_coordinate_upper"]),
                "minimum_signed_support": fs(fan["minimum_signed_support"]),
                "overlap_norm_squared_lower": fs(fan["overlap_norm_squared_lower"]),
                "ellipsoid_radius_squared_upper": fs(fan["ellipsoid_radius_squared_upper"]),
                "strict_gap": fs(fan["cross_axis_gap"]),
                "strict_gap_decimal": dec(fan["cross_axis_gap"], 55),
            },
            "volume_lower": fs(fan["near_volume_lower"]),
            "volume_lower_decimal": dec(fan["near_volume_lower"], 55),
            "margin_over_theorem_upper": fs(near_margin),
            "margin_over_theorem_upper_decimal": dec(near_margin, 55),
        },
        "pi_bounds": {"lower": fs(pi_lo), "upper": fs(pi_hi)},
        "claim_boundary": {
            "certified_inside_package": [
                "Gap-free lower circumradius partition through O3B02.",
                "Four exact doubled-angular-grid cells replacing O3A1.",
                "Exact dominant-edge coordinate-width sharpening for all three coordinate axes.",
                "Exact adjusted 98,306-ray near-Jung fan at the split.",
                "Three separately optimized antipodal cap pairs and exact six-cap disjointness.",
                "Strict exact near-Jung handoff margin and gain over the predecessor certificate.",
            ],
            "not_established": [
                "External independent reproduction or peer review.",
                "Equality, rigidity, or sharpness.",
                "Identification of a minimizing body or Meissner extremality.",
                "The universal support-box inequality.",
            ],
        },
    }
    blob = (json.dumps(cert, indent=2, sort_keys=True) + "\n").encode("ascii")
    if write:
        CERT_PATH.write_bytes(blob)
    elif not CERT_PATH.exists() or CERT_PATH.read_bytes() != blob:
        raise RuntimeError("certificate JSON is not byte-identical")
    return cert


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    cert = build_certificate(write=args.write)
    near = cert["near_Jung_branch"]
    theorem = cert["theorem"]
    caps = near["cap_pairs"]
    print("MINVOL UNIVERSAL CONTACT-BOUND CERTIFICATE: EXACT")
    print(f"split radius:                  {cert['circumradius_partition']['split_decimal']}")
    print(f"weakest lower row:            {cert['lower_branch']['weakest_row']}")
    print(f"changed fan vertices:         {near['changed_vertices_from_reference']}")
    print(f"minimum exact fan margin:     {near['minimum_margin_decimal']}")
    print(f"sharp determinant squared:    {near['determinant_squared_lower_decimal']}")
    print(
        "coordinate width lowers:      "
        + "/".join(dec(Fraction(c["coordinate_width_lower"]), 18) for c in caps)
    )
    print(f"three-pair cap lower:         {near['total_cap_lower_decimal']}")
    print(f"cross-axis disjointness gap:  {near['cross_axis_disjointness']['strict_gap_decimal']}")
    print(f"near-Jung volume lower:       {near['volume_lower_decimal']}")
    print(f"near-Jung handoff margin:     {near['margin_over_theorem_upper_decimal']}")
    print(f"universal coefficient lower: {theorem['coefficient_decimal_lower']}")
    print(f"gain over previous lower:     {theorem['strict_gain_over_previous_lower']}")
    print("PROPOSED UNIVERSAL LOWER BOUND ABOVE 0.4118775: EXACTLY CERTIFIED BY THIS PACKAGE")


if __name__ == "__main__":
    main()
