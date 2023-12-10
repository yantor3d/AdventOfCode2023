"""Advent of Code 2023, Day 10."""

import collections

from typing import Dict, List, Tuple


class Cell(collections.namedtuple("Cell", "x, y pipe", defaults=(0, 0, None))):
    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, Cell):
            return (self.x, self.y) == (other.x, other.y)
        else:
            return False


LAST_MOVE = {
    "N": "S",
    "S": "N",
    "E": "W",
    "W": "E",
}

MOVES = {
    "N": Cell(0, -1),
    "S": Cell(0, 1),
    "E": Cell(1, 0),
    "W": Cell(-1, 0),
}

PIPES = {
    "|": "NS",
    "-": "EW",
    "L": "NE",
    "J": "NW",
    "7": "SW",
    "F": "SE",
}


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    start_at, pipes = parse(puzzle_input)

    a, __ = pipes[start_at]

    cw = run(start_at, pipes, first_move=a)

    if cw % 2 == 0:
        return cw // 2
    else:
        return (cw + 1) // 2


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""


def parse(puzzle_input: List[str]) -> Dict[Cell, Dict[bool, Cell]]:
    """Parse the puzzle input"""

    result = {}

    start_at = None

    for y, line in enumerate(puzzle_input):
        for x, char in enumerate(line):
            if char == ".":
                continue

            if char == "S":
                start_at = Cell(x, y, char)
                continue

            if char in PIPES:
                cell = Cell(x, y, char)
                result[cell] = cell

    tmp = dict(result)
    tmp[start_at] = start_at

    for cell in result:
        result[cell] = {}

        for direction in PIPES[cell.pipe]:
            move = MOVES[direction]
            dest = Cell(cell.x + move.x, cell.y + move.y)

            try:
                result[cell][direction] = tmp[dest]
            except KeyError:
                pass

    start_moves = {}

    for cell, moves in result.items():
        for direction, move in moves.items():
            if move == start_at:
                start_moves[LAST_MOVE[direction]] = cell

    result[start_at] = start_moves

    return start_at, result


def run(start_at: Cell, pipes: Dict[Cell, Dict[bool, Cell]], first_move: str) -> int:
    """Return the number of steps in the loop."""

    prev = start_at
    curr = pipes[start_at][first_move]

    n = 1

    while True:
        (move_a, next_a), (move_b, next_b) = pipes[curr].items()

        if next_a == prev:
            prev, curr = curr, next_b
        elif next_b == prev:
            prev, curr = curr, next_a
        else:
            raise RuntimeError("Impossible")

        if curr == start_at:
            break
        else:
            n += 1

    return n
