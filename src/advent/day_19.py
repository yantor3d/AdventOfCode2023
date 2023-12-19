"""Advent of Code 2023, Day 19."""

from __future__ import annotations

import math
import collections
import operator
import re

from typing import Dict, Iterator, List, Tuple

OPERATORS = {
    "<": operator.lt,
    ">": operator.gt,
}


class Part(dict):
    def score(self) -> int:
        return sum(self.values())

    @classmethod
    def from_string(cls, data) -> Part:
        result = {}

        for pair in data[1:-1].split(","):
            k, v = pair.split("=")
            result[k] = int(v)

        return cls(result)


class Filter(object):
    def __init__(
        self,
        attr: str = "",
        op_code: str = None,
        op: callable = None,
        value: int = 0,
        out: str = "",
    ) -> None:
        self.attr = attr
        self.op_code = op_code
        self.op = op
        self.value = value
        self.out = out

    @classmethod
    def nop(cls, out: str) -> Filter:
        return Filter(out=out)

    @classmethod
    def from_string(cls, line: str) -> Filter:
        try:
            check, out = line.split(":")

            if "<" in check:
                op = "<"
            elif ">" in check:
                op = ">"

            attr, value = check.split(op)

            return cls(attr, op, OPERATORS[op], int(value), out)
        except ValueError:
            return cls.nop(line)

    def __call__(self, part: Part) -> bool:
        if self.op is None:
            return True
        else:
            return self.op(part[self.attr], self.value)


class Workflow(object):
    def __init__(self, name: str, filters: List[Filter]) -> None:
        self.name = name
        self.filters = filters

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Workflow):
            return self.name == other.name
        else:
            return False

    def __hash__(self) -> int:
        return hash(self.name)

    @classmethod
    def from_string(cls, data) -> Workflow:
        name, data = data[:-1].split("{")

        return cls(name, [Filter.from_string(each) for each in data.split(",")])


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    workflows, parts = parse(puzzle_input)

    accepted = run(workflows, parts)

    return score(accepted)


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""

    workflows, __ = parse(puzzle_input)

    r = (1, 4000)
    max_range = {"x": r, "m": r, "a": r, "s": r}

    result = tree(workflows, "in", max_range)

    n = 0

    for pr in result:
        rs = [r[1] - r[0] + 1 for r in pr.values()]
        n += math.prod(rs)

    return n


def tree(
    workflows: Dict[str, Workflow],
    out: str,
    pr: Dict[str, Tuple[int, int]],
    depth: int = 0,
    max_depth: int = -1,
) -> Iterator[Dict[str, Tuple[int, int]]]:
    if max_depth >= 0 and depth > max_depth:
        return

    if out == "A":
        yield pr
        return

    if out == "R":
        return

    wf = workflows[out]

    for f in wf.filters:
        if f.op_code is None:
            yield from tree(workflows, f.out, pr, depth + 1, max_depth)
        elif f.op_code == "<":
            n, m = pr[f.attr]

            if n < f.value:
                nr = dict(pr)
                nr[f.attr] = (n, f.value - 1)

                yield from tree(workflows, f.out, nr, depth + 1, max_depth)

                pr[f.attr] = (f.value, m)

        elif f.op_code == ">":
            n, m = pr[f.attr]

            if m > f.value:
                nr = dict(pr)
                nr[f.attr] = (f.value + 1, m)

                yield from tree(workflows, f.out, nr, depth + 1, max_depth)

                pr[f.attr] = (n, f.value)


def parse(puzzle_input: List[str]) -> Tuple[Dict[str, Workflow], List[Part]]:
    workflows = []
    parts = []

    dst = workflows
    fac = Workflow

    for line in puzzle_input:
        if line:
            dst.append(fac.from_string(line))
        else:
            dst = parts
            fac = Part

    workflows = {wf.name: wf for wf in workflows}

    return workflows, parts


def run(workflows: Dict[str, Workflow], parts: List[Part]) -> List[Part]:
    return [part for part in parts if accepted(workflows, part)]


def accepted(workflows: Dict[str, Workflow], part: Part) -> bool:
    out = "in"

    while True:
        workflow = workflows[out]

        for f in workflow.filters:
            if f(part):
                out = f.out
                break
        else:
            raise RuntimeError("Impossible")

        if out in "AR":
            break

    return out == "A"


def score(parts: List[Part]) -> int:
    return sum(map(operator.methodcaller("score"), parts))
