"""Advent of Code 2023, Day 10."""

import collections
import sys

from typing import Dict, Iterator, List, Set, Tuple


class Cell(collections.namedtuple("Cell", "x, y pipe", defaults=(0, 0, None))):
    def __repr__(self):
        if self.pipe:
            return f"{self.__class__.__name__}(x={self.x}, y={self.y}, pipe={self.pipe})"
        else:
            return f"{self.__class__.__name__}(x={self.x}, y={self.y})"

    def __hash__(self):
        return hash((self.x, self.y))

    def __le__(self, other):
        return self.x <= other.x and self.y <= other.y

    def __ge__(self, other):
        return self.x >= other.x and self.y >= other.y

    def __eq__(self, other):
        if isinstance(other, Cell):
            return (self.x, self.y) == (other.x, other.y)
        else:
            return False

    def adjacent(self) -> Iterator:
        """Yield the cells adjacent to this one."""

        yield Cell(self.x + 1, self.y + 1)
        yield Cell(self.x + 1, self.y + 0)
        yield Cell(self.x + 1, self.y + -1)

        yield Cell(self.x + 0, self.y + 1)
        yield Cell(self.x + 0, self.y + -1)

        yield Cell(self.x - 1, self.y + 1)
        yield Cell(self.x - 1, self.y + 0)
        yield Cell(self.x - 1, self.y + -1)


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

    start_at, pipes, __ = parse(puzzle_input)
    start_at, pipes = get_map(start_at, pipes)

    first_move = PIPES[start_at.pipe][0]

    loop = run(start_at, pipes, first_move)

    n = len(loop)

    if n % 2 == 0:
        return n // 2
    else:
        return (n + 1) // 2


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""

    # I have been trying to solve this for too many hours.
    # I think it has something to do with a scanline search.
    # There are sixteen possible turns following the loop clockwise"
    # F-7 -> S
    # F-J -> S
    # L-J -> N
    # L-7 -> N
    # J-L => N
    # J-F -> N
    # 7-F -> S
    # 7-L -> S
    #
    # F|L -> E
    # F|J -> E
    # 7|J -> W
    # 7|L -> W
    # L|F -> E
    # L|7 -> E
    # J|F -> W
    # J|7 -> W
    # For each straight tile between the turns,
    # all tiles to "right" until the next part of the loop
    # are bounded by the loop


def parse(puzzle_input: List[str]) -> List[Cell]:
    """Parse the puzzle input"""

    result = []

    start_at = None

    for y, line in enumerate(puzzle_input):
        for x, char in enumerate(line):
            cell = Cell(x, y, char)

            if char == "S":
                start_at = cell

            result.append(cell)

    return start_at, result, Cell(x, y)


def get_map(start_at: Cell, pipes: List[Cell]) -> Dict[Cell, Dict[str, Cell]]:
    result = {}

    cells = {cell: cell for cell in pipes}

    for cell in pipes:
        if cell.pipe == "S":
            continue

        if cell.pipe == ".":
            continue

        result[cell] = {}

        for direction in PIPES[cell.pipe]:
            move = MOVES[direction]
            dest = Cell(cell.x + move.x, cell.y + move.y)

            try:
                result[cell][direction] = cells[dest]
            except KeyError:
                pass

    start_moves = {}

    for cell, moves in sorted(result.items()):
        for direction, move in moves.items():
            if move == start_at:
                start_moves[LAST_MOVE[direction]] = cell

    for pipe, (a, b) in PIPES.items():
        if a in start_moves and b in start_moves:
            start_at = Cell(start_at.x, start_at.y, pipe)
            break

    result[start_at] = start_moves

    return start_at, result


def run(start_at: Cell, pipes: Dict[Cell, Dict[bool, Cell]], first_move: str) -> int:
    """Return the route of the loop."""

    result = []

    prev = start_at
    curr = pipes[start_at][first_move]

    while True:
        result.append(prev)

        (move_a, next_a), (move_b, next_b) = pipes[curr].items()

        if next_a == prev:
            prev, curr = curr, next_b
        elif next_b == prev:
            prev, curr = curr, next_a
        else:
            raise RuntimeError("Impossible")

        if curr == start_at:
            result.append(prev)
            break

    return result
