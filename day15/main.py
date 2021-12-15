import heapq
from collections import namedtuple


class Pos(namedtuple("Pos", "x, y")):
    def __add__(self, other: "Pos"):
        return Pos(self.x + other.x, self.y + other.y)


ORTHOGONAL_DIRECTIONS = [
    Pos(1, 0),
    Pos(0, 1),
    Pos(-1, 0),
    Pos(0, -1),
]


def new_next_hops(pos, pos_cost, visited_nodes, grid, goal):
    for d in ORTHOGONAL_DIRECTIONS:
        neighbor = pos + d
        if neighbor not in grid or neighbor in visited_nodes:
            continue
        neighbor_cost = pos_cost + grid[neighbor]
        yield (neighbor_cost, pos, neighbor)


def extent(iterable):
    items = list(iterable)
    return min(items), max(items)


def print_grid(grid):
    min_x, max_x = extent(p.x for p in grid)
    min_y, max_y = extent(p.y for p in grid)

    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            print(grid[Pos(x, y)], end='')
        print()


def print_visited(visited):
    min_x, max_x = extent(p.x for p in grid)
    min_y, max_y = extent(p.y for p in grid)

    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            val = visited.get(Pos(x, y), ('.', None))[0]
            print(format(val, '>3'), end='')
        print()


TIMES = 5
def big_boy_grid(grid):
    max_x = max(p.x for p in grid)
    max_y = max(p.y for p in grid)

    new_grid = {}

    for y in range(0, TIMES):
        offset_y = Pos(0, (max_y+1) * y)
        for x in range(0, TIMES):
            offset_x = Pos((max_x+1) * x, 0)
            for pos, value in grid.items():
                new_cost = value + x + y
                new_grid[pos + offset_x + offset_y] = new_cost if new_cost <= 9 else new_cost - 9

    return new_grid


if __name__ == '__main__':
    content: str = open('input.txt').read()
    grid = {
        Pos(x, y): int(char) for y, line in enumerate(content.strip().splitlines())
        for x, char in enumerate(line)
    }
    grid = big_boy_grid(grid)

    # Mapping of visited positions to tuple of total cost and previous position
    starting_position = Pos(0, 0)
    goal = Pos(max(p.x for p in grid), max(p.y for p in grid))

    visited = {starting_position: (0, None)}  # Maintain list of visited nodes and their path costs
    # (neighbor_cost, pos, neighbor)
    next_hops = list(new_next_hops(starting_position, 0, set(), grid, goal))  # Min heap of possible next hops and their path costs
    heapq.heapify(next_hops)


    while True:
        while True:
            hop_cost, from_node, to_node = heapq.heappop(next_hops)
            if to_node not in visited:
                break

        visited[to_node] = (hop_cost, from_node)
        for next_hop in new_next_hops(to_node, hop_cost, visited, grid, goal):
            heapq.heappush(next_hops, next_hop)

        if to_node == goal:
            break

    # print_visited(visited)
    print(len(visited), 'visited')

    # walk = goal
    # while walk != starting_position:
    #     score, prev_pos = visited[walk]
    #     print(score, walk)
    #     walk = prev_pos

    print('path cost:', visited[goal][0])
