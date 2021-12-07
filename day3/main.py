from typing import Iterable
from collections import defaultdict

if __name__ == '__main__':
    content: str = open('input.txt').read()
    lines: list[str] = content.strip().splitlines()
    total_count: int = len(lines)

    positions: Iterable[tuple[str]] = zip(*lines)
    zeroes: list[int] = [sum(1 for bit in position if bit == '0') for position in positions]
    is_zero: list[bool] = [count > total_count/2 for count in zeroes]
    gamma_rate_str: str = ''.join('0' if is_z else '1' for is_z in is_zero)
    epsilon_rate_str: str = ''.join('1' if is_z else '0' for is_z in is_zero)

    gamma_rate: int = int(gamma_rate_str, 2)
    epsilon_rate: int = int(epsilon_rate_str, 2)

    print('Part 1:')
    print(gamma_rate * epsilon_rate)

    # Part 2
    def split_on_position(strings: list[str], pos: int) -> dict[str, list[str]]:
        """
        >>> split_on_position(['010', '001', '110', '011'], 2)
        {
            '0': ['001'],
            '1': ['010', '110', '011'],
        }
        """
        ret = defaultdict(list)
        for string in strings:
            ret[string[pos]].append(string)
        return ret

    # find oxygen generator rating
    oxy_lines = list(lines)
    for pos in range(0, len(lines[0])):
        bit_values = split_on_position(oxy_lines, pos)
        most_common = max(bit_values, key=lambda i: len(bit_values[i]))
        if len(bit_values['0']) == len(bit_values['1']):
            oxy_lines = bit_values['1']
        else:
            oxy_lines = bit_values[most_common]

        if len(oxy_lines) <= 1:
            break

    assert len(oxy_lines) == 1, "Yo, your oxygen generator rating code sucks"
    oxygen_generator_rating_str: str = oxy_lines[0]

    # find c02 scrubber rating
    oxy_lines = list(lines)
    for pos in range(0, len(lines[0])):
        bit_values = split_on_position(oxy_lines, pos)
        least_common = min(bit_values, key=lambda i: len(bit_values[i]))
        if len(bit_values['0']) == len(bit_values['1']):
            oxy_lines = bit_values['0']
        else:
            oxy_lines = bit_values[least_common]

        if len(oxy_lines) <= 1:
            break

    assert len(oxy_lines) == 1, "Yo, your c02 scrubber rating code sucks"
    co2_scrubber_rating_str: str = oxy_lines[0]

    oxygen_generator_rating: int = int(oxygen_generator_rating_str, 2)
    co2_scrubber_rating: int = int(co2_scrubber_rating_str, 2)
    life_support_rating: int = oxygen_generator_rating * co2_scrubber_rating

    print('Part 2:')
    print(oxygen_generator_rating, co2_scrubber_rating)
    print(life_support_rating)
