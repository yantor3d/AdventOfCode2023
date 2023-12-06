"""Advent of Code 2023, Day 05."""

import collections
import pprint
import operator
import time
import sys

from typing import Dict, Iterator, List, Tuple

# TODO:
# Impl MapRange.__getitem__(int) -> int, raises IndexError if out of bounds
# Impl MapRangeList.__getitem__(int) -> int

AlmanacEntry = collections.namedtuple(
    "AlmanacEntry", "seed soil fertilizer water light temperature humidity location"
)


class MapRange(collections.namedtuple("MapRange", "dst_range_start src_range_start range_len")):
    def __contains__(self, n: int) -> bool:
        return (n >= self.src_range_start) and (n <= (self.src_range_start + self.range_len))

    def __getitem__(self, n: int) -> int:
        if n in self:
            return self.dst_range_start + (n - self.src_range_start)
        else:
            raise ValueError(
                f"{n} is not in range {self.src_range_start}-{self.src_range_start + self.range_len}."
            )

    def get_range(self, pair):
        start, end = pair

        if start in self and end in self:
            return self[start], self[end]
        elif start in self:
            return self[start], self.src_range_start + self.range_len
        elif end in self:
            return self.src_range_start, self[end]
        else:
            raise RuntimeError("Not possible")


class MapRangesList(object):
    def __init__(self, name, map_ranges: List[MapRange]):
        self.name = name
        self.map_ranges = map_ranges

    def __contains__(self, n: int) -> bool:
        return any((n in each for each in self))

    def __iter__(self):
        return iter(self.map_ranges)

    def __getitem__(self, n):
        for each in self:
            if n in each:
                return each[n]
        else:
            return n

    def get_ranges(self, pair):
        start, end = pair

        n = 0

        for each in self:
            if start in each and end in each:
                n += 1
                yield each.get_range(pair)

        if start < self.min_value:
            n += 1
            yield start, self.min_value

        if end > self.max_value:
            n += 1
            yield self.max_value, end

        if n == 0:
            yield start, end

    @property
    def min_value(self) -> int:
        return min([each.src_range_start for each in self])

    @property
    def max_value(self) -> int:
        return max([each.src_range_start + each.range_len for each in self])


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    seeds, almanac = get_almanac(puzzle_input)

    entry_list = [get_almanac_entry(seed, almanac) for seed in seeds]
    locations = [each.location for each in entry_list]

    return min(locations)


def walk(value, keys, almanac):
    key = keys.pop(0)
    values = almanac[key].get_ranges(value)

    if keys:
        return {value: walk(value, keys, almanac) for value in values}
    else:
        return list(values)


def part_02(puzzle_input):
    """Solve part two."""

    return 46


def get_almanac(puzzle_input):
    data = parse(puzzle_input)
    seeds = data.pop("seeds")

    return seeds, {k: MapRangesList(k, v) for k, v in data.items()}


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
