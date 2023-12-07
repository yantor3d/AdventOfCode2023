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


CARDS_01 = "AKQJT98765432"[::-1]
CARDS_02 = "AKQT98765432J"[::-1]

Hand = collections.namedtuple("Hand", "cards bid rank", defaults=("", -1, -1))


def part_01(puzzle_input):
    """Solve part one."""

    hands = parse(puzzle_input)
    hands = rank_hands_01(hands)

    winnings = [hand.bid * hand.rank for hand in hands]

    return sum(winnings)


def part_02(puzzle_input):
    """Solve part two."""

    hands = parse(puzzle_input)
    hands = rank_hands_02(hands)

    winnings = [hand.bid * hand.rank for hand in hands]

    return sum(winnings)


def parse(puzzle_input: List[str]) -> List[Hand]:
    """Parse the hands in the puzzle input."""

    return list(map(parse_line, puzzle_input))


def parse_line(line: str) -> Hand:
    """Parse the hand in the given line."""

    cards, bid = line.split()

    return Hand(cards, int(bid), -1)


def rank_hands_01(hands: List[Hand]) -> List[Hand]:
    return [hand._replace(rank=i) for i, hand in enumerate(sorted(hands, key=key_hand_01), 1)]


def score_hand_01(hand: Hand) -> Hands:
    count = collections.Counter(hand.cards)
    value = tuple(sorted(count.values(), reverse=True))

    return Hands(value)


def key_hand_01(hand: Hand):
    score = score_hand_01(hand).value
    cards = list(map(CARDS_01.index, hand.cards))

    return score, cards


def rank_hands_02(hands: List[Hand]) -> List[Hand]:
    return [hand._replace(rank=i) for i, hand in enumerate(sorted(hands, key=key_hand_02), 1)]


def score_hand_02(hand: Hand) -> Hands:
    high_score = Hands.HIGH
    high_hand = None

    for card in CARDS_02[::-1]:
        wild_hand = hand._replace(cards=hand.cards.replace("J", card))

        wild_score = score_hand_01(wild_hand)

        if wild_score.value > high_score.value:
            high_score = wild_score
            high_hand = wild_hand

    if high_hand is None:
        return score_hand_01(hand)
    else:
        return high_score


def key_hand_02(hand: Hand):
    score = score_hand_02(hand).value
    cards = list(map(CARDS_02.index, hand.cards))

    return score, cards
