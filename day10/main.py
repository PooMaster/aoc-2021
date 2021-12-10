from statistics import median

illegal_points = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

completion_points = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

NO_MORE = object()

class PeekableIter:
    def __init__(self, iterable):
        self.it = iter(iterable)
        self.next_val = next(self.it, NO_MORE)

    def __next__(self):
        if self.next_val is NO_MORE:
            raise StopIteration()
        
        ret = self.next_val
        self.next_val = next(self.it, NO_MORE)
        # print(ret)
        return ret

    def peek(self):
        return self.next_val


def parse_chunk(char_iter):
    match next(char_iter):
        case '(':
            while char_iter.peek() != ')':
                parse_chunk(char_iter)
            n = next(char_iter)
            assert n == ')', n
        case '[':
            while char_iter.peek() != ']':
                parse_chunk(char_iter)
            n = next(char_iter)
            assert n == ']', n
        case '{':
            while char_iter.peek() != '}':
                parse_chunk(char_iter)
            n = next(char_iter)
            assert n == '}', n
        case '<':
            while char_iter.peek() != '>':
                parse_chunk(char_iter)
            n = next(char_iter)
            assert n == '>', n
        case other:
            assert False, other


def find_bad_characters(lines):
    for l in lines:
        try:
            parse_chunk(PeekableIter(l))
        except AssertionError as err:
            yield err.args[0]
        except StopIteration:
            pass


def is_illegal(line):
    try:
        parse_chunk(PeekableIter(line))
    except AssertionError as err:
        return True
    except StopIteration:
        pass
    return False


ending = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}

def get_completion(line):
    stack = []

    for char in line:
        if char in '([{<':
            stack.append(char)
        else:
            assert char == ending[stack[-1]]
            stack.pop()
    
    return ''.join(ending[ch] for ch in reversed(stack))


def score_completion(completion):
    score = 0
    for ch in completion:
        score *= 5
        score += completion_points[ch]
    return score


if __name__ == '__main__':
    content: str = open('input.txt').read()
    lines = content.strip().splitlines()

    # Part 1
    print(sum(illegal_points[char] for char in find_bad_characters(lines)))

    # Part 2
    incomplete_lines = [l for l in lines if not is_illegal(l)]
    scores = [score_completion(get_completion(line)) for line in incomplete_lines]
    print(median(scores))
