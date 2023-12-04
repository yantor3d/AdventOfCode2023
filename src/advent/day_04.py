"""Advent of Code 2023, Day 04."""

import operator

from typing import List


class Card(object):
    """Lottory scratch card."""

    def __init__(self, drawing_numbers: List[int], winning_numbers: List[int]):
        """Initialize."""

        self.drawing_numbers = drawing_numbers
        self.winning_numbers = winning_numbers

    def score(self):
        """Return the score of this card."""

        matches = [n for n in self.drawing_numbers if n in self.winning_numbers]

        if matches:
            n = 1

            for __ in matches[:-1]:
                n *= 2
        else:
            n = 0

        return n


def part_01(puzzle_input):
    """Solve part one."""

    cards = map(parse_01, puzzle_input)
    scores = map(operator.methodcaller("score"), cards)

    return sum(scores)


def parse_01(line: str) -> Card:
    """Parse the puzzle input for part one."""

    card_num, numbers = line.split(":")
    card_num = int(card_num.split()[-1])

    drawing, winning = numbers.split("|")

    drawing_numbers = parse_numbers(drawing)
    winning_numbers = parse_numbers(winning)

    return Card(drawing_numbers, winning_numbers)


def parse_numbers(fragment: str) -> List[int]:
    """Parse the numbers in the given string."""

    return [int(n) for n in fragment.strip().split()]


def part_02(puzzle_input):
    """Solve part two."""
