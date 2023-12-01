"""Advent of Code 2023."""

import os
import time

from typing import Any, List, Tuple

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


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

    print()

    args = get_puzzle_input(day, source)

    st = time.time()
    answer_01 = fn_01(args)
    et = time.time()

    if answer_01 is not None:
        print(f"Part 01: {answer_01}")
        print("Took {:.3f} seconds".format(et - st))

    st = time.time()
    answer_02 = fn_02(args)
    et = time.time()

    if answer_02 is not None:
        print(f"Part 02: {answer_02}")
        print("Took {:.3f} seconds".format(et - st))

    return answer_01, answer_02


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
