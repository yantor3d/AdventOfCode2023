"""Common data types used in puzzles."""

from __future__ import annotations
from typing import ForwardRef, Iterator

import collections

Point = ForwardRef("Point")


class Point(collections.namedtuple("Point", "x y")):
    """2D point in a grid."""

    def __str__(self) -> str:
        return f"<{self.x},{self.y}>"

    def __repr__(self) -> str:
        return str(self)

    def __add__(self, other: Point) -> Point:
        if not isinstance(other, Point):
            raise TypeError()

        return Point(self.x + other.x, self.y + other.y)

    def adjacent(self) -> Iterator[Point]:
        """Yield the points adjacent to this one in a grid."""

        yield Point(self.x + 1, self.y + 0)
        yield Point(self.x - 1, self.y + 0)
        yield Point(self.x + 0, self.y + 1)
        yield Point(self.x + 0, self.y - 1)

    def neighbors(self) -> Iterator[Point]:
        """Yield the points neighboring this one in a grid."""

        yield Point(self.x + 1, self.y + 1)
        yield Point(self.x - 0, self.y + 1)
        yield Point(self.x - 1, self.y + 1)

        yield Point(self.x + 1, self.y + 0)
        yield Point(self.x - 1, self.y + 0)

        yield Point(self.x + 1, self.y - 1)
        yield Point(self.x + 0, self.y - 1)
        yield Point(self.x - 1, self.y - 1)
