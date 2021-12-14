from more_itertools import pairwise
from collections import Counter
from functools import lru_cache, reduce
import operator


def step(template, rules):
    return ''.join(gen_next_step(template, rules))


def gen_next_step(template, rules):
    yield template[0]
    for a, b in pairwise(template):
        yield rules[a + b]
        yield b


# DIDN'T UP USING THIS FUNCTION
# LEAVING FOR POSTERITY
def get_element_counts(template, rules, steps):
    @lru_cache()
    def pair_element_counts(pair, steps_remaining) -> int:
        left, right = pair
        if steps_remaining == 0:
            return Counter(right)
        inserted_char = rules[left + right]
        # print(left, inserted_char, right, steps_remaining)
        return pair_element_counts((left, inserted_char), steps_remaining-1) \
             + pair_element_counts((inserted_char, right), steps_remaining-1)
    
    return reduce(operator.add, (pair_element_counts(pair, steps) for pair in pairwise(template)), Counter([template[0]]))
    # return sum(pair_element_counts(pair, steps) for pair in pairwise(template))


def bottom_up(rules, step):
    pairs = list(rules.keys())
    counts = {p: Counter() for p in pairs}

    for _ in range(step):
        new_counts = {}
        # for each pair, see what it would expand to, and take the expansion
        # counts for those two new pairs from the previous step
        for pair, middle in rules.items():
            new_counts[pair] = Counter([middle]) + counts[pair[0] + middle] + counts[middle + pair[1]]
        counts = new_counts
    
    return counts


if __name__ == '__main__':
    content: str = open('input.txt').read()
    template, rules = content.strip().split('\n\n')
    rules = {left: right for line in rules.splitlines() for left, right in [line.split(' -> ')]}
    orig_template = template

    for _ in range(10):
        template = step(template, rules)

    c = Counter(template)
    most_common = max(set(template), key=c.get)
    least_common = min(set(template), key=c.get)
    # print(c[most_common], c[least_common])
    print('Part 1:')
    print(c[most_common] - c[least_common])

    # TRIED DOING MEMOIZED RECURSIVE GENERATOR
    # print(c)
    # c = get_element_counts(orig_template, rules, 20)
    # print(c)
    # most_common = max(set(template), key=c.get)
    # least_common = min(set(template), key=c.get)
    # print(c[most_common], c[least_common])
    # print(c[most_common] - c[least_common])

    expansion_counts = bottom_up(rules, 40)
    pair_counts = (expansion_counts[a+b] for a, b in pairwise(orig_template))
    counts = reduce(operator.add, pair_counts, Counter(orig_template))

    most_common = max(set(template), key=counts.get)
    least_common = min(set(template), key=counts.get)
    # print(counts[most_common], counts[least_common])
    print('Part 2:')
    print(counts[most_common] - counts[least_common])
