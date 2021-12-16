#!/usr/bin/env python3
# pip install bitstring
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


P1 = 0
def packet(bits, depth=0):
    global P1
    indent = " " * depth
    # p1 = 0
    values = []
    # header
    version = bits.read(3).uint
    P1 += version
    type_id = bits.read(3).uint
    # print(f"{indent}V{version} T{type_id}")
    if type_id == TYPE_LITERAL:
        more = bits.read(1).bool
        data_byte = bits.read(4)
        while more:
            more = bits.read(1).bool
            data_byte.append(bits.read(4))
        # print(f"{indent}LITERAL: {data_byte.uint}")
        return [data_byte.uint]
    else:
        operator = TYPE_OPERATOR[type_id]
        # print(f"OPERATOR: {operator.__name__}")
        values = []
        I = bits.read(1).uint
        if I == 0:
            subpackets_len = bits.read(15).uint
            # print(f"{indent}Packets of length: {subpackets_len}")
            # bits.read(subpackets_len)
            start_pos = bits.pos
            while bits.pos < start_pos + subpackets_len:
                res = packet(bits, depth+1)
                values.extend(res)
            # TODO: check bytes read
        elif I == 1:
            num_of_subpackets = bits.read(11).uint
            # print(f"{indent}Packets: {num_of_subpackets}")
            for i in range(num_of_subpackets):
                res = packet(bits, depth+1)
                values.extend(res)
        # print(f"RESULT: {operator.__name__}({values}) = ...")
        result = operator(values)
        # print(f"RESULT: {operator.__name__}({values}) = {result}")
        return [result]
        # L = bits.read(15).uint
    return values


def parse_packets(bits):
    bits.pos = 0
    # p1 = 0
    P2 = packet(bits)[0]
    print(P1)
    print(P2)
    # while bits.pos < len(bits)-HEADER_SIZE:
    #     version, bits = packet(bits)
    #     p1 += version
    # print(p1)


# assert packet(BitStream("0xC200B40A82")) == [3]
# assert packet(BitStream("0x04005AC33890")) == [54]


def main():
    lines = [line.strip() for line in fileinput.input()]

    packets = "0x" + lines[0].strip()
    # # print(packets)
    # packets = "0x" + "D2FE28"
    # packets = "0x" + "38006F45291200"
    # packets = "0x" + "EE00D40C823060"
    # # packets = "0x" + "8A004A801A8002F478"
    # packets = "0x" + "D8005AC2A8F0"
    
    bits = BitStream(packets)
    parse_packets(bits)


    # bits = BitArray(packets)
    # pos = 0
    # version = bits[pos:pos+3]
    # type_id = bits[pos+3:pos+3+3]
    # print(type_id)
    # pos = pos+3+3
    # last_group = False
    # while not last_group and pos < len(bits):
    #     data_byte = bits[pos:pos+5]
    #     pos += 5
    #     if not data_byte[0]:
    #         last_group = True
    #     print(data_byte)
    # print()


    # print(packets)
    # for i in range(0,len(packets)-1,2):
    #     byte = packets[i:i+2]


if __name__ == '__main__':
    main()
