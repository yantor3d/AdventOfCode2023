"""Advent of Code 2023, Day 07."""

import collections
import enum

from typing import List


class Hands(enum.Enum):
    """Winning hands."""

    FIVE = (5,)
    FOUR = (4, 1)
    FULL = (3, 2)
    THREE = (3, 1, 1)
    TWO = (2, 2, 1)
    ONE = (2, 1, 1, 1)
    HIGH = (1, 1, 1, 1, 1)


CARDS = "AKQJT98765432"[::-1]

Hand = collections.namedtuple("Hand", "cards bid rank", defaults=("", -1, -1))


def part_01(puzzle_input):
    """Solve part one."""

    hands = parse(puzzle_input)
    hands = rank_hands(hands)

    winnings = [hand.bid * hand.rank for hand in hands]

    return sum(winnings)


def part_02(puzzle_input):
    """Solve part two."""


def parse(puzzle_input: List[str]) -> List[Hand]:
    """Parse the hands in the puzzle input."""

    return list(map(parse_line, puzzle_input))


def parse_line(line: str) -> Hand:
    """Parse the hand in the given line."""

    cards, bid = line.split()

    return Hand(cards, int(bid), -1)


def rank_hands(hands: List[Hand]) -> List[Hand]:
    return [hand._replace(rank=i) for i, hand in enumerate(sorted(hands, key=key_hand), 1)]


def score_hand(hand: Hand) -> Hands:
    count = collections.Counter(hand.cards)
    value = tuple(sorted(count.values(), reverse=True))

    return Hands(value)


def key_hand(hand: Hand):
    score = score_hand(hand).value
    cards = list(map(CARDS.index, hand.cards))

    return score, cards
