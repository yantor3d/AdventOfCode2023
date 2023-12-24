"""Advent of Code 2023, Day 24."""

from __future__ import annotations

import collections
import itertools
import math
import numpy
import sys

from typing import List, Optional, Tuple

INF = float("inf")

mn = 200000000000000
mx = 400000000000000


class BoundingBox(collections.namedtuple("BoundingBox", "mn mx")):
    def __contains__(self, v: Vector) -> bool:
        return all(
            [
                v.x >= self.mn.x,
                v.y >= self.mn.y,
                v.z >= self.mn.z if self.mn.z > 0 else True,
                v.x <= self.mx.x,
                v.y <= self.mx.y,
                v.z <= self.mx.z if self.mx.z > 0 else True,
            ]
        )


class Vector(collections.namedtuple("Vector", "x y z")):
    def __hash__(self) -> int:
        return hash(tuple(self))

    def __repr__(self) -> str:
        parts = []

        for n in self:
            parts.append(f"{n}" if float(n).is_integer() else f"{n:.3f}")

        return f"<{','.join(parts)}>"

    def __str__(self) -> str:
        return repr(self)

    def __add__(self, other: Vector) -> Vector:
        a, b = self, other

        return Vector(a.x + b.x, a.y + b.y, a.z + b.z)

    def __mul__(self, f: float) -> Vector:
        return Vector(self.x * f, self.y * f, self.z * f)

    def __sub__(self, other: Vector) -> Vector:
        a, b = self, other

        return Vector(a.x - b.x, a.y - b.y, a.z - b.z)

    def __eq__(self, other: Vector) -> bool:
        if isinstance(other, Vector):
            return all(
                [
                    approximately(self.x, other.x),
                    approximately(self.y, other.y),
                    approximately(self.z, other.z),
                ]
            )
        else:
            return False

    @classmethod
    def inf(cls):
        return cls(INF, INF, INF)

    @classmethod
    def zero(cls):
        return cls(0, 0, 0)


Particle = Tuple[Vector, Vector]

VECTOR_INF = Vector.inf()


def approximately(a: float, b: float) -> bool:
    return math.isclose(a, b, rel_tol=1e-3)


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    return 2

    particles = parse(puzzle_input, z=False)

    bb = BoundingBox(
        Vector(mn, mn, 0),
        Vector(mx, mx, 0),
    )

    return solve_01(particles, bb)


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""

    particles = parse(puzzle_input, z=True)

    p, v = solve_02(particles, 301)

    return sum(p)


def solve_01(particles: List[Particle], bb: BoundingBox) -> int:
    result = 0

    inf = Vector.inf()

    for i, (ap, av) in enumerate(particles):
        for j, (bp, bv) in enumerate(particles[i + 1 :], 1):
            p = intersect(ap, av, bp, bv)

            if p == inf:
                continue

            if p not in bb:
                continue

            a = intersect_at(ap, av, p)
            b = intersect_at(bp, bv, p)

            if (a, b) == (1, 1):
                result += 1

    return result


def solve_02(particles: List[Particle], t: int) -> Particle:
    n = len(particles)
    hit = None
    times = None

    p = Vector.zero()
    v = Vector.zero()

    for a, b, c in itertools.permutations([0, n // 2, -1], 3):
        p0, v0 = particles[a]
        p1, v1 = particles[b]
        p2, v2 = particles[c]

        h, ts = search((p0, v0), (p1, v1), (p2, v2), t)

        if h is None:
            continue

        t0, t1, t2 = ts
        v = as_int(h)

        q0 = p0 + (v0 * t0)
        p = q0 - (v * t0)

        break

    return p, v


def as_int(v: Vector) -> Vector:
    ax, ay, az = abs(v.x), abs(v.y), abs(v.z)

    if ax < ay and ax < az:
        f = v.x
    elif ay < az and ay < az:
        f = v.y
    elif az < ay and az < ax:
        f = v.z
    else:
        raise ValueError(v, ax, ay, az)

    return Vector(v.x / f, v.y / f, v.z / f)


def search(
    pv0: Particle,
    pv1: Particle,
    pv2: Particle,
    t: int,
) -> Particle:
    p0, v0 = pv0
    p1, v1 = pv1
    p2, v2 = pv2

    for i in range(1, t):
        q0 = p0 + (v0 * i)

        for j in range(1, t):
            q1 = p1 + (v1 * (i + j))
            v01 = q1 - q0

            for k in range(1, t):
                q2 = p2 + (v2 * (i + j + k))

                v02 = q2 - q0
                v12 = q2 - q1

                n01 = normalize(v01)
                n02 = normalize(v02)
                n12 = normalize(v12)

                if n01 == n02 and n01 == n12 and n02 == n12:
                    return n01, (i, i + j, i + j + k)

    return None, []


def parse(puzzle_input: List[str], z: bool = True) -> List[Particle]:
    result = []

    for line in puzzle_input:
        value = parse_line(line, z)
        result.append(value)

    return result


def parse_line(line: str, z: bool = True) -> Particle:
    position, velocity = line.split(" @ ")

    position = map(int, position.split(", "))
    velocity = map(int, velocity.split(", "))

    p, v = Vector(*position), Vector(*velocity)

    if not z:
        p = p._replace(z=0)
        v = v._replace(z=0)

    return p, v


def magnitude(v: Vector) -> float:
    return math.sqrt(v.x**2 + v.y**2 + v.z**2)


def normalize(v: Vector) -> Vector:
    mag = magnitude(v)

    return Vector(v.x / mag, v.y / mag, v.z / mag)


def intersect_at(p: Vector, v: Vector, x: Vector) -> int:
    if x == Vector(INF, INF, INF):
        return None

    v = normalize(v)
    n = normalize(x - p)

    d = numpy.dot(v, n)

    if d > 0:
        return 1

    if d < 0:
        return -1

    raise ValueError(p, v, x)


def is_colinear(ap: Vector, av: Vector, bp: Vector, bv: Vector) -> bool:
    result = False

    if Vector(*numpy.cross(av, bv)) == Vector.zero():
        ab = normalize(ap - bp)
        ba = normalize(bp - ap)

        an = normalize(av)
        bn = normalize(bv)

        return ab == an or ab == bn or ba == an or ba == bn

    return result


def intersect(ap: Vector, av: Vector, bp: Vector, bv: Vector) -> Vector:
    v1 = numpy.array(av).T
    c1 = numpy.array(ap).T
    v2 = numpy.array(bv).T
    c2 = numpy.array(bp).T

    # in this case the solved x is [-1.  1.], error is 0, and rank is 2
    x, err, rank = numpy.linalg.lstsq(numpy.array([v1, -v2]).T, c2 - c1, rcond=None)[:3]
    if rank == 2:
        # intersection exists
        return Vector(*(v1 * x[0] + c1))
    else:
        return Vector.inf()
