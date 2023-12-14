"""Advent of Code 2023, Day 14."""

import collections

from typing import Dict, List, Tuple

Point = collections.namedtuple("Point", ("x y"))


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    result = get_load(tilt(puzzle_input))

    return result


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""


def get_load(rocks: List[str]) -> int:
    """Return the load on the platform."""

    n = 0
    m = len(rocks)

    for i, row in enumerate(rocks):
        n += row.count("O") * (m - i)

    return n


def tilt(rocks: List[str]) -> List[str]:
    """Tilt the platform north.

    All round rocks (0) move as far as they can in that direction until they
    encounter a square rock (#), a stationary round rock, or the platform edge.
    """

    # TODO: It would be more efficient to do this by column

    rocks = [list(row) for row in rocks]
    result = _tilt(rocks)

    return ["".join(row) for row in result]


def _tilt(rocks: List[List[str]]) -> List[List[str]]:
    old = rocks
    new = []

    rows = collections.deque(old)

    while True:
        a = rows.popleft()

        try:
            b = rows.popleft()
        except IndexError:
            new.append(a)
            break
        else:
            a, b = roll(a, b)
            new.append(a)
            rows.appendleft(b)

    if old == new:
        return new
    else:
        return _tilt(new)


def roll(old_p: List[List[str]], old_q: List[List[str]]) -> str:
    """Return the result of the rocks in b rolling towards a."""

    new_p = old_p[:]
    new_q = old_q[:]

    for i, (p, q) in enumerate(zip(old_p, old_q)):
        if (p, q) == (".", "O"):
            new_p[i] = q
            new_q[i] = "."
        else:
            new_p[i] = p
            new_q[i] = q

    return new_p, new_q
