"""Test suite for Day 24."""

import pytest
import math

import advent.day_24

from advent.day_24 import BoundingBox, Vector


@pytest.fixture
def puzzle_input():
    return [
        "19, 13, 30 @ -2,  1, -2",
        "18, 19, 22 @ -1, -1, -2",
        "20, 25, 34 @ -2, -2, -4",
        "12, 31, 28 @ -1, -2, -1",
        "20, 19, 15 @  1, -5, -3",
    ]


@pytest.fixture
def bb01():
    return BoundingBox(
        Vector(7, 7, 0),
        Vector(27, 27, 0),
    )


def test_parse(puzzle_input):
    particles = advent.day_24.parse(puzzle_input, z=True)

    assert particles == [
        (Vector(19, 13, 30), Vector(-2, 1, -2)),
        (Vector(18, 19, 22), Vector(-1, -1, -2)),
        (Vector(20, 25, 34), Vector(-2, -2, -4)),
        (Vector(12, 31, 28), Vector(-1, -2, -1)),
        (Vector(20, 19, 15), Vector(1, -5, -3)),
    ]

    particles = advent.day_24.parse(puzzle_input, z=False)

    assert particles[0] == ((Vector(19, 13, 0), Vector(-2, 1, 0)))


@pytest.mark.parametrize(
    "a,b,q",
    (
        (0, 1, Vector(14.333, 15.333, 0.0)),
        (0, 2, Vector(11.667, 16.667, 0.0)),
        (0, 3, Vector(6.2, 19.4, 0.0)),
        (1, 2, Vector.inf()),
        (1, 3, Vector(-6, -5, 0)),
        (2, 3, Vector(-2, 3, 0)),
    ),
)
def test_intersect_01(puzzle_input, a, b, q):
    particles = advent.day_24.parse(puzzle_input, z=False)

    ap, av = particles[a]
    bp, bv = particles[b]

    assert not advent.day_24.is_colinear(ap, av, bp, bv)

    p = advent.day_24.intersect(ap, av, bp, bv)

    assert p == q


@pytest.mark.parametrize(
    "ap,av,bp,bv,x",
    (
        [
            Vector(1, 0, 0),
            Vector(1, 0, 0),
            Vector(-1, 0, 0),
            Vector(1, 0, 0),
            True,
        ],
    ),
)
def test_is_colinear(ap, av, bp, bv, x):
    y = advent.day_24.is_colinear(ap, av, bp, bv)

    assert x == y


@pytest.mark.parametrize(
    "a,b,y",
    (
        (0, 1, (1, 1)),
        (0, 2, (1, 1)),
        (0, 3, (1, 1)),
        (0, 4, (-1, 1)),
        (1, 3, (1, 1)),
        (1, 4, (-1, -1)),
        (2, 3, (1, 1)),
        (2, 4, (1, -1)),
        (3, 4, (-1, -1)),
    ),
)
def test_when(puzzle_input, a, b, y):
    particles = advent.day_24.parse(puzzle_input, z=False)

    ap, av = particles[a]
    bp, bv = particles[b]

    p = advent.day_24.intersect(ap, av, bp, bv)
    x = (
        advent.day_24.intersect_at(ap, av, p),
        advent.day_24.intersect_at(bp, bv, p),
    )

    assert x == y


def test_part_01(puzzle_input, bb01):
    particles = advent.day_24.parse(puzzle_input, z=False)

    answer = advent.day_24.solve_01(particles, bb01)

    assert answer == 2


def test_part_02(puzzle_input):
    particles = advent.day_24.parse(puzzle_input, z=True)

    p, v = advent.day_24.solve_02(particles, t=10)

    assert p == Vector(24, 13, 10)
    assert v == Vector(-3, 1, 2)

    assert sum(p) == 47
