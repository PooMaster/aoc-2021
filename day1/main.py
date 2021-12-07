from typing import Iterable
from itertools import pairwise
from more_itertools import triplewise

def number_of_increases(values: Iterable[int]) -> int:
    """
    Given a list of numbers, return the number of consecutive pairs in which a
    number is larger than the one that precedes it.
    """
    return sum(a < b for a, b in pairwise(values))

def triple_sums(values: Iterable[int]) -> Iterable[int]:
    for vals in triplewise(values):
        yield sum(vals)

if __name__ == '__main__':
    content = open('input.txt').read()
    values = [int(line) for line in content.strip().splitlines()]

    print('Part1:')
    n = number_of_increases(values)
    print(n)

    print('Part2:')
    s = triple_sums(values)
    n = number_of_increases(s)
    print(n)
