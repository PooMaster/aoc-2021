import re
import itertools
from typing import cast, NamedTuple, Iterable
from collections import ChainMap


class Pos(NamedTuple):
    x: int
    y: int

Grid = dict[Pos, str]


def add_pos(*args: Pos) -> Pos:
    return Pos(sum(p.x for p in args), sum(p.y for p in args))


ORTHOGONAL_DIRECTIONS = [
    Pos(1, 0),
    Pos(0, 1),
    Pos(-1, 0),
    Pos(0, -1),
]


def neighbors(pos: Pos, exclude: set[Pos] = set()) -> Iterable[Pos]:
    for dir in itertools.starmap(Pos, itertools.product(range(-20, 20), repeat=2)):
    # for dir in ORTHOGONAL_DIRECTIONS:
        if dir == Pos(0, 0) or dir in exclude:
            continue
        neighbor = add_pos(pos, dir)
        yield neighbor


input_pattern = re.compile(r'target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)')

class Box:
    def __init__(self, x_extent: tuple[int, int], y_extent: tuple[int, int]):
        self.x = x_extent
        self.y = y_extent

    def __contains__(self, position: Pos) -> bool:
        return self.x[0] <= position.x <= self.x[1] and self.y[0] <= position.y <= self.y[1]


def extent(iterable: Iterable[int]) -> tuple[int, int]:
    items = list(iterable)
    return min(items), max(items)


def print_grid(grid: Grid) -> None:
    min_x, max_x = extent(p.x for p in grid)
    min_y, max_y = extent(p.y for p in grid)

    for y in range(max_y, min_y-1, -1):
        for x in range(min_x, max_x+1):
            print(grid.get(Pos(x, y), '.'), end='')
        print()


def run_simulation(initial_velocity: Pos, target: Box) -> tuple[bool, Grid]:
    probe: Pos = Pos(0, 0)
    velocity: Pos = initial_velocity

    grid: Grid = {}
    grid[probe] = 'S'

    hit: bool = False

    while not hit and probe.x <= max_x and probe.y >= min_y:
        probe = add_pos(probe, velocity)
        grid[probe] = '#'
        if velocity.x > 0:
            velocity = add_pos(velocity, Pos(-1, -1))
        elif velocity.x < 0:
            velocity = add_pos(velocity, Pos(1, -1))
        else:
            velocity = add_pos(velocity, Pos(0, -1))

        # print(probe)
        if probe in target:
            hit = True
    
    return hit, grid


def flood_hits(initial_velocity: Pos, target: Box) -> Grid:
    hits: set[Pos] = set()
    fails: set[Pos] = set()
    untested: set[Pos] = {initial_velocity}

    while untested:
        velocity = untested.pop()
        if not run_simulation(velocity, target)[0]:
            fails.add(velocity)
            continue

        hits.add(velocity)
        untested.update(set(neighbors(velocity, exclude=(hits & fails))) - hits - fails)
    
    return {pos: '#' for pos in hits}


#     ss = """23,-10  25,-9   27,-5   29,-6   22,-6   21,-7   9,0     27,-7   24,-5
# 25,-7   26,-6   25,-5   6,8     11,-2   20,-5   29,-10  6,3     28,-7
# 8,0     30,-6   29,-8   20,-10  6,7     6,4     6,1     14,-4   21,-6
# 26,-10  7,-1    7,7     8,-1    21,-9   6,2     20,-7   30,-10  14,-3
# 20,-8   13,-2   7,3     28,-8   29,-9   15,-3   22,-5   26,-8   25,-8
# 25,-6   15,-4   9,-2    15,-2   12,-2   28,-9   12,-3   24,-6   23,-7
# 25,-10  7,8     11,-3   26,-7   7,1     23,-9   6,0     22,-10  27,-6
# 8,1     22,-8   13,-4   7,6     28,-6   11,-4   12,-4   26,-9   7,4
# 24,-10  23,-8   30,-8   7,0     9,-1    10,-1   26,-5   22,-9   6,5
# 7,5     23,-6   28,-10  10,-2   11,-1   20,-9   14,-2   29,-7   13,-3
# 23,-5   24,-8   27,-9   30,-7   28,-5   21,-10  7,9     6,6     21,-5
# 27,-10  7,2     30,-9   21,-8   22,-7   24,-9   20,-6   6,9     29,-5
# 8,-2    27,-8   30,-5   24,-7"""
#     velo_grid = {Pos(int(x), int(y)): '#' for p in ss.split() for x, y in [p.split(',')]}
#     velo_grid[Pos(0, 0)] = 'S'
#     print_grid(velo_grid)
#     exit()
"""
......##.......................
......##.......................
......##.......................
......##.......................
......##.......................
......##.......................
......##.......................
......##.......................
......###......................
S.....####.....................
.......#####...................
........########...............
...........#####...............
...........#####...............
....................###########
....................###########
....................###########
....................###########
....................###########
....................###########
"""

if __name__ == '__main__':
    content: str = open('input.txt').read()
    m = input_pattern.fullmatch(content.strip())
    if m is None:
        raise ValueError("Bad problem input")
    else:
        min_x, max_x, min_y, max_y = map(int, m.groups())
        min_x, max_x, min_y, max_y = 156, 202, -110, -69
        # min_x, max_x, min_y, max_y = 20, 30, -10, -5

    target = Box((min_x, max_x), (min_y, max_y))
    # velocity: Pos = Pos(6, 9)
    velocity: Pos = Pos(20, 0)

    target_grid: Grid = {Pos(x, y): '/' for y in range(min_y, max_y+1) for x in range(min_x, max_x+1)}
    start_grid: Grid = {Pos(0, 0): 'S'}

    # hit, path_grid = run_simulation(velocity, target)
    hit_grid = flood_hits(velocity, target)

    grid: Grid = cast(Grid, ChainMap(start_grid, hit_grid, target_grid))

    print_grid(grid)
    ways_to_hit = len(hit_grid) + len(target_grid)
    print(ways_to_hit)
    # print("HIT!!!" if hit else "MISSED")
    # highest_point = max(p.y for p, ch in grid.items() if ch == '#')
    # print(f"Max height of {highest_point}")
