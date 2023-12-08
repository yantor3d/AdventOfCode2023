"""Advent of Code 2023, Day 08."""

import collections
import itertools
import math
import re

from typing import Dict, List, Tuple


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    result = 0

    turns, tree = parse(puzzle_input)
    old = "AAA"
    new = None

    for i, turn in enumerate(itertools.cycle(turns), 1):
        if i > 100000:
            raise RuntimeError(i)

        new = tree[old][turn]

        result = i

        if new == "ZZZ":
            break
        else:
            old = new

    return result


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""

    result = 0

    turns, tree = parse(puzzle_input)

    starts = [each for each in tree if each.endswith("A")]
    ends = [each for each in tree if each.endswith("Z")]

    old_nodes = [None] * len(starts)
    new_nodes = starts[:]

    turns = itertools.cycle(turns)
    turn = next(turns)

    at_end = [0] * len(starts)

    while True:
        result += 1
        old_nodes, new_nodes = next_02(tree, turn, old_nodes, new_nodes)

        for i, node in enumerate(new_nodes):
            if node in ends:
                at_end[i] = result

        if all(at_end):
            break

        turn = next(turns)

    (gcd,) = {math.gcd(a, b) for a, b in itertools.combinations(at_end, 2)}
    factors = [end // gcd for end in at_end]

    return gcd * math.prod(factors)


def next_02(tree: Dict, turn: str, old_nodes: List[str], new_nodes: List[str]) -> List[str]:
    for i, old in enumerate(new_nodes):
        new = tree[old][turn]
        old_nodes[i], new_nodes[i] = old, new

    return old_nodes, new_nodes


def parse(puzzle_input: List[str]) -> Tuple[List[str], Dict]:
    turns = []
    tree = {}

    lines = iter(puzzle_input)

    turns = next(lines).strip()
    next(lines)

    for line in lines:
        tree.update(parse_line(line))

    return turns, tree


def parse_line(line: str) -> Dict:
    name, lf, rt = re.findall(r"\w{3}", line)

    return {name: {"L": lf, "R": rt}}
