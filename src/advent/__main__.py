"""Advent of Code 2023 entry script."""

import argparse
import importlib
import time

import advent


def main():
    """Solve the puzzle for the given day."""

    parser = argparse.ArgumentParser()
    parser.add_argument("days", type=str, nargs="*")

    args = parser.parse_args()

    st = time.time()

    days = []

    for day in args.days:
        if "-" in day:
            mn, mx = day.split("-")
            days.extend(range(int(mn), int(mx) + 1))
        elif "," in day:
            days.extend((int(d) for d in day.split))
        else:
            days.append(int(day))

    for day in days:
        day_name = "day_{:02d}".format(day)

        try:
            module = importlib.import_module(day_name, advent)
        except ModuleNotFoundError:
            break

        print(f"\nDay {day:02d}")
        advent.solve(day, getattr(module, "part_01", None), getattr(module, "part_02", None))

    et = time.time()

    if len(days) > 1:
        print(f"\nSolved {len(days)} puzzles in {et - st:.2f} seconds.")


if __name__ == "__main__":
    main()
