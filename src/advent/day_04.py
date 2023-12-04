"""Advent of Code 2023, Day 04."""

import collections
import operator

from typing import List


class Card(object):
    """Lottory scratch card."""

    def __init__(self, number: int, drawing_numbers: List[int], winning_numbers: List[int]):
        """Initialize."""

        self.number = number
        self.drawing_numbers = drawing_numbers
        self.winning_numbers = winning_numbers

    def rewards(self) -> List[int]:
        """Return the rewards (card numbers) for this card."""

        matches = [n for n in self.drawing_numbers if n in self.winning_numbers]

        return [self.number + i for i in range(1, len(matches) + 1)]

    def score(self) -> int:
        """Return the score of this card."""

        matches = [n for n in self.drawing_numbers if n in self.winning_numbers]

        if matches:
            n = 1

            for __ in matches[:-1]:
                n *= 2
        else:
            n = 0

        return n


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    cards = map(parse, puzzle_input)
    scores = map(operator.methodcaller("score"), cards)

    return sum(scores)


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""

    n = 0

    cards = list(map(parse, puzzle_input))
    rewards = {card.number: card.rewards() for card in cards}

    this_stack = collections.Counter(rewards.keys())
    next_stack = collections.Counter()

    while this_stack:
        for card_number, count in sorted(this_stack.items()):
            n += count

            for reward in rewards.get(card_number, []):
                next_stack[reward] += count

        this_stack, next_stack = next_stack, collections.Counter()

    return n


def parse(line: str) -> Card:
    """Parse the puzzle input for part one."""

    card_num, numbers = line.split(":")
    card_num = int(card_num.split()[-1])

    drawing, winning = numbers.split("|")

    drawing_numbers = parse_numbers(drawing)
    winning_numbers = parse_numbers(winning)

    return Card(card_num, drawing_numbers, winning_numbers)


def parse_numbers(fragment: str) -> List[int]:
    """Parse the numbers in the given string."""

    return [int(n) for n in fragment.strip().split()]
