"""Common data types used in puzzles."""

from __future__ import annotations
from typing import ForwardRef, Iterator

import collections

Point = ForwardRef("Point")


class Point(collections.namedtuple("Point", "x y")):
    """2D point in a grid."""

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
