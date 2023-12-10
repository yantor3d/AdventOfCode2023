"""Test suite for Day ."""

import pytest

import advent.day_10

from advent.day_10 import Cell


def test_parse_example_01a():
    puzzle_input = [
        ".....",
        ".S-7.",
        ".|.|.",
        ".L-J.",
        ".....",
    ]

    start_at, result = advent.day_10.parse(puzzle_input)

    assert start_at == Cell(1, 1, "S")

    check_results(start_at, result)

    assert result[start_at]["E"] == Cell(2, 1, "-"), "Wrong clockwise cell for start"
    assert result[start_at]["S"] == Cell(1, 2, "|"), "Wrong counter-clockwise cell for start"


def test_parse_example_01b():
    puzzle_input = [
        "..F7.",
        ".FJ|.",
        "SJ.L7",
        "|F--J",
        "LJ...",
    ]

    start_at, result = advent.day_10.parse(puzzle_input)

    assert start_at == Cell(0, 2, "S")

    check_results(start_at, result)

    assert result[start_at]["E"] == Cell(1, 2, "J")
    assert result[start_at]["S"] == Cell(0, 3, "|")


def check_results(start_at, result):
    assert start_at in result, "Start position not in results."

    assert len(result[start_at]) == 2, (start_at, result[start_at])

    a, b = result[start_at]

    assert result[start_at][a] in result, "Start position exits to cell out of range"
    assert result[start_at][b] in result, "Start position exits to cell out of range"


def test_example_01a():
    puzzle_input = [
        ".....",
        ".S-7.",
        ".|.|.",
        ".L-J.",
        ".....",
    ]

    answer = advent.day_10.part_01(puzzle_input)

    assert answer == 4


def test_example_01b():
    puzzle_input = [
        "..F7.",
        ".FJ|.",
        "SJ.L7",
        "|F--J",
        "LJ...",
    ]

    answer = advent.day_10.part_01(puzzle_input)

    assert answer == 8
