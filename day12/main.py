from collections import defaultdict


def gen_paths(next_hop, path, visited, double_visited=None):
    if path[-1] == 'end':
        yield path
        return

    # non-deterministically pick next hop in path
    for n in next_hop[path[-1]]:
        new_double = double_visited
        if n[0].islower() and n in visited:
            # Can't visit lowercase node more than once
            if not new_double and n != 'start':
                # Unless one hasn't been visited twice yet
                new_double = n
            else:
                continue

        yield from gen_paths(next_hop, path + [n], visited | {n}, new_double)


if __name__ == '__main__':
    # content: str = open('input.txt').read()
    content: str = open('input.txt').read()
    edges = [line.split('-') for line in content.strip().splitlines()]

    next_hop = defaultdict(list)
    for here, there in edges:
        next_hop[here].append(there)
        next_hop[there].append(here)

    print(next_hop)

    paths = list(gen_paths(next_hop, ['start'], {'start'}))
    # for p in paths:
    #     print(p)
    print(len(paths))
