"""Advent of Code 2023, Day 25."""

import collections
import itertools
import math
import networkx
import random

from typing import Dict, FrozenSet, List, Set, Tuple


class Edge(frozenset):
    def __repr__(self) -> str:
        return "/".join(sorted(self))


Node = str
Nodes = Dict[Node, Set[Node]]


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    nodes = parse(puzzle_input)

    return solve_01(nodes)


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""


def solve_01(nodes: Nodes) -> int:
    graph = networkx.Graph()

    for curr_node, next_nodes in nodes.items():
        for next_node in next_nodes:
            graph.add_edge(curr_node, next_node)

    graph.remove_edges_from(networkx.minimum_edge_cut(graph))

    subnets = networkx.connected_components(graph)

    return math.prod(map(len, subnets))


def parse(puzzle_input: List[str]) -> Nodes:
    nodes = collections.defaultdict(set)

    for line in puzzle_input:
        a, bs = line.split(": ")

        for b in bs.split(" "):
            nodes[a].add(b)
            nodes[b].add(a)

    return nodes


def min_cut(nodes: Nodes) -> List[Set[Node]]:
    graph = networkx.Graph()

    for curr_node, next_nodes in nodes.items():
        for next_node in next_nodes:
            graph.add_edge(curr_node, next_node)

    graph.remove_edges_from(networkx.minimum_edge_cut(graph))

    result = [set(cc) for cc in networkx.connected_components(graph)]
    result.sort(key=len)

    return result
