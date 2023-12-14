"""Advent of Code 2023, Day 13."""

import functools

from typing import List, Tuple


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    patterns = parse(puzzle_input)
    reflections = map(find_reflection, patterns)
    scores = map(score, reflections)

    return sum(scores)


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""

    find_smudged_reflection = functools.partial(find_reflection, max_smudge=1)

    patterns = parse(puzzle_input)
    reflections = map(find_smudged_reflection, patterns)
    scores = map(score, reflections)

    return sum(scores)


def parse(puzzle_input: List[str]) -> List[List[str]]:
    results = []
    result = []

    for line in puzzle_input:
        line = line.strip()

        if line:
            result.append(line)
        else:
            results.append(result)
            result = []
    else:
        if result:
            results.append(result)

    return results


def score(reflection: Tuple[str, Tuple[int, int]]) -> int:
    d, (s, __) = reflection

    if d == "v":
        return s
    elif d == "h":
        return s * 100
    else:
        return 0


def find_reflection(pattern: List[str], max_smudge: int = 0) -> Tuple[str, Tuple[int, int]]:
    h = find_h_reflection(pattern, max_smudge)
    v = find_v_reflection(pattern, max_smudge)

    return h or v


def find_v_reflection(pattern: List[str], max_smudge: int = 0) -> Tuple[str, Tuple[int, int]]:
    pattern = col_major(pattern)

    rows = list(range(len(pattern)))

    for s, e in zip(rows, rows[1:]):
        if is_mirrored_at(pattern, s, e, max_smudge):
            return ("v", (s + 1, e + 1))


def find_h_reflection(pattern: List[str], max_smudge: int = 0) -> Tuple[str, Tuple[int, int]]:
    pattern = row_major(pattern)

    rows = list(range(len(pattern)))

    for s, e in zip(rows, rows[1:]):
        if is_mirrored_at(pattern, s, e, max_smudge):
            return ("h", (s + 1, e + 1))


def row_major(pattern: List[str]) -> List[str]:
    return pattern


def col_major(pattern: List[str]) -> List[str]:
    rows = range(len(pattern))
    cols = range(len(pattern[0]))

    return ["".join([pattern[row][col] for row in rows]) for col in cols]


def is_mirrored_at(
    pattern: List[str], s: int, e: int, max_smudge: int = 0, num_smudge: int = 0
) -> bool:
    if s < 0:
        return num_smudge == max_smudge

    if e == len(pattern):
        return num_smudge == max_smudge

    if num_smudge > max_smudge:
        return False

    if is_mirrored(pattern[s], pattern[e]):
        return True and is_mirrored_at(pattern, s - 1, e + 1, max_smudge, num_smudge)
    elif max_smudge and is_smudged(pattern[s], pattern[e]):
        return True and is_mirrored_at(pattern, s - 1, e + 1, max_smudge, num_smudge + 1)
    else:
        return False


def is_mirrored(lhs: str, rhs: str) -> bool:
    return lhs == rhs


def is_smudged(lhs: str, rhs: str) -> bool:
    return [a == b for a, b in zip(lhs, rhs)].count(False) == 1
