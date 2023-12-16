"""Advent of Code 2023, Day 10."""

import collections
import itertools
import sys
import time

from typing import Dict, Iterator, List, Set


Point = collections.namedtuple("Point", "x y")


class Cell(collections.namedtuple("Cell", "x, y pipe direction", defaults=(0, 0, None, None))):
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
    "J": "WN",
    "7": "SW",
    "F": "ES",
}

TURNS = {
    ("|", "|"): None,
    ("-", "-"): None,
    ("|", "F"): "E",
    ("|", "L"): "E",
    ("|", "7"): "W",
    ("|", "J"): "W",
    ("-", "F"): "S",
    ("-", "7"): "S",
    ("-", "L"): "N",
    ("-", "J"): "N",
}


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    start_at, pipes, __ = parse(puzzle_input)
    start_at, pipes = get_map(start_at, pipes)

    first_move = PIPES[start_at.pipe][0]

    loop = run_01(start_at, pipes, first_move)

    n = len(loop)

    if n % 2 == 0:
        return n // 2
    else:
        return (n + 1) // 2


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""

    start_at, pipes, __ = parse(puzzle_input)
    start_at, moves = get_map(start_at, pipes)

    first_move = PIPES[start_at.pipe][0]

    loop = run_01(start_at, moves, first_move)

    result = run_02(pipes, loop, flip=True)

    return len(result)


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

    return start_at, result, Point(x, y)


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


def run_01(start_at: Cell, moves: Dict[Cell, Dict[bool, Cell]], first_move: str) -> int:
    """Return the route of the loop."""

    result = []

    prev = start_at._replace(direction=first_move)
    curr = moves[start_at][first_move]

    while True:
        result.append(prev)

        (move_a, next_a), (move_b, next_b) = moves[curr].items()

        if next_a == prev:
            curr = curr._replace(direction=move_b)
            prev, curr = curr, Cell(next_b.x, next_b.y, next_b.pipe)
        elif next_b == prev:
            curr = curr._replace(direction=move_a)
            prev, curr = curr, Cell(next_a.x, next_a.y, next_a.pipe)
        else:
            raise RuntimeError("Impossible")

        if curr == start_at:
            result.append(prev)
            break

    return result


def run_02(pipes: List[Cell], loop: List[Cell], flip=False) -> Set[Cell]:
    """Return the cells enclosed by the loop."""

    pipes = {each: each for each in pipes}

    loop.append(loop[0])

    steps = itertools.cycle(loop)
    loop = {Point(p.x, p.y) for p in loop}

    prev_turn = None

    runs = []
    run = []

    start_at = None

    for step in steps:
        if step.pipe in ["|", "-"]:
            if prev_turn is None:
                continue
            else:
                run.append(step)
        else:
            if prev_turn is None:
                start_at = step
                run.append(step)
            else:
                run.append(step)
                runs.append(run)
                run = [step]

                if step == start_at:
                    break

            prev_turn = step

    on_right = {
        ("7", "S"): "W",
        ("7", "W"): "N",
        ("J", "N"): "E",
        ("J", "W"): "N",
        ("L", "N"): "E",
        ("L", "E"): "S",
        ("F", "S"): "W",
        ("F", "E"): "S",
    }

    result = set()

    for i, run in enumerate(runs, 1):
        key = (run[0].pipe, run[0].direction)

        direction = on_right[key]

        if flip:
            direction = LAST_MOVE[direction]

        move = MOVES[direction]

        for each in run:
            for i in itertools.count(1):
                cell = Point(each.x + (move.x * i), each.y + (move.y * i))

                if cell in loop:
                    break
                else:
                    result.add(cell)

    result = {Point(each.x, each.y) for each in result}

    return result
