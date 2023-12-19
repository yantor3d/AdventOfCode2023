"""Advent of Code 2023, Day 19."""

from __future__ import annotations

import collections
import operator
import re

from typing import Dict, List, Tuple

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
    def __init__(self, attr: str = "", op: callable = None, value: int = 0, out: str = "") -> None:
        self.attr = attr
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

            return cls(attr, OPERATORS[op], int(value), out)
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
