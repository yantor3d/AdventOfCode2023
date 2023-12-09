"""Advent of Code 2023, Day 05."""

import collections
import operator
import sys

from typing import Dict, Iterator, List, Tuple


class Range(collections.namedtuple("Range", "start end")):
    def __contains__(self, n: int) -> bool:
        if isinstance(n, int):
            return n >= self.start and n <= self.end
        elif isinstance(n, MapRange):
            return n.src in self
        elif isinstance(n, Range):
            return n.start in self and n.end in self
        else:
            raise TypeError(type(n).__name__)

    def __lt__(self, mr) -> bool:
        return self.start < mr.src.start and self.end < mr.src.start

    def __le__(self, mr) -> bool:
        return self.start < mr.src.start and self.end in mr.src

    def __ge__(self, mr) -> bool:
        return self.start in mr.src and self.end > mr.src.end

    def __gt__(self, mr) -> bool:
        return self.start > mr.src.end and self.end > mr.src.end


class MapRange(collections.namedtuple("MapRange", "src dst")):
    def __contains__(self, n: int) -> bool:
        if isinstance(n, int):
            return n in self.src
        elif isinstance(n, Range):
            return (n.start in self.src) and (n.end in self.src)
        else:
            raise TypeError(type(n).__name__)

    def __getitem__(self, n: int) -> int:
        if n in self:
            return self.dst.start + (n - self.src.start)
        else:
            raise ValueError(f"{n} is not in range {self.src.start}-{self.src.end}.")

    @classmethod
    def from_spec(cls, dst_range_start, src_range_start, range_len):
        return cls(
            Range(src_range_start, src_range_start + range_len - 1),
            Range(dst_range_start, dst_range_start + range_len - 1),
        )


class MapRangesList(object):
    def __init__(self, name, map_ranges: List[MapRange]):
        self.name = name
        self.map_ranges = map_ranges[:]
        self.map_ranges.sort(key=lambda mr: mr.src.start)

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


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    result = sys.maxsize

    seeds, almanac = get_data(puzzle_input)

    src_ranges = [Range(s, s) for s in seeds]
    src_ranges.sort(key=operator.attrgetter("start"))

    for __, map_ranges in almanac.items():
        src_ranges = remap(src_ranges, map_ranges)
        result = min([r.start for r in src_ranges])

    return result


def walk(value, keys, almanac):
    key = keys.pop(0)
    values = almanac[key].get_ranges(value)

    if keys:
        return {value: walk(value, keys, almanac) for value in values}
    else:
        return list(values)


def part_02(puzzle_input):
    """Solve part two."""

    result = sys.maxsize

    seeds, almanac = get_data(puzzle_input)

    src_ranges = [Range(s, s + e) for s, e in zip(seeds[::2], seeds[1::2])]
    src_ranges.sort(key=operator.attrgetter("start"))

    for __, map_ranges in almanac.items():
        src_ranges = remap(src_ranges, map_ranges)
        result = min([r.start for r in src_ranges])

    return result


def remap(src_ranges: List[Range], map_ranges: List[MapRange]) -> List[Range]:
    """Return the remapped values of the given src ranges."""

    src_ranges = collections.deque(src_ranges)
    dst_ranges = []

    while src_ranges:
        src_range = src_ranges.popleft()

        found = False

        for map_range in map_ranges:
            if src_range < map_range:
                pass
            elif src_range <= map_range:
                dst_ranges.append(
                    Range(
                        src_range.start,
                        map_range.src.start - 1,
                    )
                )

                src_ranges.append(
                    Range(
                        map_range.src.start,
                        src_range.end,
                    )
                )

                found = True
            elif src_range in map_range:
                dst_ranges.append(
                    Range(
                        map_range[src_range.start],
                        map_range[src_range.end],
                    )
                )

                found = True
            elif src_range >= map_range:
                dst_ranges.append(
                    Range(
                        map_range[src_range.start],
                        map_range.dst.end,
                    )
                )

                src_ranges.append(
                    Range(
                        map_range.src.end + 1,
                        src_range.end,
                    )
                )
                found = True
            elif src_range > map_range:
                pass
            elif map_range in src_range:
                dst_ranges.append(
                    Range(
                        map_range.dst.start,
                        map_range.dst.end,
                    )
                )
                found = True

            if found:
                break

        if not found:
            dst_ranges.append(src_range)

    dst_ranges.sort(key=operator.attrgetter("start"))

    return dst_ranges


def get_data(puzzle_input) -> Tuple[List[str], Dict[str, MapRangesList]]:
    data = parse(puzzle_input)
    seeds = data.pop("seeds")

    return seeds, {k: MapRangesList(k, v) for k, v in data.items()}


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

        map_range = MapRange.from_spec(*map(int, line.strip().split()))
        values.append(map_range)

    return key, values


def parse_seeds(line: str) -> List[int]:
    __, seeds = line.split(":")

    return [int(n) for n in seeds.strip().split()]


def get_value(n: int, map_ranges: List[MapRange]) -> int:
    return sum([each.get(n) for each in map_ranges]) or n
