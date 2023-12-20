"""Advent of Code 2023, Day 20."""

import collections
import enum

from typing import Dict, List, Optional, Tuple


class Pulse(enum.Enum):
    HI = "high"
    LO = "low"
    NO = None


class Module(object):
    TYPE: str = None

    def __init__(self, name: str, outputs: List[str]):
        self.name = name
        self.outputs = outputs


class BroadcasterModule(Module):
    TYPE = "broadcaster"

    def __call__(self, src: str, pulse: Pulse) -> Pulse:
        return pulse.LO


class FlipFlopModule(Module):
    TYPE = "%"

    def __init__(self, name: str, outputs: List[str]):
        super(FlipFlopModule, self).__init__(name, outputs)

        self.state = False

    def __call__(self, src: str, pulse: Pulse) -> Pulse:
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

    def __call__(self, src: str, pulse: Pulse) -> Pulse:
        self.state[src] = pulse.value

        inputs = set(self.state.values())

        # print(f"    {src} -{pulse.value}-> [{self.name}]: {self.state}")

        if inputs == {Pulse.HI.value}:
            return Pulse.LO
        else:
            return Pulse.HI


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    modules = parse(puzzle_input)

    num_lo, num_hi = 0, 0

    for _ in range(1000):
        lo, hi, __ = run(modules, verbose=False)

        num_lo += lo
        num_hi += hi

    return num_lo * num_hi


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""

    modules = parse(puzzle_input)

    n = 0

    while True:
        n += 1
        __, __, rx = run(modules, verbose=False)

        if rx:
            break

    return n


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


def run(modules: Dict[str, Module], verbose: bool = False):
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
            if module_name == "rx" and old_pulse.value == Pulse.LO.value:
                result[module_name] = 1
                break
            continue

        new_pulse = module(src, old_pulse)

        if new_pulse.value is None:
            continue
        else:
            for dst in module.outputs:
                queue.append((module_name, dst, new_pulse))

    return (result[Pulse.LO.value], result[Pulse.HI.value], result["rx"])
