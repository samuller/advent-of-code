#!/usr/bin/env python3
"""
Requirements:
    pip install bitstring
"""
import fileinput
import functools
from bitstring import BitArray, BitStream


def prod(iterable):
    # operator.mul
    return functools.reduce(lambda a,b,: a*b, iterable, 1)

def gt(values):
    assert len(values) == 2
    return 1 if values[0] > values[1] else 0

def lt(values):
    assert len(values) == 2
    return 1 if values[0] < values[1] else 0

def eq(values):
    assert len(values) == 2
    return 1 if values[0] == values[1] else 0


TYPE_LITERAL = 4
HEADER_SIZE = 6
TYPE_OPERATOR = {
    0: sum,
    1: prod,
    2: min,
    3: max,
    4: 'literal',
    5: gt,
    6: lt,
    7: eq,
}
# Length types
LEN_BITS = 0
LEN_PACKET_COUNT = 1


P1 = 0
def packet(bits, depth=0, debug=False):
    global P1
    indent = " " * depth
    # header
    version = bits.read(3).uint
    P1 += version
    type_id = bits.read(3).uint
    if debug: print(f"{indent}V{version} T{type_id}")
    if type_id == TYPE_LITERAL:
        more = bits.read(1).bool
        data_byte = bits.read(4)
        while more:
            more = bits.read(1).bool
            data_byte.append(bits.read(4))
        if debug: print(f"{indent}LITERAL: {data_byte.uint}")
        return data_byte.uint

    # Else type is operator
    operator = TYPE_OPERATOR[type_id]
    if debug: print(f"{indent}OPERATOR: {operator.__name__}")
    values = []
    length_type = bits.read(1).uint
    if length_type == LEN_BITS:
        subpackets_len = bits.read(15).uint
        if debug: print(f"{indent}Packets of length: {subpackets_len}")
        start_pos = bits.pos
        while bits.pos < start_pos + subpackets_len:
            res = packet(bits, depth+1)
            values.append(res)
        assert bits.pos - start_pos == subpackets_len
    elif length_type == LEN_PACKET_COUNT:
        num_of_subpackets = bits.read(11).uint
        if debug: print(f"{indent}Packets: {num_of_subpackets}")
        for i in range(num_of_subpackets):
            res = packet(bits, depth+1)
            values.append(res)
    # print(f"{indent}RESULT: {operator.__name__}({values}) = ...")
    result = operator(values)
    if debug: print(f"{indent}RESULT: {operator.__name__}({values}) = {result}")
    return result


# All examples
assert packet(BitStream("0xD2FE28")) == 2021
# 1 if lt(10, 20)
assert packet(BitStream("0x38006F45291200")) == 1
# max(1, 2, 3)
assert packet(BitStream("0xEE00D40C823060")) == 3
P1 = 0; packet(BitStream("0x8A004A801A8002F478")); assert P1 == 16
P1 = 0; packet(BitStream("0x620080001611562C8802118E34")); assert P1 == 12
P1 = 0; packet(BitStream("0xC0015000016115A2E0802F182340")); assert P1 == 23
P1 = 0; packet(BitStream("0xA0016C880162017C3686B18A3D4780")); assert P1 == 31
assert packet(BitStream("0xC200B40A82")) == 3
assert packet(BitStream("0x04005AC33890")) == 54
assert packet(BitStream("0x880086C3E88112")) == 7
assert packet(BitStream("0xCE00C43D881120")) == 9
assert packet(BitStream("0xD8005AC2A8F0")) == 1
assert packet(BitStream("0xF600BC2D8F")) == 0
assert packet(BitStream("0x9C005AC2F8F0")) == 0
assert packet(BitStream("0x9C0141080250320F1802104A08")) == 1


P1 = 0
def main():
    global P1
    lines = [line.strip() for line in fileinput.input()]
    packets = lines[0].strip()

    P1 = 0
    bits = BitStream(hex=packets)
    P2 = packet(bits)
    print(P1)
    print(P2)


if __name__ == '__main__':
    main()
