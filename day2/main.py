# https://adventofcode.com/2021/day/2

if __name__ == '__main__':
    content = open('input.txt').read()
    commands: list[tuple[str, int]] = [(dir, int(amount)) for line in content.strip().splitlines() for dir, amount in [line.split()]]

    horizontal: int = 0
    depth: int = 0

    for direction, amount in commands:
        match direction:
            case 'forward':
                horizontal += amount
            case 'down':
                depth += amount
            case 'up':
                depth -= amount

    print("Part 1:")
    print(horizontal * depth)

    horizontal: int = 0
    depth: int = 0
    aim: int = 0

    for direction, amount in commands:
        match direction:
            case 'forward':
                horizontal += amount
                depth += aim * amount
            case 'down':
                aim += amount
            case 'up':
                aim -= amount

    print("Part 2:")
    print(horizontal * depth)
    