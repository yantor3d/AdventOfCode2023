"""Advent of Code 2023, Day 20."""

import collections
import itertools
import math
import enum

from typing import Dict, List


START = "broadcaster"


class Pulse(enum.Enum):
    HI = True
    LO = False
    NO = None


class Module(object):
    TYPE: str = None

    def __init__(self, name: str, outputs: List[str]):
        self.name = name
        self.outputs = outputs

    def __str__(self) -> str:
        return f"{self.TYPE}{self.name}"

    def __repr__(self) -> str:
        return str(self)

    def reset(self):
        pass


class BroadcasterModule(Module):
    TYPE = "broadcaster"

    def __call__(self, src: str, pulse: Pulse, n: int) -> Pulse:
        return pulse.LO

    def __str__(self) -> str:
        return self.name


class FlipFlopModule(Module):
    TYPE = "%"

    def __init__(self, name: str, outputs: List[str]):
        super(FlipFlopModule, self).__init__(name, outputs)

        self.state = False

    def __call__(self, src: str, pulse: Pulse, n: int) -> Pulse:
        if pulse.value == Pulse.HI.value:
            return Pulse.NO
        else:
            self.state, result = not self.state, Pulse.LO if self.state else Pulse.HI
            return result


class ConjunctionModule(Module):
    TYPE = "&"

    def __init__(self, name: str, outputs: List[str]):
        super(ConjunctionModule, self).__init__(name, outputs)

        self.state = {}
        self.state_cache = {}

    def __call__(self, src: str, pulse: Pulse, n: int) -> Pulse:
        self.state[src] = pulse.value

        if pulse.value and src not in self.state_cache:
            self.state_cache[src] = n

        if all(self.state.values()):
            result = Pulse.LO
        else:
            result = Pulse.HI

        return result


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    modules = parse(puzzle_input)

    num_lo, num_hi = 0, 0

    for _ in range(1000):
        lo, hi = run(modules, verbose=False)

        num_lo += lo
        num_hi += hi

    return num_lo * num_hi


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""

    end = "rx"

    modules = parse(puzzle_input)

    cycles = []

    for start in modules[START].outputs:
        subnet = get_subnet(puzzle_input, start)

        cycle = unroll(subnet, end)
        cycles.append(cycle)

    return math.prod(cycles)


def parse(puzzle_input: List[str]) -> Dict[str, Module]:
    result = {}

    for line in puzzle_input:
        name, out = line.split(" -> ")
        outputs = out.split(", ")

        if name == "broadcaster":
            module_type = None
        else:
            module_type, name = name[0], name[1:]

        if module_type == "%":
            klass = FlipFlopModule
        elif module_type == "&":
            klass = ConjunctionModule
        else:
            klass = BroadcasterModule

        result[name] = klass(name, outputs)

    for src, src_module in result.items():
        for out in src_module.outputs:
            try:
                dst_module = result[out]
            except KeyError:
                pass
            else:
                if dst_module.TYPE == ConjunctionModule.TYPE:
                    dst_module.state[src] = Pulse.LO.value

    return result


def run(modules: Dict[str, Module], n: int = 1, verbose: bool = False):
    result = collections.Counter()

    queue = collections.deque()
    queue.append(("button", "broadcaster", Pulse.LO))

    if verbose:
        print()

    while queue:
        src, module_name, old_pulse = queue.popleft()

        result[old_pulse.value] += 1

        if verbose:
            print(f"{src} -{old_pulse.value}-> {module_name}")

        try:
            module = modules[module_name]
        except KeyError:
            continue

        new_pulse = module(src, old_pulse, n)

        if new_pulse.value is None:
            continue
        else:
            for dst in module.outputs:
                queue.append((module_name, dst, new_pulse))

    return (
        result[Pulse.LO.value],
        result[Pulse.HI.value],
    )


def unroll(subnet: Dict[str, Module], end: str) -> int:
    (join,) = [module for module in subnet.values() if end in module.outputs]

    for i in itertools.count(1):
        run(subnet, i)

        if any(join.state_cache):
            break

    return i


def get_subnet(puzzle_input, start):
    modules = parse(puzzle_input)

    seen = {}

    queue = collections.deque([start])

    while queue:
        node = queue.popleft()

        if node in seen:
            continue

        seen[node] = None

        try:
            module = modules[node]
        except KeyError:
            pass

        for out in module.outputs:
            queue.append(out)

    result = {name: module for name, module in modules.items() if name in seen}
    result[START] = BroadcasterModule(START, [start])

    return result
