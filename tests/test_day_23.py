"""Test suite for Day 23."""

import operator
import itertools
import pytest

import advent.day_23

from advent.day_23 import Point


@pytest.fixture()
def puzzle_input():
    return [
        "#.#####################",
        "#.......#########...###",
        "#######.#########.#.###",
        "###.....#.>.>.###.#.###",
        "###v#####.#v#.###.#.###",
        "###.>...#.#.#.....#...#",
        "###v###.#.#.#########.#",
        "###...#.#.#.......#...#",
        "#####.#.#.#######.#.###",
        "#.....#.#.#.......#...#",
        "#.#####.#.#.#########v#",
        "#.#...#...#...###...>.#",
        "#.#.#v#######v###.###v#",
        "#...#.>.#...>.>.#.###.#",
        "#####v#.#.###v#.#.###.#",
        "#.....#...#...#.#.#...#",
        "#.#########.###.#.#.###",
        "#...###...#...#...#.###",
        "###.###.#.###v#####v###",
        "#...#...#.#.>.>.#.>.###",
        "#.###.###.#.###.#.#v###",
        "#.....###...###...#...#",
        "#####################.#",
    ]


def test_parse(puzzle_input):
    maze, start, end = advent.day_23.parse(puzzle_input)

    assert start == Point(1, 0)
    assert end == Point(21, 22)


def test_digraph_01(puzzle_input):
    maze, start, end = advent.day_23.parse(puzzle_input)

    graph = advent.day_23.as_digraph(maze, start, end, advent.day_23.can_move_01)

    assert start in graph
    assert end in outputs(graph)


def test_walk_01(puzzle_input):
    answers = advent.day_23.solve(puzzle_input, advent.day_23.can_move_01)

    assert answers == [94, 90, 86, 82, 74]


def test_part_01(puzzle_input):
    answer = advent.day_23.part_01(puzzle_input)

    assert answer == 94


def test_digraph_02(puzzle_input):
    maze, start, end = advent.day_23.parse(puzzle_input)

    graph = advent.day_23.as_digraph(maze, start, end, advent.day_23.can_move_02)

    assert start in graph
    assert end in outputs(graph)


def test_part_02(puzzle_input):
    answer = advent.day_23.part_02(puzzle_input)

    assert answer == 154


def outputs(graph):
    result = []

    for src, edges in graph.items():
        result.extend(edges)

    return result
