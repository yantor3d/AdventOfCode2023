"""Advent of Code 2023, Day 06."""

from typing import Dict, Iterator, List


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    result = 1

    races = parse(puzzle_input)

    for duration, record in sorted(races.items()):
        wins = win(duration, record)

        result *= len(wins)

    return result


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""


def parse(puzzle_input: List[str]) -> Dict[int, int]:
    t, d = puzzle_input

    return dict(
        zip(
            parse_line(t),
            parse_line(d),
        ),
    )


def parse_line(line: str) -> List[int]:
    __, values = line.split(":")

    return list(map(int, values.strip().split()))


def run(duration: int, hold: int) -> int:
    speed = hold

    distance = (duration - hold) * speed

    return distance


def win(duration: int, record: int) -> List[int]:
    result = []

    for hold in range(duration):
        distance = run(duration, hold)

        if distance > record:
            result.append(hold)

    return result
