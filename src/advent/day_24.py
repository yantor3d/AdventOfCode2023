"""Advent of Code 2023, Day 24."""

from __future__ import annotations

import collections
import math
import numpy
import itertools

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


Particle = Tuple[Vector, Vector]


def approximately(a: float, b: float) -> bool:
    return math.isclose(a, b, rel_tol=1e-3)


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    particles = parse(puzzle_input, z=False)

    bb = BoundingBox(
        Vector(mn, mn, 0),
        Vector(mx, mx, 0),
    )

    # 31910 too low

    return solve(particles, bb)


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""


def solve(particles: List[Particle], bb: BoundingBox) -> int:
    result = 0

    # print()

    inf = Vector.inf()

    print()

    for i, (ap, av) in enumerate(particles):
        for j, (bp, bv) in enumerate(particles[i + 1 :], 1):
            p = intersect_2d(ap, av, bp, bv)

            if p == inf:
                continue

            a = intersect_at(ap, av, p)
            b = intersect_at(bp, bv, p)

            if (a, b) == (1, 1) and p in bb:
                result += 1

    return result


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
    u = Vector(-n.x, -n.y, -n.z)

    d = numpy.dot(v, n)

    if d > 0:
        return 1

    if d < 0:
        return -1

    raise ValueError(p, v, x)


def intersect_2d(ap: Vector, av: Vector, bp: Vector, bv: Vector) -> Vector:
    a1 = (ap.x, ap.y)
    a2 = (ap.x + av.x, ap.y + av.y)

    b1 = (bp.x, bp.y)
    b2 = (bp.x + bv.x, bp.y + bv.y)

    # shamelessly 'borrowed' from StackOverflow
    s = numpy.vstack([a1, a2, b1, b2])  # s for stacked
    h = numpy.hstack((s, numpy.ones((4, 1))))  # h for homogeneous
    l1 = numpy.cross(h[0], h[1])  # get first line
    l2 = numpy.cross(h[2], h[3])  # get second line
    x, y, z = numpy.cross(l1, l2)  # point of intersection

    if z == 0:  # lines are parallel
        return Vector(float("inf"), float("inf"), float("inf"))
    else:
        return Vector(x / z, y / z, 0.0)
