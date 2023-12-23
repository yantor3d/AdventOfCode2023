"""Advent of Code 2023, Day 22."""

import collections
import operator
import string
import itertools

from typing import Dict, Iterable, List, Set, Tuple

Matrix = List[List[str]]


class Point(collections.namedtuple("Point", "x,y,z")):
    def __repr__(self) -> str:
        return f"{self.x},{self.y},{self.z}"

    def __str__(self) -> str:
        return repr(self)


class Block(collections.namedtuple("Block", "name,start,end")):
    def __repr__(self) -> str:
        s, e = self.start, self.end

        return f"{self.name}: {s.x},{s.y},{s.z}~{e.x},{e.y},{e.z}"

    def __str__(self) -> str:
        return repr(self)

    def points(self) -> List[Point]:
        s, e = self.start, self.end
        for x in range(s.x, e.x + 1):
            for y in range(s.y, e.y + 1):
                for z in range(s.z, e.z + 1):
                    yield Point(x, y, z)

    def score(self) -> Tuple[int, int]:
        return (
            min(self.start.z, self.end.z),
            max(self.start.z, self.end.z),
            min(self.start.y, self.end.y),
            max(self.start.y, self.end.y),
            min(self.start.x, self.end.x),
            max(self.start.x, self.end.x),
        )


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    blocks = parse(puzzle_input)
    blocks = fall(blocks)
    safe, unsafe = dust(blocks)

    return len(safe)


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""

    blocks = parse(puzzle_input)
    blocks = fall(blocks)
    safe, unsafe = dust(blocks)

    n = 0

    for each in unsafe:
        x = dust_and_fall(blocks, each)
        n += x

    return n


def parse(puzzle_input: List[str]) -> List[Block]:
    if len(puzzle_input) <= 26:
        names = string.ascii_uppercase
    else:
        names = itertools.count()

    result = list()

    for n, line in zip(names, puzzle_input):
        s, e = line.split("~")

        s = Point(*map(int, s.split(",")))
        e = Point(*map(int, e.split(",")))

        b = Block(str(n), s, e)
        result.append(b)

    return result


def fall(blocks: List[Block]) -> List[Block]:
    result = []

    zyx = as_matrix(blocks)

    blocks = sorted(blocks, key=operator.methodcaller("score"))

    ny = len(zyx[0])
    nx = len(zyx[0][0])

    xy = [[0] * ny for _ in range(nx + 1)]

    # print()
    for old_block in blocks:
        z = 1
        h = old_block.end.z - old_block.start.z

        for p in old_block.points():
            z = max(z, xy[p.x][p.y])

        n, s, e = old_block

        new_block = Block(n, Point(s.x, s.y, z), Point(e.x, e.y, z + h))

        for p in new_block.points():
            xy[p.x][p.y] = p.z + 1

        result.append(new_block)

        # print(f"{old_block} -> {new_block}")

    return result


def rest(blocks: List[Point]) -> Tuple[Dict[Point, Set]]:
    above = {b.name: set() for b in blocks}
    below = {b.name: set() for b in blocks}

    zyx = as_matrix(blocks)

    for k in blocks:
        for p in k.points():
            try:
                a = zyx[p.z - 1][p.y][p.x]
            except IndexError:
                a = "."

            if a not in (".", k.name):
                above[k.name].add(a)

            try:
                b = zyx[p.z + 1][p.y][p.x]
            except IndexError:
                b = "."

            if b not in (".", k.name):
                below[k.name].add(b)

    return above, below


def dust(blocks: List[Block]) -> Set[str]:
    safe = set()
    unsafe = set()

    above, below = rest(blocks)

    for block in blocks:
        for b in below[block.name]:
            if len(above[b]) == 1:
                unsafe.add(block.name)
                break
        else:
            safe.add(block.name)

    return safe, unsafe


def dust_and_fall(blocks: List[Block], to_dust: str) -> int:
    old_blocks = [b for b in blocks if b.name != to_dust]
    new_blocks = fall(old_blocks)

    old_blocks = {b.name: b for b in old_blocks}
    new_blocks = {b.name: b for b in new_blocks}

    n = 0

    for name, old_block in old_blocks.items():
        new_block = new_blocks[name]

        n += old_block.score() != new_block.score()

    return n


def as_matrix(blocks: List[Block]) -> Matrix:
    xs, ys, zs = (
        {
            0,
        },
        {
            0,
        },
        {
            0,
        },
    )

    points = dict()

    for b in blocks:
        xs.add(b.start.x), xs.add(b.end.x)
        ys.add(b.start.y), ys.add(b.end.y)
        zs.add(b.start.z), zs.add(b.end.z)

        for p in b.points():
            points[p] = b.name

    mn = Point(0, 0, 0)
    mx = Point(max(xs), max(ys), max(zs))

    zyx = []

    for z in range(mn.z, mx.z + 1):
        z_ = []
        for y in range(mn.y, mx.y + 1):
            y_ = []
            for x in range(mn.x, mx.x + 1):
                p = Point(x, y, z)

                y_.append(points.get(p, "."))
            z_.append(y_)
        zyx.append(z_)

    return zyx


def xz_view(blocks: List[Point]) -> List[str]:
    zyx = as_matrix(blocks)

    num_rows = len(zyx)
    num_cols = len(zyx[0])

    empty = "."
    many = "?"

    rows = [[empty for _ in range(num_cols)] for r in range(num_rows)]

    for i, z in enumerate(zyx):
        for j, y in enumerate(z):
            for k, x in enumerate(y):
                if x == ".":
                    continue

                if rows[i][k] == empty:
                    rows[i][k] = x
                elif rows[i][k] != x:
                    rows[i][k] = many
                else:
                    rows[i][k] = x

    view(rows, "x")


def yz_view(blocks: List[Point]) -> List[str]:
    zyx = as_matrix(blocks)
    num_rows = len(zyx)
    num_cols = len(zyx[0])

    empty = "."
    many = "?"

    rows = [[empty for _ in range(num_cols)] for _ in range(num_rows)]

    for i, z in enumerate(zyx):
        for j, y in enumerate(z):
            for k, x in enumerate(y):
                if x == ".":
                    continue

                if rows[i][j] == empty:
                    rows[i][j] = x
                elif rows[i][j] != x:
                    rows[i][j] = many
                else:
                    rows[i][j] = x

    view(rows, "y")


def view(rows, axis):
    num_rows = len(rows)
    num_cols = len(rows[0])

    expand = False
    for i, row in enumerate(rows):
        for j, col in enumerate(row):
            if str.isdigit(col):
                expand = True
    for i, row in enumerate(rows):
        for j, col in enumerate(row):
            if expand:
                if str.isdigit(col):
                    rows[i][j] = f" {int(col): >4d} "
                else:
                    rows[i][j] = f" {col * 4} "

    rows.reverse()
    if expand:
        rows[-1] = [f" {'-' * 4} " for _ in range(num_cols)]
    else:
        rows[-1] = "-" * num_cols

    n = num_rows
    print()

    cols = list(range(num_cols))
    cols = [f" {c: >4d} " if expand else f"{c}" for c in cols]
    print("".join(cols))

    for i, row in enumerate(rows, 1):
        print(f"{''.join(row)} {n - i}{' z' if num_rows // 2 == i else ''}")
