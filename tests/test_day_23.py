"""Test suite for Day 23."""

import operator
import pytest

import advent.day_23

from advent.day_23 import Point, Route


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


def test_route_segments(puzzle_input):
    maze, start, end = advent.day_23.parse(puzzle_input)

    routes = list(advent.day_23.route_segments(maze, "v", start, end))
    routes.sort(key=operator.attrgetter("start"))

    assert routes[0] == Route(Point(1, 0), Point(3, 5), 16, [Point(3, 6), Point(4, 5)])
    assert routes[1] == Route(Point(3, 6), Point(5, 13), 22, [Point(5, 14), Point(6, 13)])
    assert routes[2] == Route(Point(4, 5), Point(11, 3), 22, [Point(12, 3), Point(11, 4)])


def test_route_map(puzzle_input):
    maze, start, end = advent.day_23.parse(puzzle_input)

    routes_map = advent.day_23.get_route_map(maze, start, end)

    assert routes_map[Point(1, 0)] == {
        Point(3, 6): 16,
        Point(4, 5): 16,
    }


def test_part_01_routes(puzzle_input):
    maze, start, end = advent.day_23.parse(puzzle_input)

    routes_map = advent.day_23.get_route_map(maze, start, end)
    routes = advent.day_23.get_routes(routes_map, start)
    routes.sort(reverse=True)

    assert routes == [94, 90, 86, 82, 82, 74]


def test_part_01(puzzle_input):
    answer = advent.day_23.part_01(puzzle_input)

    assert answer == 94
