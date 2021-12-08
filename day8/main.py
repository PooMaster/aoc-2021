"""
1 is len(2)
7 is len(3)
4 is len(4)
8 is len(8)
3 is len(5) and superset of 1{}
9 is len(6) and superset of 4{}
2 is len(5) and not 3{} and superset of (8{} - 9{})
5 is len(5) and not 3{} and not 2{}
6 is len(6) and superset of 5{}
0 is len(6) and not 6{} and not 9{}

lengths:
2: 1
3: 7
4: 4
5: 2, 3, 5
6: 0, 6, 9
7: 8
"""

from collections import defaultdict


def solve_segments(digit_samples: list[str]) -> dict[frozenset, int]:
    """
    Given all possible seven segment signals for this display, solve and return
    a dictionary that can be used to decode what numbers the signals refer to.

    >>> decode(['acedgfb', 'cdfbe', 'gcdfa', 'fbcad', 'dab', 'cefabd', 'cdfgeb', 'eafb', 'cagedb', 'ab'])
    {'acedgfb': 8, 'cdfbe': 5, 'gcdfa': 2, 'fbcad': 3, 'dab': 7, 'cefabd': 9, 'cdfgeb': 6, 'eafb': 4, 'cagedb': 0, 'ab': 1}
    """
    solved: dict[int, str] = {}
    lengths: dict[int, set[str]] = defaultdict(list)
    for digit in digit_samples:
        lengths[len(digit)].append(digit)

    # Do the easy digits
    solved[1] = lengths[2].pop()
    solved[7] = lengths[3].pop()
    solved[4] = lengths[4].pop()
    solved[8] = lengths[7].pop()

    # Do the trickier digits
    def issuperset(digit_big, digit_small):
        "Returns True iff the first digit contains all the segments of the second digit"
        return set(digit_big).issuperset(set(digit_small))
    def pop_predicate(sample_set, predicate):
        "Pops and returns the first item of the sample set for which the predicate returns True for"
        found = next(filter(predicate, sample_set))
        sample_set.remove(found)
        return found
    solved[3] = pop_predicate(lengths[5], lambda d: issuperset(d, solved[1]))
    solved[9] = pop_predicate(lengths[6], lambda d: issuperset(d, solved[4]))
    solved[2] = pop_predicate(lengths[5], lambda d: issuperset(d, set(solved[8]) - set(solved[9])))
    solved[5] = lengths[5].pop()
    solved[6] = pop_predicate(lengths[6], lambda d: issuperset(d, solved[5]))
    solved[0] = lengths[6].pop()

    return {frozenset(segments): num for num, segments in solved.items()}

def decode_display(segments: list[str], segment_map: dict[frozenset, int]) -> int:
    display_ints = [segment_map[frozenset(seg)] for seg in segments]
    display_str = ''.join(map(str, display_ints))
    return int(display_str)

if __name__ == '__main__':
    content: str = open('input.txt').read()
    cases: list[list[str], list[str]] = [
        (digits_str.split(), display_str.split())
        for line in content.strip().splitlines()
        for digits_str, display_str in [line.split(' | ')]
    ]

    # Part 1
    total_easy_digits: int = sum(
        len(display_digit) in {2, 3, 4, 7}
        for digits, display in cases
        for display_digit in display
    )
    print('Part 1:')
    print(total_easy_digits)

    # Part 2
    display_values = [
        decode_display(display, solve_segments(digits))
        for digits, display in cases
    ]
    print('Part 2:')
    print(sum(display_values))
