from collections import defaultdict
from dataclasses import dataclass

LINE_LEN = 5

Number = int

@dataclass
class Line:
    count: int = 0

class BingoBoard:
    def __init__(self, grid: list[list[Number]]):
        """
        grid is a list of rows of numbers
        """
        self.grid = grid
        # Lines in which a win can occur
        self.lines: list[Line] = []
        self.num_to_lines: dict[Number, list[Line]] = defaultdict(list)
        self.marked_nums: set[int] = set()

        # rows
        for row in grid:
            new_line = Line()
            self.lines.append(new_line)
            for num in row:
                self.num_to_lines[num].append(new_line)
        # columns
        for col in zip(*grid):
            new_line = Line()
            self.lines.append(new_line)
            for num in col:
                self.num_to_lines[num].append(new_line)

    def mark(self, num: Number) -> None:
        for line in self.num_to_lines[num]:
            line.count += 1
        self.marked_nums.add(num)

    def unmarked(self) -> set[Number]:
        grid_numbers = set(i for row in self.grid for i in row)
        return grid_numbers - self.marked_nums

    def is_win(self) -> bool:
        return any(line.count >= LINE_LEN for line in self.lines)

    def __str__(self):
        return '\n'.join(
            ' '.join(format(i, '>2') for i in row) for row in self.grid
        )


def str_to_board(board_str):
    grid = [[int(i) for i in line.split()] for line in board_str.splitlines()]
    return BingoBoard(grid)


if __name__ == '__main__':
    content: str = open('input.txt').read()
    drawn_numbers_str, *boards_str = content.strip().split('\n\n')
    drawn_numbers: list[int] = [int(i) for i in drawn_numbers_str.split(',')]
    boards: list[BingoBoard] = [str_to_board(b) for b in boards_str]

    # Play game until a board wins
    for num in drawn_numbers:
        for b in boards:
            b.mark(num)
        if any(b.is_win() for b in boards):
            break
    
    winning_board: BingoBoard = next(b for b in boards if b.is_win())
    unmarked_nums = winning_board.unmarked()
    print('Part 1:')
    print(winning_board)
    print(unmarked_nums)
    print(sum(unmarked_nums) * num)

    # Play game until only one board hasn't won
    boards: list[BingoBoard] = [str_to_board(b) for b in boards_str]

    for num in drawn_numbers:
        for b in boards:
            b.mark(num)
        if sum(not b.is_win() for b in boards) == 1:
            losing_board: BingoBoard = next(b for b in boards if not b.is_win())
        if all(b.is_win() for b in boards):
            break
    
    unmarked_nums = losing_board.unmarked()
    print('Part 2:')
    print(losing_board)
    print(unmarked_nums)
    print(sum(unmarked_nums) * num)
