"""Test suite for Day 05."""

import pytest

import advent.day_05

from advent.day_05 import MapRange, MapRangesList


@pytest.fixture(scope="function")
def puzzle_input(get_example_input):
    return get_example_input(5)


def test_parse_puzzle_input(puzzle_input):
    data = advent.day_05.parse(puzzle_input)

    assert data["seeds"] == [79, 14, 55, 13]
    assert data["seed-to-soil"] == [
        MapRange(50, 98, 2),
        MapRange(52, 50, 48),
    ]

    assert data["soil-to-fertilizer"] == [
        MapRange(0, 15, 37),
        MapRange(37, 52, 2),
        MapRange(39, 0, 15),
    ]

    assert data["fertilizer-to-water"] == [
        MapRange(49, 53, 8),
        MapRange(0, 11, 42),
        MapRange(42, 0, 7),
        MapRange(57, 7, 4),
    ]

    assert data["water-to-light"] == [
        MapRange(88, 18, 7),
        MapRange(18, 25, 70),
    ]

    assert data["light-to-temperature"] == [
        MapRange(45, 77, 23),
        MapRange(81, 45, 19),
        MapRange(68, 64, 13),
    ]

    assert data["temperature-to-humidity"] == [
        MapRange(0, 69, 1),
        MapRange(1, 0, 69),
    ]

    assert data["humidity-to-location"] == [
        MapRange(60, 56, 37),
        MapRange(56, 93, 4),
    ]


def test_seed_to_soil_mapping(puzzle_input):
    data = advent.day_05.parse(puzzle_input)

    seed_to_soil = MapRangesList(data["seed-to-soil"])

    assert seed_to_soil[79] == 81
    assert seed_to_soil[14] == 14
    assert seed_to_soil[55] == 57
    assert seed_to_soil[13] == 13


def test_part_01(puzzle_input):
    answer = advent.day_05.part_01(puzzle_input)

    assert answer == 35
