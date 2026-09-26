#!/usr/bin/env python3
"""Exact arithmetic primitives for the public MinVol contact-bound certificate.

This module contains only deterministic integer and Fraction arithmetic used by
``certify_universal_bound.py``. It has no repository-parent imports and no
network or floating-point proof dependencies.
"""
from __future__ import annotations

import hashlib
import itertools
from decimal import Decimal, getcontext
from fractions import Fraction
from math import comb, isqrt
from pathlib import Path
from typing import Any, Callable

N = 128
BITS = 52
DBITS = 60
BETA_DEN = 1 << 60
SIGNS = ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))
PAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
ALLOCATION_GRID = 10**20

BASES: dict[tuple[int, int], Fraction] = {
    (0, 1): Fraction(846_823, 625_000),
    (0, -1): Fraction(13_586_621, 10_000_000),
    (1, 1): Fraction(13_632_281, 10_000_000),
    (1, -1): Fraction(13_632_281, 10_000_000),
    (2, 1): Fraction(13_632_281, 10_000_000),
    (2, -1): Fraction(13_632_281, 10_000_000),
}

PI_TERMS = 180
SQRT_BITS = 500


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


def pi_bounds(terms: int = PI_TERMS) -> tuple[Fraction, Fraction]:
    partial = Fraction(0)
    for k in range(terms):
        partial += Fraction(comb(2 * k, k), (2 * k + 1) * 2 ** (4 * k + 1))
    first = Fraction(comb(2 * terms, terms), (2 * terms + 1) * 2 ** (4 * terms + 1))
    return 6 * partial, 6 * (partial + Fraction(4, 3) * first)


def sqrt_lower(x: Fraction, bits: int = SQRT_BITS) -> Fraction:
    if x < 0:
        raise ValueError("negative square root")
    scale = 1 << bits
    n = isqrt((x.numerator * scale * scale) // x.denominator)
    lo = Fraction(n, scale)
    if lo * lo > x or Fraction(n + 1, scale) ** 2 <= x:
        raise AssertionError("invalid square-root lower enclosure")
    return lo


def sqrt_upper(x: Fraction, bits: int = SQRT_BITS) -> Fraction:
    lo = sqrt_lower(x, bits)
    if lo * lo == x:
        return lo
    up = lo + Fraction(1, 1 << bits)
    if up * up <= x:
        raise AssertionError("invalid square-root upper enclosure")
    return up


def det3_int(a: tuple[int, int, int], b: tuple[int, int, int], c: tuple[int, int, int]) -> int:
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


def reconstruct_cube_fan() -> tuple[
    list[tuple[int, int, int]],
    list[tuple[int, int, int]],
    set[tuple[int, int]],
    dict[tuple[int, int, int], int],
]:
    """Reconstruct the immutable N=128 cubical spherical fan.

    Vertex insertion order is face-axis order x-,x+,y-,y+,z-,z+, with the
    two in-face coordinates increasing from -N to N in steps of two.  Each
    square uses the fixed lower-left to upper-right diagonal.  This exact
    reconstruction is checked against the immutable reference-fan volume numerator.
    """
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
    edges: set[tuple[int, int]] = set()
    for grid in grids:
        for i in range(N):
            for j in range(N):
                a = grid[i][j]
                b = grid[i + 1][j]
                c = grid[i + 1][j + 1]
                d = grid[i][j + 1]
                for tri0 in ((a, b, c), (a, c, d)):
                    tri = tri0
                    if det3_int(qvec[tri[0]], qvec[tri[1]], qvec[tri[2]]) < 0:
                        tri = (tri[0], tri[2], tri[1])
                    if det3_int(qvec[tri[0]], qvec[tri[1]], qvec[tri[2]]) <= 0:
                        raise AssertionError("nonpositive reconstructed cone determinant")
                    faces.append(tri)
                    for x, y in ((tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])):
                        edges.add(tuple(sorted((x, y))))

    if len(qvec) != 98_306 or len(faces) != 196_608 or len(edges) != 294_912:
        raise AssertionError("reconstructed fan census mismatch")
    if len(qvec) - len(edges) + len(faces) != 2:
        raise AssertionError("reconstructed fan Euler characteristic mismatch")
    return qvec, faces, edges, index


def stabilizer_orbits(
    qvec: list[tuple[int, int, int]], index: dict[tuple[int, int, int], int]
) -> list[list[int]]:
    transforms: tuple[Callable[[tuple[int, int, int]], tuple[int, int, int]], ...] = (
        lambda q: q,
        lambda q: (q[0], q[2], q[1]),
        lambda q: (q[0], -q[1], -q[2]),
        lambda q: (q[0], -q[2], -q[1]),
    )
    seen: set[int] = set()
    out: list[list[int]] = []
    for i, q in enumerate(qvec):
        if i in seen:
            continue
        orbit = sorted({index[t(q)] for t in transforms})
        out.append(orbit)
        seen.update(orbit)
    if len(out) != 24_833 or len(seen) != len(qvec):
        raise AssertionError("edge-stabilizer orbit census mismatch")
    return out


def beta_numerators(q: tuple[int, int, int], radial: int) -> list[int]:
    return [
        (1 << 58) + radial * sum(SIGNS[k][j] * q[j] for j in range(3))
        for k in range(4)
    ]


def dominant_lower(c: list[Fraction], E: Fraction) -> Fraction:
    negative = sorted([j for j in range(1, 6) if c[j] < 0], key=lambda j: c[j])
    candidates = [Fraction(0), E] + [E / (k + 1) for k in range(1, len(negative) + 1)]
    best: Fraction | None = None
    for t in candidates:
        budget = max(Fraction(0), E - t)
        value = c[0] * t
        for j in negative:
            amount = min(t, budget)
            value += c[j] * amount
            budget -= amount
            if budget <= 0:
                break
        best = value if best is None or value < best else best
    if best is None:
        raise AssertionError("empty dominant-bound candidate set")
    return best


def exact_margin(
    q: tuple[int, int, int], radial: int, delta: int, E: Fraction
) -> tuple[Fraction | None, str, int]:
    beta = beta_numerators(q, radial)
    negative = [x < 0 for x in beta]
    nneg = sum(negative)
    if nneg == 0:
        return None, "convex", 0
    mu = [
        0 if negative[k] else beta[k] + (delta if nneg == 2 else 0)
        for k in range(4)
    ]
    total = sum(mu)
    remainder = total - BETA_DEN
    if remainder <= 0:
        raise AssertionError("nonpositive S-procedure remainder")
    z = [beta[k] - mu[k] for k in range(4)]
    c: list[Fraction] = []
    for i, j in PAIRS:
        c.append(
            -Fraction(2 * beta[i] * beta[j], BETA_DEN * BETA_DEN)
            - Fraction(2 * z[i] * z[j], BETA_DEN * remainder)
        )
    regular = Fraction(1) - Fraction(total, BETA_DEN) - sum(c, Fraction(0)) / 2
    edge = min(Fraction(0), min(c)) * E
    dominant = dominant_lower(c, E)
    if edge > dominant:
        active, correction = "edge", edge
    elif dominant > edge:
        active, correction = "dominant", dominant
    else:
        active, correction = "tie", edge
    return regular + correction / 2, active, nneg


# Minimal polynomial algebra for the inherited sharp determinant theorem.
Monomial = tuple[int, ...]
Polynomial = dict[Monomial, Fraction]
ZERO_MON = (0, 0, 0, 0, 0, 0)


def pconst(x: Fraction | int) -> Polynomial:
    x = Fraction(x)
    return {} if x == 0 else {ZERO_MON: x}


def pvar(i: int) -> Polynomial:
    m = [0] * 6
    m[i] = 1
    return {tuple(m): Fraction(1)}


def padd(a: Polynomial, b: Polynomial) -> Polynomial:
    out = dict(a)
    for mon, val in b.items():
        out[mon] = out.get(mon, Fraction(0)) + val
        if out[mon] == 0:
            del out[mon]
    return out


def pneg(a: Polynomial) -> Polynomial:
    return {mon: -val for mon, val in a.items()}


def psub(a: Polynomial, b: Polynomial) -> Polynomial:
    return padd(a, pneg(b))


def pmul(a: Polynomial, b: Polynomial) -> Polynomial:
    out: Polynomial = {}
    for ma, va in a.items():
        for mb, vb in b.items():
            mon = tuple(ma[i] + mb[i] for i in range(6))
            out[mon] = out.get(mon, Fraction(0)) + va * vb
    return {mon: val for mon, val in out.items() if val}


def pscale(a: Polynomial, c: Fraction | int) -> Polynomial:
    c = Fraction(c)
    return {mon: c * val for mon, val in a.items() if c * val}


def determinant_sharp_census() -> dict[str, Any]:
    e = [pvar(i) for i in range(6)]
    s = [psub(pconst(1), e[i]) for i in range(6)]
    s12, s13, s14, s23, s24, s34 = s
    half = Fraction(1, 2)
    m11, m22, m33 = s14, s24, s34
    m12 = pscale(padd(padd(s14, s24), pneg(s12)), half)
    m13 = pscale(padd(padd(s14, s34), pneg(s13)), half)
    m23 = pscale(padd(padd(s24, s34), pneg(s23)), half)
    det = padd(
        psub(
            pmul(m11, psub(pmul(m22, m33), pmul(m23, m23))),
            pmul(m12, psub(pmul(m12, m33), pmul(m23, m13))),
        ),
        pmul(m13, psub(pmul(m12, m23), pmul(m22, m13))),
    )
    ratio = pscale(det, 2)
    S: Polynomial = {}
    for v in e:
        S = padd(S, v)
    target = padd(psub(pconst(1), pscale(S, half)), pneg(pscale(pmul(S, S), half)))
    diff = psub(ratio, target)
    quadratic = [(mon, c) for mon, c in diff.items() if sum(mon) == 2]
    positive_cubic = [(mon, c) for mon, c in diff.items() if sum(mon) == 3 and c > 0]
    negative_cubic = [(mon, c) for mon, c in diff.items() if sum(mon) == 3 and c < 0]
    if len(quadratic) != 15 or any(c < 1 for _, c in quadratic):
        raise AssertionError("determinant quadratic census failed")
    if len(negative_cubic) != 12 or any(c != Fraction(-1, 2) for _, c in negative_cubic):
        raise AssertionError("determinant negative-cubic census failed")
    pair_counts = {pair: 0 for pair in itertools.combinations(range(6), 2)}
    for mon, _ in negative_cubic:
        support = [i for i, power in enumerate(mon) if power]
        for pair in itertools.combinations(support, 2):
            pair_counts[pair] += 1
    if max(pair_counts.values()) != 4:
        raise AssertionError("determinant pair-incidence census failed")
    return {
        "ratio_term_count": len(ratio),
        "difference_quadratic_count": len(quadratic),
        "minimum_quadratic_pair_coefficient": fs(min(c for _, c in quadratic)),
        "negative_cubic_count": len(negative_cubic),
        "negative_cubic_coefficient": "-1/2",
        "maximum_negative_cubic_pair_incidence": max(pair_counts.values()),
        "positive_cubic_count": len(positive_cubic),
    }


def cross2(
    o: tuple[Fraction, Fraction],
    a: tuple[Fraction, Fraction],
    b: tuple[Fraction, Fraction],
) -> Fraction:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_hull(points: set[tuple[Fraction, Fraction]]) -> list[tuple[Fraction, Fraction]]:
    pts = sorted(points)
    lower: list[tuple[Fraction, Fraction]] = []
    for p in pts:
        while len(lower) >= 2 and cross2(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper: list[tuple[Fraction, Fraction]] = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross2(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    hull = lower[:-1] + upper[:-1]
    if len(hull) < 3:
        raise AssertionError("degenerate section hull")
    return hull


def section_hull(
    coords: list[tuple[Fraction, Fraction, Fraction]],
    edges: set[tuple[int, int]],
    axis: int,
    sign: int,
    base: Fraction,
) -> list[tuple[Fraction, Fraction]]:
    target = sign * base
    other = [j for j in range(3) if j != axis]
    points: set[tuple[Fraction, Fraction]] = set()
    for i, j in edges:
        x1, x2 = coords[i][axis], coords[j][axis]
        if x1 == target:
            points.add((coords[i][other[0]], coords[i][other[1]]))
        if x2 == target:
            points.add((coords[j][other[0]], coords[j][other[1]]))
        if (x1 < target < x2) or (x2 < target < x1):
            t = (target - x1) / (x2 - x1)
            points.add(
                (
                    coords[i][other[0]] + t * (coords[j][other[0]] - coords[i][other[0]]),
                    coords[i][other[1]] + t * (coords[j][other[1]] - coords[i][other[1]]),
                )
            )
    return convex_hull(points)


def polygon_area(hull: list[tuple[Fraction, Fraction]]) -> Fraction:
    twice = sum(
        hull[i][0] * hull[(i + 1) % len(hull)][1]
        - hull[i][1] * hull[(i + 1) % len(hull)][0]
        for i in range(len(hull))
    )
    if twice == 0:
        raise AssertionError("zero section area")
    return abs(twice) / 2


def cap_profile(area: Fraction, depth: Fraction, extension: Fraction) -> Fraction:
    return area * extension**3 / (24 * (depth + extension) ** 2)


def cap_derivative(area: Fraction, depth: Fraction, extension: Fraction) -> Fraction:
    return area * extension**2 * (3 * depth + extension) / (24 * (depth + extension) ** 3)


def allocation_certificate(
    area_plus: Fraction,
    depth_plus: Fraction,
    area_minus: Fraction,
    depth_minus: Fraction,
    total_excess: Fraction,
    determinant_lower: Fraction,
) -> dict[str, Fraction]:
    def derivative(t: Fraction) -> Fraction:
        return cap_derivative(area_plus, depth_plus, t) - cap_derivative(
            area_minus, depth_minus, total_excess - t
        )

    if not derivative(Fraction(0)) < 0 < derivative(total_excess):
        raise AssertionError("allocation endpoint derivative signs failed")
    lo, hi = Fraction(0), total_excess
    for _ in range(250):
        mid = (lo + hi) / 2
        if derivative(mid) < 0:
            lo = mid
        else:
            hi = mid
    left = Fraction((lo.numerator * ALLOCATION_GRID) // lo.denominator, ALLOCATION_GRID)
    right = left + Fraction(1, ALLOCATION_GRID)
    while derivative(left) >= 0:
        left -= Fraction(1, ALLOCATION_GRID)
    while derivative(right) <= 0:
        right += Fraction(1, ALLOCATION_GRID)
    if not (0 <= left < right <= total_excess and derivative(left) < 0 < derivative(right)):
        raise AssertionError("allocation rational bracket failed")

    # The unique minimizer t* lies in [left,right].  Since each profile is
    # increasing, phi_+(t*) >= phi_+(left) and
    # phi_-(T-t*) >= phi_-(T-right).
    lower = determinant_lower * (
        cap_profile(area_plus, depth_plus, left)
        + cap_profile(area_minus, depth_minus, total_excess - right)
    )
    return {
        "left": left,
        "right": right,
        "derivative_left": derivative(left),
        "derivative_right": derivative(right),
        "lower": lower,
    }
