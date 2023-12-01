"""Advent of Code 2023 entry script."""

import argparse


def main():
    """Solve the puzzle for the given day."""

    parser = argparse.ArgumentParser()
    parser.add_argument('day', type=int, nargs=1)

    args = parser.parse_args()
    day = '{:02d}'.format(*args.day)


if __name__ == '__main__':
    main()