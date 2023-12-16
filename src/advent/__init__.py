"""Advent of Code 2023."""

import contextlib
import collections
import os
import time

from typing import Any, List, Tuple

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

Answer = collections.namedtuple("Answer", "value time")


def solve(
    day: int, fn_01: callable = None, fn_02: callable = None, source: str = "data"
) -> Tuple[Any, Any]:
    """Solve the puzzle for the given day.

    Args:
        day (int): Day of the puzzle.
        fn_01 (callable): Solver for part 01.
        fn_02 (callable): Solver for part 02.
        source (str): Name of the data dir (eg, 'test').

    Returns:
        tuple
    """

    puzzle_input = get_puzzle_input(day, source)

    answer_01 = run("Part 01", fn_01, puzzle_input)
    answer_02 = run("Part 02", fn_02, puzzle_input)

    return answer_01, answer_02


def run(part: str, fn: callable, puzzle_input: List[str]) -> Answer:
    st = time.time()
    value = fn(puzzle_input)
    et = time.time()

    answer = Answer(value, et - st)

    if value is not None:
        print(f"{part}: {answer.value:< 16} in {answer.time:.3f}s")

    return answer


def get_puzzle_input(day: int, source: str = "data") -> List[str]:
    """Return the puzzle input for the given day.

    Args:
        day (int): Day to get the puzzle inpurt for.
        source (str): Name of the data dir (eg, 'test').

    Returns:
        list[str]
    """

    path = os.path.join(ROOT, source, f"day_{day:02d}.txt")

    with open(path, "r") as fp:
        return [line.strip() for line in fp.readlines()]
