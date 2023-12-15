"""Advent of Code 2023, Day 15."""

import collections
import itertools

from typing import Dict, List, Tuple


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    hashes = map(hash_of, parse(puzzle_input))

    return sum(hashes)


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""

    steps = parse(puzzle_input)

    hashmap = collections.defaultdict(dict)

    for step in steps:
        label, op, lens_id = unpack(step)

        key = hash_of(label)

        if op == "=":
            hashmap[key][label] = lens_id

        if op == "-":
            hashmap[key].pop(label, None)

    powers = itertools.starmap(focusing_power, hashmap.items())

    return sum(powers)


def pprint(hashmap: Dict[str, Dict[str, int]]):
    for n, lenses in sorted(hashmap.items()):
        if not lenses:
            continue

        lenses = [f"[{name} {fl}]" for name, fl in lenses.items()]

        print(f"Box {n}: {' '.join(lenses)}")


def focusing_power(box_number: int, lenses: Dict[str, int]) -> int:
    result = 0

    for i, fl in enumerate(lenses.values(), 1):
        result += (box_number + 1) * i * fl

    return result


def parse(puzzle_input: List[str]) -> List[str]:
    result = []

    for line in puzzle_input:
        result.extend(line.split(","))

    return result


def unpack(chars: str) -> Tuple[str, str, int]:
    if "=" in chars:
        sep = "="
    elif "-" in chars:
        sep = "-"

    label, op, focal_length = chars.partition(sep)

    return label, op, int(focal_length) if focal_length else None


def hash_of(chars: str):
    result = 0

    for char in chars:
        result += ord(char)
        result *= 17
        result %= 256

    return result
