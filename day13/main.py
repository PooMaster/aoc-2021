def print_points(points):
    print(''.join(gen_str_points(points)))


def gen_str_points(points):
    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)

    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            if (x, y) in points:
                yield '#'
            else:
                yield '.'
        yield '\n'


def fold_points(points, axis, value):
    print(f"Folding {len(points)} points over {axis}={value}")
    def fold_val(val, fold_val):
        if val < fold_val:
            return val
        else:
            return fold_val * 2 - val
    if axis == 'x':
        return {(fold_val(x, value), y) for x, y in points}
    elif axis == 'y':
        return {(x, fold_val(y, value)) for x, y in points}
    else:
        raise NotImplementedError()


if __name__ == '__main__':
    content: str = open('input.txt').read()
    points, folds = content.strip().split('\n\n')
    points = {(int(x), int(y)) for line in points.splitlines() for x, y in [line.split(',')]}
    folds = [(axis, int(value)) for line in folds.splitlines() for axis, value in [line.split()[-1].split('=')]]

    for axis, value in folds:
        points = fold_points(points, axis, value)
        print(len(points))

    print_points(points)
