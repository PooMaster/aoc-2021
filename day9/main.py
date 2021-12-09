from collections import namedtuple

class Pos(namedtuple("Pos", "x, y")):
    def __add__(self, other: "Pos"):
        return Pos(self.x + other.x, self.y + other.y)

def neighbor_values(pos, grid):
    deltas = [
        Pos(-1, 0),
        Pos(0, -1),
        Pos(1, 0),
        Pos(0, 1),
    ]
    for d in deltas:
        neighbor_pos = pos + d
        if neighbor_pos in grid:
            yield grid[neighbor_pos]

if __name__ == '__main__':
    content: str = open('input.txt').read()
    grid = {
        Pos(x, y): int(char) for y, line in enumerate(content.strip().splitlines())
        for x, char in enumerate(line)
    }

    # Part 1
    low_points = [
        pos for pos, value in grid.items()
        if all(value < other for other in neighbor_values(pos, grid))
    ]
    print('Part 1:')
    print(sum(grid[pos] + 1 for pos in low_points))
