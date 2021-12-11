from collections import namedtuple
import itertools


class Pos(namedtuple("Pos", "x, y")):
    def __add__(self, other: "Pos"):
        return Pos(self.x + other.x, self.y + other.y)


def neighbors(pos, grid):
    for x, y in itertools.product([-1, 0, 1], repeat=2):
        if x == 0 and y == 0:
            continue
        n = pos + Pos(x ,y)
        if n not in grid:
            continue
        yield n


def inc(grid, pos):
    if grid[pos] < 10:
        grid[pos] = grid[pos] + 1


def step_forward(grid):
    # Increment all by one
    for pos in grid:
        inc(grid, pos)

    # print()
    # print_grid(grid)

    # Find all nines
    done_flashes = set()
    flashes = set(find_flashes(grid))
    while flashes:
        for n in flashes:
            for p in set(neighbors(n, grid)):
                inc(grid, p)
        done_flashes.update(flashes)
        flashes = set(find_flashes(grid)) - done_flashes

        # print()
        # print_grid(grid)

    for pos in grid:
        if grid[pos] == 10:
            grid[pos] = 0


def find_flashes(grid):
    return (pos for pos, val in grid.items() if val == 10)


GRID_SIZE = 10
# GRID_SIZE = 5
def print_grid(grid):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            print(grid[Pos(x, y)], end='')
        print()


def count_zeroes(grid):
    return sum(v == 0 for v in grid.values())


if __name__ == '__main__':
    content: str = open('input.txt').read()
    grid = {
        Pos(x, y): int(char) for y, line in enumerate(content.strip().splitlines())
        for x, char in enumerate(line)
    }
    # print(list(neighbors(Pos(8, 8), grid)))
    # zs = count_zeroes(grid)
    # for _ in range(100):
    for i in itertools.count(start=1):
        step_forward(grid)
        if all(v == 0 for v in grid.values()):
            print(i)
            break
        # zs += count_zeroes(grid)

    # print(zs)
