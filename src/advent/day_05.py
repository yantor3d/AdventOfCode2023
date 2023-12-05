"""Advent of Code 2023, Day 05."""

import collections

from typing import Dict, Iterator, List, Tuple

# TODO:
# Impl MapRange.__getitem__(int) -> int, raises IndexError if out of bounds
# Impl MapRangeList.__getitem__(int) -> int

AlmanacEntry = collections.namedtuple(
    "AlmanacEntry", "seed soil fertilizer water light temperature humidity location"
)


class MapRange(collections.namedtuple("MapRange", "dst_range_start src_range_start range_len")):
    def __getitem__(self, n: int) -> int:
        result = 0

        if (self.src_range_start <= n) and (n <= (self.src_range_start + self.range_len)):
            result = self.dst_range_start + (n - self.src_range_start)

        return result


class MapRangesList(object):
    def __init__(self, map_ranges: List[MapRange]):
        self.map_ranges = map_ranges

    def __iter__(self):
        return iter(self.map_ranges)

    def __getitem__(self, n):
        return sum([each[n] for each in self]) or n


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    seeds, almanac = get_almanac(puzzle_input)

    entry_list = [get_almanac_entry(seed, almanac) for seed in seeds]
    locations = [each.location for each in entry_list]

    return min(locations)


def part_02(puzzle_input):
    """Solve part two."""


def get_almanac(puzzle_input):
    data = parse(puzzle_input)
    seeds = data.pop("seeds")

    return seeds, {k: MapRangesList(v) for k, v in data.items()}


def get_almanac_entry(seed: int, data: dict) -> AlmanacEntry:
    """Return the AlmanacEntry for the given seed."""

    soil = data["seed-to-soil"][seed]
    fertilizer = data["soil-to-fertilizer"][soil]
    water = data["fertilizer-to-water"][fertilizer]
    light = data["water-to-light"][water]
    temp = data["light-to-temperature"][light]
    humidity = data["temperature-to-humidity"][temp]
    location = data["humidity-to-location"][humidity]

    return AlmanacEntry(seed, soil, fertilizer, water, light, temp, humidity, location)


def parse(puzzle_input: List[str]) -> Dict:
    """Parse the puzzle input."""

    lines = iter(puzzle_input)

    result = {}
    result["seeds"] = parse_seeds(next(lines))

    next(lines)

    while True:
        try:
            key, values = parse_map(lines)
        except StopIteration:
            break
        else:
            result[key] = values

    return result


def parse_map(lines: Iterator[str]) -> Tuple[str, List[MapRange]]:
    key = next(lines)
    key, __ = key.split(" ")

    values = []

    for line in lines:
        line = line.strip()

        if not line:
            break

        map_range = MapRange(*map(int, line.strip().split()))

        values.append(map_range)

    return key, values


def parse_seeds(line: str) -> List[int]:
    __, seeds = line.split(":")

    return [int(n) for n in seeds.strip().split()]


def get_value(n: int, map_ranges: List[MapRange]) -> int:
    return sum([each.get(n) for each in map_ranges]) or n
