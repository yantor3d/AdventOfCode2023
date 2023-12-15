"""Test suite for Day 14."""

import pytest

import advent.day_14


@pytest.fixture()
def puzzle_input():
    return [
        "O....#....",
        "O.OO#....#",
        ".....##...",
        "OO.#O....O",
        ".O.....O#.",
        "O.#..O.#.#",
        "..O..#O..O",
        ".......O..",
        "#....###..",
        "#OO..#....",
    ]


def test_rotate():
    old = ["#.O", "##.", "..#"]

    new = [
        ".##",
        ".#.",
        "#.O",
    ]

    tmp = advent.day_14.unpack(old)
    out = advent.day_14.rotate_cw(tmp)
    out = advent.day_14.repack(out)

    assert out == new

    tmp = advent.day_14.unpack(new)
    out = advent.day_14.rotate_ccw(tmp)
    out = advent.day_14.repack(out)

    assert out == old


def test_mirror_h():
    old = ["#.O", "##.", "..#"]

    new = [
        "O.#",
        ".##",
        "#..",
    ]

    tmp = advent.day_14.unpack(old)
    out = advent.day_14.mirror_h(tmp)
    out = advent.day_14.repack(out)

    assert out == new

    tmp = advent.day_14.unpack(new)
    out = advent.day_14.mirror_h(tmp)
    out = advent.day_14.repack(out)

    assert out == old


def test_mirror_v():
    old = ["#.O", "##.", "..#"]

    new = [
        "..#",
        "##.",
        "#.O",
    ]

    tmp = advent.day_14.unpack(old)
    out = advent.day_14.mirror_v(tmp)
    out = advent.day_14.repack(out)

    assert out == new

    tmp = advent.day_14.unpack(new)
    out = advent.day_14.mirror_v(tmp)
    out = advent.day_14.repack(out)

    assert out == old


@pytest.mark.parametrize(
    "old,new",
    (
        ("OO.O.O..##", "OOOO....##"),
        ("...OO....O", "OOO......."),
        (".O...#O..O", "O....#OO.."),
        (".#.O......", ".#O......."),
        ("#.#..O#.##", "#.#O..#.##"),
        ("..#...O.#.", "..#O....#."),
        ("....O#.O#.", "O....#O.#."),
        ("....#.....", "....#....."),
        (".#.O.#O...", ".#O..#O..."),
    ),
)
def test_roll(old, new):
    out = advent.day_14.roll(old)

    assert out == tuple(new)


def test_tilt_n(puzzle_input):
    old = advent.day_14.unpack(puzzle_input)
    new = advent.day_14.tilt_n(old)
    new = advent.day_14.repack(new)

    assert new == [
        "OOOO.#.O..",
        "OO..#....#",
        "OO..O##..O",
        "O..#.OO...",
        "........#.",
        "..#....#.#",
        "..O..#.O.O",
        "..O.......",
        "#....###..",
        "#....#....",
    ]


def test_tilt_e(puzzle_input):
    old = advent.day_14.unpack(puzzle_input)
    new = advent.day_14.tilt_e(old)
    new = advent.day_14.repack(new)

    assert new == [
        "....O#....",
        ".OOO#....#",
        ".....##...",
        ".OO#....OO",
        "......OO#.",
        ".O#...O#.#",
        "....O#..OO",
        ".........O",
        "#....###..",
        "#..OO#....",
    ]


def test_tilt_s(puzzle_input):
    old = advent.day_14.unpack(puzzle_input)
    new = advent.day_14.tilt_s(old)
    new = advent.day_14.repack(new)

    assert new == [
        ".....#....",
        "....#....#",
        "...O.##...",
        "...#......",
        "O.O....O#O",
        "O.#..O.#.#",
        "O....#....",
        "OO....OO..",
        "#OO..###..",
        "#OO.O#...O",
    ]


def test_tilt_w(puzzle_input):
    old = advent.day_14.unpack(puzzle_input)
    new = advent.day_14.tilt_w(old)
    new = advent.day_14.repack(new)

    assert new == [
        "O....#....",
        "OOO.#....#",
        ".....##...",
        "OO.#OO....",
        "OO......#.",
        "O.#O...#.#",
        "O....#OO..",
        "O.........",
        "#....###..",
        "#OO..#....",
    ]


def test_part_01(puzzle_input):
    answer = advent.day_14.part_01(puzzle_input)

    assert answer == 136


def test_spin_1(puzzle_input):
    grid = advent.day_14.unpack(puzzle_input)
    grid = advent.day_14.spin(grid)
    grid = advent.day_14.repack(grid)

    assert grid == [
        ".....#....",
        "....#...O#",
        "...OO##...",
        ".OO#......",
        ".....OOO#.",
        ".O#...O#.#",
        "....O#....",
        "......OOOO",
        "#...O###..",
        "#..OO#....",
    ]


def test_spin_2(puzzle_input):
    grid = advent.day_14.unpack(puzzle_input)
    grid = advent.day_14.spin(grid)
    grid = advent.day_14.spin(grid)
    grid = advent.day_14.repack(grid)

    assert grid == [
        ".....#....",
        "....#...O#",
        ".....##...",
        "..O#......",
        ".....OOO#.",
        ".O#...O#.#",
        "....O#...O",
        ".......OOO",
        "#..OO###..",
        "#.OOO#...O",
    ]


def test_spin_3(puzzle_input):
    grid = advent.day_14.unpack(puzzle_input)
    grid = advent.day_14.spin(grid)
    grid = advent.day_14.spin(grid)
    grid = advent.day_14.spin(grid)
    grid = advent.day_14.repack(grid)

    assert grid == [
        ".....#....",
        "....#...O#",
        ".....##...",
        "..O#......",
        ".....OOO#.",
        ".O#...O#.#",
        "....O#...O",
        ".......OOO",
        "#...O###.O",
        "#.OOO#...O",
    ]


def test_part_02(puzzle_input):
    answer = advent.day_14.part_02(puzzle_input)

    assert answer == 64
