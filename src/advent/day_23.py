"""Advent of Code 2023, Day 23."""

import collections

from typing import Dict, List, Tuple

from advent.datatypes import Point

# Compute path segments as branches - eg 1,0: (4,5, 3,6)
# Get lengths of all routes, return highest

Route = collections.namedtuple("Route", "start end steps turns")

N = Point(+0, -1)
S = Point(+0, +1)
E = Point(+1, +0)
W = Point(-1, +0)

MOVE = {
    ">": E,
    "^": N,
    "v": S,
    "<": W,
}

MOVES = {
    ">": ">^v",
    "^": "^<>",
    "v": "v<>",
    "<": "<^v",
}


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    maze, start, end = parse(puzzle_input)

    routes_map = get_route_map(maze, start, end)
    routes = get_routes(routes_map, start)
    routes.sort(reverse=True)

    return routes[0]


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""


def parse(puzzle_input: List[str]) -> Tuple[Dict[Point, str], Point, Point]:
    result = {}

    for y, row in enumerate(puzzle_input):
        for x, col in enumerate(row):
            if col == "#":
                continue

            p = Point(x, y)

            result[p] = col

    start = min(result)
    end = max(result)

    return result, start, end


def get_routes(routes_map: Dict[Point, Dict[Point, int]], start: Point) -> List[int]:
    queue = collections.deque()
    queue.append((start, 0))

    result = []

    while queue:
        p, x = queue.popleft()

        try:
            turns = routes_map[p]
        except KeyError:
            result.append(x - 1)
        else:
            for t, n in turns.items():
                queue.append((t, x + n))

    return result


def get_route_map(
    puzzle: Dict[Point, str], start: Point, end: Point
) -> Dict[Point, Dict[Point, int]]:
    result = collections.defaultdict(dict)

    for route in route_segments(puzzle, "v", start, end):
        for turn in route.turns:
            result[route.start][turn] = route.steps

    return dict(result)


def route_segments(
    puzzle: Dict[Point, str], d: str, start: Point, end: Point
) -> List[Tuple[Point, int]]:
    result = [start]

    while True:
        p = result[-1]

        adj = adjacent(p, d, puzzle)

        if len(adj) == 1:
            ((a, b),) = adj.items()

            result.append(a)

            if a == end:
                yield as_route(result, [a])
                break
            else:
                d = b
        else:
            yield as_route(result, adj.keys())

            for a, b in adj.items():
                yield from route_segments(puzzle, b, a, end)

            break


def as_route(steps: List[Point], turns: List[Point]) -> Route:
    return Route(steps[0], steps[-1], len(steps), list(turns))


def adjacent(p: Point, d: str, puzzle: Dict[Point, str]) -> Dict[Point, str]:
    result = {}
    moves = MOVES[d]

    for b in moves:
        m = MOVE[b]
        q = p + m

        x = puzzle.get(q)

        if x == "." or x == b:
            result[q] = b

    return result
