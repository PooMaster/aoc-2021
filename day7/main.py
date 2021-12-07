from statistics import median

if __name__ == '__main__':
    content: str = open('input.txt').read()
    crab_locations: list[int] = [int(v) for v in content.strip().split(',')]

    # Part 1
    # Does this always work??
    median_location: int = int(median(crab_locations))
    fuel_required: int = sum(abs(l - median_location) for l in crab_locations)
    print('Part 1:')
    print(fuel_required)

    # Part 2
    # Just go for brute force i guess
    def summation(n: int) -> int:
        "Sum of integers from 1 to n"
        return n * (n + 1) // 2
    fuel_required = [
        sum(summation(abs(crab - pos)) for crab in crab_locations)
        for pos in range(len(crab_locations))
    ]
    print(min(fuel_required))
