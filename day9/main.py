import heapq
import operator
from functools import reduce
from collections import namedtuple
from typing import Iterable


class Pos(namedtuple("Pos", "x, y")):
    def __add__(self, other: "Pos"):
        return Pos(self.x + other.x, self.y + other.y)


def neighbor_positions(pos: Pos, grid: dict[Pos, int]) -> Iterable[Pos]:
    deltas = [
        Pos(-1, 0),
        Pos(0, -1),
        Pos(1, 0),
        Pos(0, 1),
    ]
    for d in deltas:
        neighbor_pos = pos + d
        if neighbor_pos in grid:
            yield neighbor_pos


def grow_basin(pos: Pos, grid: dict[Pos, int]) -> set[Pos]:
    """
    Iteratively find non-9 neighbors of pos until a full basin in built.
    """
    basin: set[Pos] = {pos}
    unvisited: set[Pos] = set(neighbor_positions(pos, grid))
    while unvisited:
        next_pos: Pos = unvisited.pop()
        if grid[next_pos] == 9:
            continue
        basin.add(next_pos)
        new_neighbors: set[Pos] = set(neighbor_positions(next_pos, grid)) - unvisited - basin
        unvisited.update(new_neighbors)
    return basin


def prod(nums):
    return reduce(operator.mul, nums, 1)


if __name__ == '__main__':
    content: str = open('input.txt').read()
    grid = {
        Pos(x, y): int(char) for y, line in enumerate(content.strip().splitlines())
        for x, char in enumerate(line)
    }

    # Part 1
    low_points = [
        pos for pos, value in grid.items()
        if all(value < grid[other] for other in neighbor_positions(pos, grid))
    ]
    print('Part 1:')
    print(sum(grid[pos] + 1 for pos in low_points))

    # Part 2
    # Get all of the non-9 valued positions
    # Make a set of all the positions that haven't been assigned to a basin yet
    unassigned_positions = {
        pos for pos, value in grid.items() if value != 9
    }

    # For each unassigned position, grow one of the positions into a full basin
    # until all of the positions have been assigned
    basins = []
    while unassigned_positions:
        pos = unassigned_positions.pop()
        basin = grow_basin(pos, grid)
        unassigned_positions -= basin
        basins.append(basin)

    three_largest = heapq.nlargest(3, map(len, basins))
    print('Part 2:')
    print(prod(three_largest))
