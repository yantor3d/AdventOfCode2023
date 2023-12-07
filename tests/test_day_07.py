"""Test suite for Day 07."""

import pytest

import advent.day_07

from advent.day_07 import Hand, Hands


@pytest.fixture(scope="function")
def puzzle_input():
    return [
        "32T3K 765",
        "T55J5 684",
        "KK677 28",
        "KTJJT 220",
        "QQQJA 483",
    ]


@pytest.fixture(scope="function")
def cards_01():
    advent.day_07.CARDS = advent.day_07.CARDS_01


@pytest.fixture(scope="function")
def cards_02():
    advent.day_07.CARDS = advent.day_07.CARDS_02


def test_parse_01(puzzle_input):
    hands = advent.day_07.parse(puzzle_input)

    assert hands == [
        Hand("32T3K", 765),
        Hand("T55J5", 684),
        Hand("KK677", 28),
        Hand("KTJJT", 220),
        Hand("QQQJA", 483),
    ]


@pytest.mark.parametrize(
    "hand,expected",
    [
        (Hand("32T3K", 765), Hands.ONE),
        (Hand("T55J5", 684), Hands.THREE),
        (Hand("KK677", 28), Hands.TWO),
        (Hand("KTJJT", 220), Hands.TWO),
        (Hand("QQQJA", 483), Hands.THREE),
    ],
    ids=[
        "32T3K - One pair",
        "T55J5 - Three of a kind",
        "KK677 - Two pair",
        "KTJJT - Two pair",
        "QQQJA - Three of a kind",
    ],
)
def test_type_01(hand, expected):
    actual = advent.day_07.score_hand_01(hand)

    assert actual.name == expected.name


def test_strength_01(puzzle_input, cards_01):
    hands = advent.day_07.parse(puzzle_input)

    scores = advent.day_07.rank_hands_01(hands)
    scores = {hand.cards: hand for hand in scores}

    assert scores["32T3K"].rank == 1
    assert scores["KTJJT"].rank == 2
    assert scores["KK677"].rank == 3
    assert scores["T55J5"].rank == 4
    assert scores["QQQJA"].rank == 5


def test_part_01(puzzle_input):
    answer = advent.day_07.part_01(puzzle_input)

    assert answer == 6440


@pytest.mark.parametrize(
    "hand,expected",
    [
        (Hand("32T3K", 765), Hands.ONE),
        (Hand("T55J5", 684), Hands.FOUR),
        (Hand("KK677", 28), Hands.TWO),
        (Hand("KTJJT", 220), Hands.FOUR),
        (Hand("QQQJA", 483), Hands.FOUR),
    ],
    ids=[
        "32T3K - One pair",
        "T55J5 - Four of a kind",
        "KK677 - Two pair",
        "KTJJT - Four of a kind",
        "QQQJA - Four of a kind",
    ],
)
def test_type_02(hand, expected):
    actual = advent.day_07.score_hand_02(hand)

    assert actual.name == expected.name


def test_strength_02(puzzle_input, cards_02):
    hands = advent.day_07.parse(puzzle_input)

    scores = advent.day_07.rank_hands_02(hands)
    scores = {hand.cards: hand for hand in scores}

    assert scores["32T3K"].rank == 1
    assert scores["KK677"].rank == 2
    assert scores["T55J5"].rank == 3
    assert scores["QQQJA"].rank == 4
    assert scores["KTJJT"].rank == 5


def test_part_02(puzzle_input):
    answer = advent.day_07.part_02(puzzle_input)

    assert answer == 5905
