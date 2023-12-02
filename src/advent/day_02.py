"""Advent of Code 2023, Day 02."""

import collections
import operator
import functools

from typing import Dict, List

Game = collections.namedtuple("Game", "id draws")
Cubes = collections.namedtuple("Draw", "red blue green")

CUBES = Cubes(red=12, blue=14, green=13)


def part_01(puzzle_input):
    """Solve part one."""

    games = map(get_results, puzzle_input)
    games = filter(functools.partial(is_game_possible, cubes=CUBES), games)

    game_ids = map(operator.attrgetter("id"), games)

    return sum(game_ids)


def part_02(puzzle_input):
    """Solve part two."""


def get_results(line: str) -> Game:
    """Return the results of the given game."""

    game, draws = line.split(":")
    draws = draws.strip().split(";")

    return Game(id=int(game.split()[-1]), draws=[get_result(draw) for draw in draws])


def get_result(draw: str) -> Cubes:
    """Return the results of the given draw."""

    result = Cubes(0, 0, 0)._asdict()

    for cubes in draw.strip().split(","):
        n, color = cubes.split()

        result[color] = int(n)

    return Cubes(**result)


def is_game_possible(game: Game, cubes: Cubes) -> bool:
    """Return True if the given game is possible."""

    return all([is_draw_possible(draw, cubes) for draw in game.draws])


def is_draw_possible(draw: Cubes, cubes: Cubes) -> bool:
    """Return True if the given draw is possible."""

    return all(
        [
            draw.red <= cubes.red,
            draw.blue <= cubes.blue,
            draw.green <= cubes.green,
        ]
    )
