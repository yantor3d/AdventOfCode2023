"""Advent of Code 2023, Day 06."""

import sys

from typing import Dict, List, Tuple


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    result = 1

    races = parse_01(puzzle_input)

    for duration, record in sorted(races.items()):
        mn, mx = win(duration, record)

        result *= num_wins(mn, mx)

    return result


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""

    result = 1

    races = parse_02(puzzle_input)

    for duration, record in sorted(races.items()):
        mn, mx = win(duration, record)

        result *= num_wins(mn, mx)

    return result


def parse_01(puzzle_input: List[str]) -> Dict[int, int]:
    t, d = puzzle_input

    return dict(
        zip(
            parse_line_01(t),
            parse_line_01(d),
        ),
    )


def parse_02(puzzle_input: List[str]) -> Dict[int, int]:
    t, d = puzzle_input

    t = parse_line_02(t)
    d = parse_line_02(d)

    return {t: d}


def parse_line_01(line: str) -> List[int]:
    __, values = line.split(":")

    return list(map(int, values.strip().split()))


def parse_line_02(line: str) -> int:
    __, values = line.split(":")

    return int(values.replace(" ", ""))


def run(duration: int, hold: int) -> int:
    speed = hold

    distance = (duration - hold) * speed

    return distance


def win(duration: int, record: int) -> Tuple[int, int]:
    mn = sys.maxsize
    mx = -1

    for hold in range(0, duration, 1):
        distance = run(duration, hold)

        if distance > record:
            mn = min(mn, hold)

        if hold > mn:
            break

    for hold in range(duration, 1, -1):
        distance = run(duration, hold)

        if distance > record:
            mx = max(mx, hold)

        if hold < mx:
            break

    return mn, mx


def num_wins(mn: int, mx: int) -> int:
    return mx - mn + 1
