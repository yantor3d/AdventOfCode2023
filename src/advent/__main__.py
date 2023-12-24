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
    t01s = []
    t02s = []

    n = 0

    for day in args.days or ["1-25"]:
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
        except ModuleNotFoundError as exc:
            print(str(exc))
            break

        print(f"\nDay {day:02d}")
        a01, a02 = advent.solve(
            day, getattr(module, "part_01", None), getattr(module, "part_02", None)
        )

        if a01.value is not None:
            t01s.append(a01.time)

        if a02.value is not None:
            t02s.append(a02.time)

        n += 1

    et = time.time()

    if n > 1:
        print(f"\nSolved {n} puzzles in {et - st:.3f} seconds.")
        print(
            f"\tPart 01 min: {min(t01s):.3f}s max: {max(t01s):.3f}s average: {sum(t01s) / float(len(t01s)):.3f}s"
        )
        print(
            f"\tPart 02 min: {min(t02s):.3f}s max: {max(t02s):.3f}s average: {sum(t02s) / float(len(t02s)):.3f}s"
        )


if __name__ == "__main__":
    main()
