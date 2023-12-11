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

    start_at, result, mx = advent.day_10.parse(puzzle_input)

    assert start_at == Cell(1, 1, "S")
    assert mx == Cell(4, 4)

    start_at, result = advent.day_10.get_map(start_at, result)

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

    start_at, result, mx = advent.day_10.parse(puzzle_input)

    assert start_at == Cell(0, 2, "S")
    assert mx == Cell(4, 4)

    start_at, result = advent.day_10.get_map(start_at, result)

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


@pytest.mark.parametrize(
    "a,b,expected",
    [
        [Cell(1, 2), Cell(1, 2), True],
        [Cell(1, 2), Cell(1, 3), True],
        [Cell(1, 2), Cell(3, 2), True],
        [Cell(1, 2), Cell(3, 3), True],
        [Cell(1, 2), Cell(1, 1), False],
        [Cell(1, 2), Cell(0, 1), False],
        [Cell(2, 2), Cell(1, 2), False],
    ],
    ids=[
        "ax == ax, ay == by",
        "ax == ax, ay <  by",
        "ax <  ax, ay == by",
        "ax <  ax, ay <  by",
        "ax == by, ay >  by",
        "ax >  bx, ay >  by",
        "ax >  bx, ay == by",
    ],
)
def test_cell_less_than_or_equal(a, b, expected):
    assert (a <= b) == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        [Cell(1, 2), Cell(1, 2), True],
        [Cell(1, 3), Cell(1, 2), True],
        [Cell(2, 2), Cell(1, 2), True],
        [Cell(2, 3), Cell(1, 2), True],
        [Cell(1, 1), Cell(1, 2), False],
        [Cell(0, 1), Cell(1, 2), False],
        [Cell(0, 2), Cell(1, 2), False],
    ],
    ids=[
        "ax == ax, ay == by",
        "ax == ax, ay <  by",
        "ax <  ax, ay == by",
        "ax <  ax, ay <  by",
        "ax == by, ay <  by",
        "ax <  bx, ay <  by",
        "ax <  bx, ay == by",
    ],
)
def test_cell_geater_than_or_equal(a, b, expected):
    assert (a >= b) == expected


def test_example_02_01a():
    puzzle_input = [
        ".....",
        ".S-7.",
        ".|.|.",
        ".L-J.",
        ".....",
    ]

    answer = run_02(puzzle_input)

    assert answer == {
        Cell(2, 2),
    }


def test_example_02_01b():
    puzzle_input = [
        "..F7.",
        ".FJ|.",
        "SJ.L7",
        "|F--J",
        "LJ...",
    ]

    answer = run_02(puzzle_input)

    assert answer == {
        Cell(2, 2),
    }


def test_example_02a():
    puzzle_input = [
        "...........",
        ".S-------7.",
        ".|F-----7|.",
        ".||.....||.",
        ".||.....||.",
        ".|L-7.F-J|.",
        ".|..|.|..|.",
        ".L--J.L--J.",
        "...........",
    ]

    answer = run_02(puzzle_input)

    assert len(answer) == 4

    assert answer == {
        Cell(2, 6),
        Cell(3, 6),
        Cell(7, 6),
        Cell(8, 6),
    }


def test_example_02b():
    puzzle_input = [
        "..........",
        ".S------7.",
        ".|F----7|.",
        ".||....||.",
        ".||....||.",
        ".|L-7F-J|.",
        ".|..||..|.",
        ".L--JL--J.",
        "..........",
    ]

    answer = run_02(puzzle_input)

    assert len(answer) == 4

    assert answer == {
        Cell(2, 6),
        Cell(3, 6),
        Cell(6, 6),
        Cell(7, 6),
    }


def test_example_02c():
    puzzle_input = [
        ".F----7F7F7F7F-7....",
        ".|F--7||||||||FJ....",
        ".||.FJ||||||||L7....",
        "FJL7L7LJLJ||LJ.L-7..",
        "L--J.L7...LJS7F-7L7.",
        "....F-J..F7FJ|L7L7L7",
        "....L7.F7||L7|.L7L7|",
        ".....|FJLJ|FJ|F7|.LJ",
        "....FJL-7.||.||||...",
        "....L---J.LJ.LJLJ...",
    ]

    actual = run_02(puzzle_input, flip=True)

    expected = {
        Cell(x=6, y=6),
        Cell(x=7, y=4),
        Cell(x=7, y=5),
        Cell(x=8, y=4),
        Cell(x=8, y=5),
        Cell(x=9, y=4),
        Cell(x=14, y=3),
        Cell(x=14, y=6),
    }

    assert len(actual) == 8
    assert actual == expected


def test_example_02d():
    puzzle_input = [
        "FF7FSF7F7F7F7F7F---7",
        "L|LJ||||||||||||F--J",
        "FL-7LJLJ||||||LJL-77",
        "F--JF--7||LJLJ7F7FJ-",
        "L---JF-JLJ.||-FJLJJ7",
        "|F|F-JF---7F7-L7L|7|",
        "|FFJF7L7F-JF7|JL---7",
        "7-L-JL7||F7|L7F-7F7|",
        "L.L7LFJ|||||FJL7||LJ",
        "L7JLJL-JLJLJL--JLJ.L",
    ]

    puzzle_output = [
        "FF7FSF7F7F7F7F7F---7",
        "L|LJ||||||||||||F--J",
        "FL-7LJLJ||||||LJL-77",
        "F--JF--7||LJLJIF7FJ-",
        "L---JF-JLJIIIIFJLJJ7",
        "|F|F-JF---7IIIL7L|7|",
        "|FFJF7L7F-JF7IIL---7",
        "7-L-JL7||F7|L7F-7F7|",
        "L.L7LFJ|||||FJL7||LJ",
        "L7JLJL-JLJLJL--JLJ.L",
    ]

    actual = run_02(puzzle_input, first_move="S")
    expected = get_answer(puzzle_output)

    assert len(actual) == 10
    assert actual == expected


def run_02(puzzle_input, flip=False, first_move="E"):
    start_at, pipes, mx = advent.day_10.parse(puzzle_input)
    start_at, moves = advent.day_10.get_map(start_at, pipes)
    loop = advent.day_10.run_01(start_at, moves, first_move)

    return advent.day_10.run_02(pipes, loop, flip)


def get_answer(puzzle_output):
    result = set()

    for y, line in enumerate(puzzle_output):
        for x, char in enumerate(line):
            if char == "I":
                cell = Cell(x, y)
                result.add(cell)

    return result
