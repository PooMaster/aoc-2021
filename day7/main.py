from statistics import median

if __name__ == '__main__':
    content: str = open('input.txt').read()
    values: list[int] = [int(v) for v in content.strip().split(',')]

    median_value: int = int(median(values))
    fuel_required: int = sum(abs(v - median_value) for v in values)
    print('Part 1:')
    print(fuel_required)
