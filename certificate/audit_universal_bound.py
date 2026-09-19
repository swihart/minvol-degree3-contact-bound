#!/usr/bin/env python3
"""Independent binary64 audit for the public universal contact-bound certificate."""
from __future__ import annotations

import csv
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REFERENCE_FAN = HERE / "certificates" / "reference_near_jung_fan.npz"
FAN = HERE / "certificates" / "universal_contact_fan.npz"
HULLS = HERE / "certificates" / "all_axis_pair_section_hulls.tsv"
CERT = HERE / "certificates" / "universal_contact_bound_certificate.json"
ROW_FILES = [HERE / "certificates" / f"refined_lower_cell_{i}.npz" for i in range(1, 5)]

N = 128
BITS = 52
SIGNS = np.array(((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)), dtype=np.float64)
PAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
BETA_DEN = float(1 << 60)


def reconstruct_cube_fan() -> tuple[np.ndarray, np.ndarray]:
    vals = list(range(-N, N + 1, 2))
    qvec: list[tuple[int, int, int]] = []
    index: dict[tuple[int, int, int], int] = {}
    grids: list[list[list[int]]] = []
    for axis in range(3):
        for sign in (-1, 1):
            other = [j for j in range(3) if j != axis]
            grid: list[list[int]] = []
            for u in vals:
                row: list[int] = []
                for v in vals:
                    q = [0, 0, 0]
                    q[axis] = sign * N
                    q[other[0]] = u
                    q[other[1]] = v
                    qt = tuple(q)
                    if qt not in index:
                        index[qt] = len(qvec)
                        qvec.append(qt)
                    row.append(index[qt])
                grid.append(row)
            grids.append(grid)
    faces: list[tuple[int, int, int]] = []
    for grid in grids:
        for i in range(N):
            for j in range(N):
                a, b, c, d = grid[i][j], grid[i + 1][j], grid[i + 1][j + 1], grid[i][j + 1]
                for tri in ((a, b, c), (a, c, d)):
                    qa, qb, qc = qvec[tri[0]], qvec[tri[1]], qvec[tri[2]]
                    determinant = (
                        qa[0] * (qb[1] * qc[2] - qb[2] * qc[1])
                        - qa[1] * (qb[0] * qc[2] - qb[2] * qc[0])
                        + qa[2] * (qb[0] * qc[1] - qb[1] * qc[0])
                    )
                    if determinant < 0:
                        tri = (tri[0], tri[2], tri[1])
                    faces.append(tri)
    return np.asarray(qvec, dtype=np.float64), np.asarray(faces, dtype=np.int64)


def dominant_lower(c: np.ndarray, E: float) -> float:
    negative = sorted([j for j in range(1, 6) if c[j] < 0.0], key=lambda j: c[j])
    best = math.inf
    for t in [0.0, E] + [E / (k + 1) for k in range(1, len(negative) + 1)]:
        budget = max(0.0, E - t)
        value = c[0] * t
        for j in negative:
            amount = min(t, budget)
            value += c[j] * amount
            budget -= amount
            if budget <= 0.0:
                break
        best = min(best, value)
    return best


def margin_binary64(ray: np.ndarray, radial: float, delta: float, E: float) -> tuple[float | None, str]:
    beta = (1 << 58) + radial * (SIGNS @ ray)
    negative = beta < 0.0
    nneg = int(np.sum(negative))
    if nneg == 0:
        return None, "convex"
    mu = np.where(negative, 0.0, beta + (delta if nneg == 2 else 0.0))
    total = float(np.sum(mu))
    remainder = total - BETA_DEN
    z = beta - mu
    c = np.empty(6, dtype=np.float64)
    for k, (i, j) in enumerate(PAIRS):
        c[k] = -2.0 * beta[i] * beta[j] / BETA_DEN**2 - 2.0 * z[i] * z[j] / (BETA_DEN * remainder)
    regular = 1.0 - total / BETA_DEN - 0.5 * float(np.sum(c))
    edge = min(0.0, float(np.min(c))) * E
    dominant = dominant_lower(c, E)
    if edge > dominant:
        return regular + 0.5 * edge, "edge"
    if dominant > edge:
        return regular + 0.5 * dominant, "dominant"
    return regular + 0.5 * edge, "tie"


def polygon_area(points: list[tuple[float, float]]) -> float:
    return abs(
        sum(
            points[i][0] * points[(i + 1) % len(points)][1]
            - points[i][1] * points[(i + 1) % len(points)][0]
            for i in range(len(points))
        )
    ) / 2.0


def profile(area: float, depth: float, extension: float) -> float:
    return area * extension**3 / (24.0 * (depth + extension) ** 2)


def profile_derivative(area: float, depth: float, extension: float) -> float:
    return area * extension**2 * (3.0 * depth + extension) / (24.0 * (depth + extension) ** 3)


def optimize_pair(area_plus: float, depth_plus: float, area_minus: float, depth_minus: float, total: float, determinant: float) -> float:
    lo, hi = 0.0, total
    for _ in range(100):
        mid = (lo + hi) / 2.0
        derivative = profile_derivative(area_plus, depth_plus, mid) - profile_derivative(
            area_minus, depth_minus, total - mid
        )
        if derivative < 0.0:
            lo = mid
        else:
            hi = mid
    tplus = (lo + hi) / 2.0
    return determinant * (
        profile(area_plus, depth_plus, tplus)
        + profile(area_minus, depth_minus, total - tplus)
    )


def angle(k: int, angular_n: int) -> tuple[float, float]:
    t = k / angular_n
    return (1.0 - t * t) / (1.0 + t * t), 2.0 * t / (1.0 + t * t)


def audit_refined_row(path: Path) -> tuple[float, float, int, int, float]:
    data = np.load(path, allow_pickle=False)
    rlo = float(data["rlo_num"]) / float(data["rlo_den"])
    rhi = float(data["rhi_num"]) / float(data["rhi_den"])
    s0 = float(data["s0_num"]) / float(data["s0_den"])
    archived = float(data["coef_num"]) / float(data["coef_den"])
    angular_n = int(data["N"])
    grid = float(data["grid"])
    ws = np.asarray(data["w_num"], dtype=np.float64) / grid
    zs = np.asarray(data["z_num"], dtype=np.float64) / grid
    m = 1.0 - rhi * rhi
    a = 2.0 * (s0 * s0 + 3.0 * m) / (3.0 * (s0 * s0 + m) ** 2)
    b = 2.0 * s0**3 / (s0 * s0 + m) - a * s0**3

    min_step_gap = math.inf
    for k in range(1, len(ws)):
        c0, s_0 = angle(k - 1, angular_n)
        c1, s1 = angle(k, angular_n)
        cd = c1 * c0 + s1 * s_0
        sd = s1 * c0 - c1 * s_0
        X, Y = ws[k], ws[k - 1]
        T = X * X + m
        D = 4.0 * X * X - T * T
        lhs = T * T * (Y * cd - X) ** 2
        rhs = Y * Y * D * sd * sd
        scale = max(1.0, abs(lhs), abs(rhs))
        min_step_gap = min(min_step_gap, (lhs - rhs) / scale)
        if not (D >= -1e-15 and T * (Y * cd - X) > -1e-15 and lhs + 2e-14 * scale >= rhs):
            raise RuntimeError("binary64 refined positive-step audit failed")

    min_ball_gap = math.inf
    for k, z in enumerate(zs, 1):
        c, s = angle(k, angular_n)
        lhs = (z + rlo * c) ** 2
        rhs = 1.0 - rlo * rlo * s * s
        min_ball_gap = min(min_ball_gap, lhs - rhs)
        if not (z <= s0 + 1e-14 and z + rlo * c >= -1e-14 and lhs + 2e-14 >= rhs):
            raise RuntimeError("binary64 refined antipodal-step audit failed")

    acc = 0.0
    for k in range(1, len(ws)):
        c0, _ = angle(k - 1, angular_n)
        c1, _ = angle(k, angular_n)
        s = ws[k]
        gap = a * s**3 + b - 2.0 * s**3 / (s * s + m)
        acc += (c0 - c1) * gap
    for k, z in enumerate(zs, 1):
        c0, _ = angle(k - 1, angular_n)
        c1, _ = angle(k, angular_n)
        gap = a * z**3 + b - 2.0 * z**3 / (z * z + m)
        acc += (c0 - c1) * gap
    coefficient = (2.0 / 3.0 - 4.0 * b + 8.0 * acc) / (3.0 * a - 2.0)
    if abs(coefficient - archived) > 8e-12:
        raise RuntimeError("binary64 refined-row coefficient reconstruction failed")
    return coefficient, archived, len(ws) - 1, len(zs), min(min_step_gap, min_ball_gap)


def run_audit() -> dict[str, float | int]:
    cert = json.loads(CERT.read_text())
    theorem_pi = float(Fraction(cert["theorem"]["coefficient_of_pi"]))
    row_results = [audit_refined_row(path) for path in ROW_FILES]
    min_row = min(result[0] for result in row_results)
    if not min_row > theorem_pi + 1.0e-5:
        raise RuntimeError("binary64 refined rows do not clear O3B02")

    reference = np.load(REFERENCE_FAN, allow_pickle=False)
    fan = np.load(FAN, allow_pickle=False)
    Q, F = reconstruct_cube_fan()
    A = np.asarray(fan["Aint"], dtype=np.float64)
    delta = np.asarray(fan["delta_num"], dtype=np.float64)
    reference_A = np.asarray(reference["Aint"], dtype=np.float64)
    R = float(fan["R_num"]) / float(fan["R_den"])
    q = R * R
    E = (3.0 - 8.0 * q) / (4.0 * q - 1.0)

    minimum = math.inf
    active = {"edge": 0, "dominant": 0, "tie": 0, "convex": 0}
    for i in range(len(Q)):
        margin, which = margin_binary64(Q[i], A[i], delta[i], E)
        active[which] += 1
        if margin is not None:
            minimum = min(minimum, margin)
    if not minimum > 1.8e-12:
        raise RuntimeError("binary64 fan margin is too small")

    qa, qb, qc = Q[F[:, 0]], Q[F[:, 1]], Q[F[:, 2]]
    determinants = np.einsum("ij,ij->i", qa, np.cross(qb, qc))
    raw = np.sum(A[F[:, 0]] * A[F[:, 1]] * A[F[:, 2]] * determinants)
    C = raw / (2.0 * 6.0 * N**3 * float(1 << BITS) ** 3)
    coords = A[:, None] * Q / float((1 << 51) * N)
    supports = {(axis, 1): float(np.max(coords[:, axis])) for axis in range(3)}
    supports.update({(axis, -1): float(np.max(-coords[:, axis])) for axis in range(3)})

    hulls: dict[tuple[int, int], list[tuple[float, float]]] = {}
    with HULLS.open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            key = (int(row["axis"]), int(row["sign"]))
            hulls.setdefault(key, []).append(
                (
                    float(int(row["u_num"]) / int(row["u_den"])),
                    float(int(row["v_num"]) / int(row["v_den"])),
                )
            )
    areas = {key: polygon_area(points) for key, points in hulls.items()}

    det_sq = 1.0 - E / 2.0 - E * E / 2.0
    det = math.sqrt(det_sq)
    core = C * math.sqrt(det_sq / 2.0)
    # Dominant-edge coordinate-width sharpening.  In the exact atlas e01 is
    # the largest deficiency.  The normalized Gram diagonal satisfies
    # H00 <= 1+E/2 and H11,H22 <= 1+E/6.  Since
    # (H^{-1})jj >= 1/Hjj, the normalized transformed coordinate widths
    # are bounded below by the following three values.
    g = {
        0: 1.0 / math.sqrt(1.0 + E / 2.0),
        1: 1.0 / math.sqrt(1.0 + E / 6.0),
        2: 1.0 / math.sqrt(1.0 + E / 6.0),
    }

    # Independently solve the three diagonal linear programs over the
    # dominant-edge simplex.  Its vertices have e01 and an arbitrary subset
    # of the other deficiencies tied at E/(k+1), with all remaining entries
    # zero.  Enumerating all 32 subsets recovers the sharp diagonal maxima.
    diagonal_twice_offsets = np.array(
        (
            (1.0, -1.0, -1.0, -1.0, -1.0, 1.0),
            (-1.0, 1.0, -1.0, -1.0, 1.0, -1.0),
            (-1.0, -1.0, 1.0, 1.0, -1.0, -1.0),
        )
    )
    diagonal_maxima = np.full(3, -math.inf)
    for mask in range(1 << 5):
        tied = [j + 1 for j in range(5) if mask & (1 << j)]
        e = np.zeros(6, dtype=np.float64)
        e[[0, *tied]] = E / (1 + len(tied))
        diagonal = 1.0 + 0.5 * (diagonal_twice_offsets @ e)
        diagonal_maxima = np.maximum(diagonal_maxima, diagonal)
    expected_diagonal_maxima = np.array((1.0 + E / 2.0, 1.0 + E / 6.0, 1.0 + E / 6.0))
    if not np.allclose(diagonal_maxima, expected_diagonal_maxima, rtol=0.0, atol=3e-15):
        raise RuntimeError("binary64 coordinate-width linear programs failed")

    cap_total = 0.0
    pair_values: list[float] = []
    sqrt2 = math.sqrt(2.0)
    for pair in cert["near_Jung_branch"]["cap_pairs"]:
        axis = int(pair["axis"])
        bplus = float(Fraction(pair["base_plus"]))
        bminus = float(Fraction(pair["base_minus"]))
        total = g[axis] - (supports[(axis, 1)] + supports[(axis, -1)]) / (2.0 * sqrt2)
        dplus = (supports[(axis, 1)] - bplus) / (2.0 * sqrt2)
        dminus = (supports[(axis, -1)] - bminus) / (2.0 * sqrt2)
        value = optimize_pair(areas[(axis, 1)], dplus, areas[(axis, -1)], dminus, total, det)
        pair_values.append(value)
        cap_total += value
        archived = float(Fraction(pair["pair_cap_lower"]))
        if value + 5.0e-18 < archived:
            raise RuntimeError(f"axis {axis} cap audit fell below exact lower bound")

    near = core + cap_total
    cmax = 3.0 - 8.0 * q
    hmin = min(supports.values())
    cross_gap = 2.0 * (hmin - cmax) ** 2 - 3.0 / (1.0 - E)
    if not cross_gap > 0.6:
        raise RuntimeError("binary64 cross-axis disjointness failed")

    theorem = theorem_pi * math.pi
    previous = 131_098_268_771_713 / 1_000_000_000_000_000 * math.pi
    if not near > theorem > previous:
        raise RuntimeError("binary64 universal assembly ordering failed")
    changed = int(np.sum(A < reference_A))
    if changed != int(cert["near_Jung_branch"]["changed_vertices_from_reference"]):
        raise RuntimeError("changed-vertex census mismatch")

    return {
        "refined_rows": len(row_results),
        "minimum_refined_row": min_row,
        "minimum_refined_row_margin": min_row - theorem_pi,
        "minimum_refined_step_gap": min(result[4] for result in row_results),
        "fan_vertices": len(Q),
        "changed_vertices": changed,
        "minimum_fan_margin": minimum,
        "dominant_active": active["dominant"],
        "tie_active": active["tie"],
        "reference_fan_coefficient": C,
        "sharp_determinant_squared": det_sq,
        "core_volume_lower": core,
        "axis0_gram_diagonal_maximum": float(diagonal_maxima[0]),
        "axis1_gram_diagonal_maximum": float(diagonal_maxima[1]),
        "axis2_gram_diagonal_maximum": float(diagonal_maxima[2]),
        "axis0_coordinate_width": g[0],
        "axis1_coordinate_width": g[1],
        "axis2_coordinate_width": g[2],
        "axis0_cap": pair_values[0],
        "axis1_cap": pair_values[1],
        "axis2_cap": pair_values[2],
        "total_cap_lower": cap_total,
        "cross_axis_gap": cross_gap,
        "near_jung_lower": near,
        "universal_coefficient": theorem,
        "gain_over_previous": theorem - previous,
    }


def main() -> int:
    out = run_audit()
    print(f"refined O3A1 rows:          {out['refined_rows']}")
    print(f"minimum refined row coeff:     {out['minimum_refined_row']:.15f}")
    print(f"refined row coeff margin:      {out['minimum_refined_row_margin']:.3e}")
    print(f"minimum row inequality gap:    {out['minimum_refined_step_gap']:.3e}")
    print(f"fan vertices:                  {out['fan_vertices']}")
    print(f"changed fan vertices:          {out['changed_vertices']}")
    print(f"minimum binary64 fan margin:   {out['minimum_fan_margin']:.15e}")
    print(f"dominant/tie active rays:      {out['dominant_active']}/{out['tie_active']}")
    print(f"reference fan coefficient:     {out['reference_fan_coefficient']:.15f}")
    print(f"sharp determinant squared:     {out['sharp_determinant_squared']:.15f}")
    print(f"core volume lower:             {out['core_volume_lower']:.15f}")
    print(f"coordinate width lowers:       {out['axis0_coordinate_width']:.15f}/{out['axis1_coordinate_width']:.15f}/{out['axis2_coordinate_width']:.15f}")
    print(f"axis cap lowers:               {out['axis0_cap']:.15f}/{out['axis1_cap']:.15f}/{out['axis2_cap']:.15f}")
    print(f"three-pair cap lower:          {out['total_cap_lower']:.15f}")
    print(f"cross-axis gap:                {out['cross_axis_gap']:.15f}")
    print(f"near-Jung lower:               {out['near_jung_lower']:.15f}")
    print(f"universal coefficient:         {out['universal_coefficient']:.15f}")
    print(f"gain over previous:            {out['gain_over_previous']:.15e}")
    print("MINVOL UNIVERSAL CONTACT-BOUND BINARY64 AUDIT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
