"""Advent of Code 2023, Day 14."""

import math
import collections
import functools
import itertools

from typing import Dict, List, Tuple

Point = collections.namedtuple("Point", ("x y"))


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    grid = unpack(puzzle_input)
    grid = tilt_n(grid)

    return get_load(grid)


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""

    grid = unpack(puzzle_input)

    grids = dict()
    loads = dict()

    start, end = None, None
    n = 1000000000

    for i in range(1, n + 1):
        grid = spin(grid)
        loads[i] = get_load(grid)

        if grid in grids:
            if start is None:
                start = grids[grid]

            if end is None:
                end = i - 1
                break
        else:
            grids[grid] = i

    d = end - start + 1
    f = (n - end) // d

    r = start + (n - (end + (f * d) + 1))

    # Brute force answer check
    # x = start
    # while x < n:
    #     x += d
    # s = end - (x - n) + 1

    # print(s)
    # print(r)

    return loads[r]


def get_load(grid: List[str]) -> int:
    """Return the load on the platform."""

    n = 0
    m = len(grid)

    for i, row in enumerate(grid):
        n += row.count("O") * (m - i)

    return n


def unpack(grid: List[str]) -> List[List[str]]:
    return tuple([tuple(row) for row in grid])


def repack(grid: List[List[str]]) -> List[str]:
    return ["".join(row) for row in grid]


@functools.cache
def spin(grid: List[List[str]]) -> List[List[str]]:
    grid = tilt_n(grid)
    grid = tilt_w(grid)
    grid = tilt_s(grid)
    grid = tilt_e(grid)

    return grid


@functools.cache
def tilt_n(grid: List[List[str]]) -> List[List[str]]:
    grid = rotate_ccw(grid)
    grid = roll_all(grid)
    grid = rotate_cw(grid)

    return grid


@functools.cache
def tilt_e(grid: List[List[str]]) -> List[List[str]]:
    grid = mirror_h(grid)
    grid = roll_all(grid)
    grid = mirror_h(grid)

    return grid


@functools.cache
def tilt_s(grid: List[List[str]]) -> List[List[str]]:
    grid = mirror_v(grid)
    grid = tilt_n(grid)
    grid = mirror_v(grid)

    return grid


@functools.cache
def tilt_w(grid: List[List[str]]) -> List[List[str]]:
    return roll_all(grid)


@functools.cache
def rotate_cw(grid: List[List[str]]) -> List[List[str]]:
    num_rows = len(grid)
    num_cols = len(grid[0])

    return tuple([tuple([grid[y][x] for y in reversed(range(num_rows))]) for x in range(num_cols)])


@functools.cache
def rotate_ccw(grid: List[List[str]]) -> List[List[str]]:
    num_rows = len(grid)
    num_cols = len(grid[0])

    return tuple([tuple([grid[y][x] for y in range(num_rows)]) for x in reversed(range(num_cols))])


@functools.cache
def mirror_h(grid: List[List[str]]) -> List[List[str]]:
    num_rows = len(grid)
    num_cols = len(grid[0])

    return tuple([tuple([grid[y][x] for x in reversed(range(num_cols))]) for y in range(num_rows)])


@functools.cache
def mirror_v(grid: List[List[str]]) -> List[List[str]]:
    num_rows = len(grid)
    num_cols = len(grid[0])

    return tuple([tuple([grid[y][x] for x in range(num_cols)]) for y in reversed(range(num_rows))])


@functools.cache
def roll_all(grid: List[List[str]]) -> List[List[str]]:
    return tuple([roll(each) for each in grid])


@functools.cache
def roll(items: List[str]):
    empty = None

    items = list(items)

    for i, item in enumerate(items):
        if item == "O":
            if empty is None:
                # Can't roll any further
                continue
            else:
                items[empty], items[i] = item, "."
                empty += 1
        elif item == ".":
            empty = i if empty is None else empty
        elif item == "#":
            empty = None
            continue
        else:
            raise RuntimeError(items)

    return tuple(items)
