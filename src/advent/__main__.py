"""Advent of Code 2023 entry script."""

import argparse
import importlib

import advent


def main():
    """Solve the puzzle for the given day."""

    parser = argparse.ArgumentParser()
    parser.add_argument("day", type=int, nargs=1)

    args = parser.parse_args()

    day = args.day[0]
    day_name = "day_{:02d}".format(*args.day)

    module = importlib.import_module(day_name, advent)

    advent.solve(day, getattr(module, "part_01", None), getattr(module, "part_02", None))


if __name__ == "__main__":
    main()
