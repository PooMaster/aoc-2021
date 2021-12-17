import logging
from enum import Enum
from math import prod
from typing import cast, NamedTuple, Iterator, Iterable


class StrChunkReader:
    def __init__(self, string: str):
        self.it: Iterator[str] = iter(string)
        self.remaining: int = len(string)
    
    def take(self, n: int) -> str:
        self.remaining -= n
        ret = ''.join(next(self.it) for _ in range(n))
        logging.debug(f"Next {n} bits are {ret}")
        return ret

    def finished(self) -> bool:
        return self.remaining == 0


class PacketType(Enum):
    sum = 0
    product = 1
    minimum = 2
    maximum = 3
    literal_value = 4
    greater_than = 5
    less_than = 6
    equal_to = 7


class Packet(NamedTuple):
    version: int
    type: PacketType
    value: int | list["Packet"]


def parse_packet(reader: StrChunkReader) -> Packet:
    version, type = read_packet_header(reader)

    logging.info(f"Started parsing packet of type {type} version {version}")

    if type == PacketType.literal_value:
        chunks = list(read_chunks(reader))
        value = int(''.join(chunks), 2)
    else:
        # Some operator packet
        length_type_id = reader.take(1)

        if length_type_id == '0':
            sub_packets_length = int(reader.take(15), 2)
            logging.info(f"Operator with length type 0, reading packets in the next {sub_packets_length} bits")
            value = list(parse_packets(StrChunkReader(reader.take(sub_packets_length))))

        else:  # length_type_id == '1':
            sub_packets_count = int(reader.take(11), 2)
            logging.info(f"Operator with length type 1, reading {sub_packets_count} sub packets")
            value = [parse_packet(reader) for _ in range(sub_packets_count)]

    return Packet(version, type, value)


def parse_packets(reader: StrChunkReader) -> Iterable[Packet]:
    while not reader.finished():
        yield parse_packet(reader)


def read_packet_header(reader: StrChunkReader) -> tuple[int, PacketType]:
    version = int(reader.take(3), 2)
    type_id = int(reader.take(3), 2)

    return version, PacketType(type_id)


def read_chunks(reader: StrChunkReader) -> Iterable[str]:
    continue_bit = '1'
    while continue_bit == '1':
        continue_bit = reader.take(1)
        yield reader.take(4)


hex_table: dict[int, str] = {ord(h): format(bin(int(h, 16))[2:], '>04') for h in '0123456789ABCDEF'}

def hex_to_bits(hex: str) -> str:
    return hex.translate(hex_table)


def packet_version_sum(packet: Packet) -> int:
    def packet_version_generator(packet: Packet) -> Iterable[int]:
        yield packet.version
        if isinstance(packet.value, list):
            for p in packet.value:
                yield from packet_version_generator(p)

    return sum(packet_version_generator(packet))


def evaluate_packet(packet: Packet) -> int:
    match packet.type:
        case PacketType.sum:
            return sum(evaluate_packet(p) for p in cast(list[Packet], packet.value))

        case PacketType.product:
            return prod(evaluate_packet(p) for p in cast(list[Packet], packet.value))

        case PacketType.minimum:
            return min(evaluate_packet(p) for p in cast(list[Packet], packet.value))

        case PacketType.maximum:
            return max(evaluate_packet(p) for p in cast(list[Packet], packet.value))

        case PacketType.literal_value:
            return cast(int, packet.value)

        case PacketType.greater_than:
            left, right = cast(list[Packet], packet.value)
            return int(evaluate_packet(left) > evaluate_packet(right))

        case PacketType.less_than:
            left, right = cast(list[Packet], packet.value)
            return int(evaluate_packet(left) < evaluate_packet(right))

        case PacketType.equal_to:
            left, right = cast(list[Packet], packet.value)
            return int(evaluate_packet(left) == evaluate_packet(right))


if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)

    content: str = open('input.txt').read()
    # content = "9C0141080250320F1802104A08"
    p: Packet = parse_packet(StrChunkReader(hex_to_bits(content.strip())))
    print(packet_version_sum(p))
    print(evaluate_packet(p))
