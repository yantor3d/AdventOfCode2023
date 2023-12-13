"""Advent of Code 2023, Day 13."""

from typing import List, Tuple


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    patterns = parse(puzzle_input)
    reflections = map(find_reflection, patterns)
    scores = map(score, reflections)

    return sum(scores)


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""


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


def find_reflection(pattern: List[str]) -> Tuple[str, Tuple[int, int]]:
    h = find_h_reflection(pattern)
    v = find_v_reflection(pattern)

    return h or v


def find_v_reflection(pattern: List[str]) -> Tuple[str, Tuple[int, int]]:
    pattern = col_major(pattern)

    rows = list(range(len(pattern)))

    for s, e in zip(rows, rows[1:]):
        sr = pattern[s]
        er = pattern[e]

        if sr == er and is_perfect_mirror(pattern, s, e):
            return ("v", (s + 1, e + 1))


def find_h_reflection(pattern: List[str]) -> Tuple[str, Tuple[int, int]]:
    pattern = row_major(pattern)

    rows = list(range(len(pattern)))

    for s, e in zip(rows, rows[1:]):
        sr = pattern[s]
        er = pattern[e]

        if sr == er and is_perfect_mirror(pattern, s, e):
            return ("h", (s + 1, e + 1))


def row_major(pattern: List[str]) -> List[str]:
    return pattern


def col_major(pattern: List[str]) -> List[str]:
    rows = range(len(pattern))
    cols = range(len(pattern[0]))

    return ["".join([pattern[row][col] for row in rows]) for col in cols]


def is_perfect_mirror(pattern: List[str], s: int, e: int) -> bool:
    result = True

    n = len(pattern)

    while True:
        if not is_mirror_image(pattern[s : e + 1]):
            result = False
            break

        s -= 1
        e += 1

        if s < 0:
            break

        if e == n:
            break

    return result


def is_mirror_image(pattern: List[str]) -> bool:
    n = len(pattern) // 2

    return pattern[:n] == pattern[n:][::-1]
