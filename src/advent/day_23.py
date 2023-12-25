"""Advent of Code 2023, Day 23."""

import collections
import itertools
import networkx
import time

from typing import Dict, List, Tuple

from advent.datatypes import Point

Maze = Dict[Point, str]
DiGraph = Dict[Point, Dict[Point, int]]

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

    return solve(puzzle_input, can_move_01)[0]


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""

    return solve(puzzle_input, can_move_02)[0]


def solve(puzzle_input: List[str], can_move: callable) -> List[int]:
    maze, start, end = parse(puzzle_input)
    graph = as_digraph(maze, start, end, can_move)

    answers = walk(graph, start, end)

    return answers


def parse(puzzle_input: List[str]) -> Tuple[Maze, Point, Point]:
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


def walk(graph: DiGraph, start: Point, end: Point) -> List[int]:
    result = set()
    x = 0

    digraph = networkx.DiGraph()

    for src, edges in graph.items():
        for dst, __ in edges.items():
            digraph.add_edge(src, dst)

    paths = networkx.all_simple_paths(digraph, start, end)

    st = time.time()

    for path in paths:
        n = cost(path, graph)

        result.add(n)

        if n > x:
            x = n
            # et = time.time() - st
            # print(f"{et: >8.1f}s {len(path)}, {n}")

    result = list(result)
    result.sort(reverse=True)

    return result


def cost(path: List[Point], graph: DiGraph) -> int:
    n = 0

    for s, e in zip(path, path[1:]):
        n += graph[s][e]

    return n


def _walk(graph: DiGraph, start: Point, end: Point) -> List[int]:
    result = []

    queue = collections.deque()
    queue.append(((start,), 0))

    # print()
    while queue:
        path, length = queue.popleft()

        p = path[-1]

        if p == end:
            result.append(length)
            continue

        for q, x in graph[p].items():
            if q in path:
                continue

            queue.append((path + (q,), length + x))

    result.sort(reverse=True)

    return result


def as_digraph(maze: Maze, start: Point, end: Point, can_move: callable) -> DiGraph:
    result = collections.defaultdict(dict)
    route_ids = itertools.count()

    queue = collections.deque()
    queue.append((start, None, start, 0, "v", next(route_ids)))

    seen = set()

    # print()

    while queue:
        h, o, p, length, d, r = queue.popleft()

        tmp = []

        seen.add((d, p))

        for b, x in MOVE.items():
            q = p + x

            if q not in maze:
                continue

            if o == q:
                continue

            if (b, q) in seen:
                continue

            if not can_move(b, p, q, maze):
                continue

            if is_intersection(q, maze):
                result[h][q] = length + 1
                # print(h, q, length + 1)

                tmp.append([q, p, q, 0, b, r])
            elif q == end:
                result[h][q] = length + 1
                # print(h, q, length + 1)
            else:
                tmp.append([h, p, q, length + 1, b, r])

        for each in tmp[1:]:
            each[-1] = next(route_ids)

        queue.extend(tmp)

    return result


def can_move_02(d: str, p: Point, q: Point, maze: Maze) -> bool:
    return True


def can_move_01(d: str, p: Point, q: Point, maze: Maze) -> bool:
    x = maze[q]

    b = {"^": "v", ">": "<", "<": ">", "v": "^", ".": "."}[d]

    if x == ".":
        return True
    else:
        return b != x


def is_intersection(p: Point, maze: Maze) -> bool:
    return all([maze[a] != "." for a in p.adjacent() if a in maze])


def pprint(route: List[Point], maze: Maze) -> None:
    mn = min(maze)
    mx = max(maze)

    lines = []

    visits = collections.Counter(route)

    for y in range(mn.y, mx.y + 1):
        line = []

        for x in range(mn.x - 1, mx.x + 2):
            p = Point(x, y)

            if p in visits and maze.get(p) == ".":
                char = f"{visits[p]:x}"
            else:
                char = maze.get(p, "#")

            line.append(char)
        lines.append("".join(line))

    print()
    print("\n".join(lines))
