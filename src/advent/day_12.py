"""Advent of Code 2023, Day 12."""

import collections
import functools
import itertools

from typing import Iterator, List, Set, Tuple


def part_01(puzzle_input: List[str]) -> int:
    """Solve part one."""

    values = parse(puzzle_input)

    n = 0

    for line, blocks in values:
        n += num_solutions(line + ".", blocks)

    return n


def part_02(puzzle_input: List[str]) -> int:
    """Solve part two."""

    values = parse(puzzle_input)

    n = 0

    for line, blocks in values:
        line, blocks = unfold(line, blocks)
        n += num_solutions(line + ".", blocks)

    return n


def unfold(line: str, blocks: Tuple[int], n: int = 5) -> Tuple[str, Tuple[int]]:
    return ("?".join([line] * n), blocks * n)


def parse(puzzle_input: List[str]) -> List:
    result = []

    for line in puzzle_input:
        line, numbers = line.split()

        blocks = tuple(map(int, numbers.split(",")))

        result.append((line, blocks))

    return result


def num_solutions(line: str, blocks: Tuple[int]) -> int:
    @functools.cache
    def fn(start, block_num, count=0):
        end_of_line = start == len(line)

        if end_of_line:
            return int(block_num == len(blocks))

        end_of_block = line[start] in ".?"

        if end_of_block:
            count += fn(start + 1, block_num)

        end_of_blocks = block_num == len(blocks)

        if end_of_blocks:
            pass
        else:
            end = start + blocks[block_num]

            try:
                start_of_block = line[start] in "#?"
                can_fit_block = "." not in line[start:end]
                can_end_block = line[end] in ".?"
            except IndexError:
                pass
            else:
                if start_of_block and can_fit_block and can_end_block:
                    count += fn(end + 1, block_num + 1)

        return count

    return fn(0, 0)
