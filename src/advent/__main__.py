"""Advent of Code 2023 entry script."""

import argparse
import importlib
import time

import advent


def main():
    """Solve the puzzle for the given day."""

    parser = argparse.ArgumentParser()
    parser.add_argument("days", type=int, nargs="*")

    args = parser.parse_args()

    st = time.time()

    for day in args.days:
        day_name = "day_{:02d}".format(day)

        module = importlib.import_module(day_name, advent)

        print(f"\nDay {day:02d}")
        advent.solve(day, getattr(module, "part_01", None), getattr(module, "part_02", None))

    et = time.time()

    if len(args.days) > 1:
        print(f"\nSolved {len(args.days)} puzzles in {et - st:.2f} seconds.")


if __name__ == "__main__":
    main()
