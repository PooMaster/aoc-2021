import re
from operator import methodcaller
from collections import Counter
from dataclasses import dataclass
from typing import Iterable

@dataclass
class Line:
    x1: int
    y1: int
    x2: int
    y2: int

    def is_orthogonal(self) -> bool:
        return self.x1 == self.x2 or self.y1 == self.y2

    def points(self) -> Iterable[tuple[int, int]]:
        """
        Generate points that make up this line as tuples.
        """
        def auto_range(a, b):
            step = 1 if a < b else -1
            return range(a, b+step, step)

        if self.x1 == self.x2:
            # Generate along the y axis
            yield from ((self.x1, y) for y in auto_range(self.y1, self.y2))
        elif self.y1 == self.y2:
            # Generate along the x axis
            yield from ((x, self.y1) for x in auto_range(self.x1, self.x2))
        else:
            # Assume diagonal?
            yield from zip(auto_range(self.x1, self.x2), auto_range(self.y1, self.y2))

    @staticmethod
    def from_str(input: str):
        match = re.match(r"(\d+),(\d+) -> (\d+),(\d+)", input)
        ints = map(int, match.groups())
        return Line(*ints)

    def __str__(self) -> str:
        return "{x1},{y1} -> {x2},{y2}".format_map(self.__dict__)

if __name__ == '__main__':
    lines = [Line.from_str(s) for s in open('input.txt')]

    # Part 1
    orthogonal_lines = [l for l in lines if l.is_orthogonal()]

    overlaps = Counter()
    for line in orthogonal_lines:
        overlaps.update(line.points())
    
    at_least_two = [k for k, v in overlaps.items() if v >= 2]
    print('Part 1:')
    print(len(at_least_two))

    # Part 2
    overlaps = Counter()
    for line in lines:
        overlaps.update(line.points())

    at_least_two = [k for k, v in overlaps.items() if v >= 2]
    print('Part 2:')
    print(len(at_least_two))
