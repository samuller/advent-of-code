#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("../..")
from lib import *


def compute(ins, states):
    pointer = 0
    output = []
    # 3-bit = 0-7
    while pointer < len(ins):
        opcode = ins[pointer]
        # literal or combo
        literal_operand = ins[pointer+1]
        if opcode in [0, 6, 7]: # adv, bdv, cdv
            combo_operand = combo(literal_operand, states)
            reg_mapping = {0: 'A', 6: 'B', 7: 'C'}
            reg_idx = reg_mapping[opcode]
            num = states['A']
            den = 2**combo_operand
            states[reg_idx] = int(num/den)
        if opcode == 1:
            states['B'] = states['B']^literal_operand
        if opcode == 2:
            combo_operand = combo(literal_operand, states)
            states['B'] = combo_operand % 8
        if opcode == 3:
            if states['A'] == 0:
                pass
            elif states['A'] != 0:
                pointer = literal_operand
        if opcode == 4:
            states['B'] = states['B']^states['C']
        if opcode == 5:
            combo_operand = combo(literal_operand, states)
            output.append(combo_operand % 8)
        if not (opcode == 3 and states['A'] != 0):
            pointer += 2
        # print(pointer, ":", opcode, literal_operand, {a:format(b, 'b') for a, b in states.items()})
    return output


def combo(operand, registers):
    assert operand != 7
    if 0 <= operand <= 3:
        return operand
    if operand == 4:
        return registers['A']
    if operand == 5:
        return registers['B']
    if operand == 6:
        return registers['C']
    assert False, operand
    return None


# 7:34 - don't add commas till 7:36
# Stop at 7:45 / Return at 10:15 ... 12:15
def main():
    lines = [line.strip() for line in fileinput.input()]
    registers, instructions = list(grouped(lines))
    states = {reg.split(': ')[0].replace("Register ", ""): int(reg.split(': ')[1]) for reg in registers}
    assert list(states.keys()) == ['A', 'B', 'C']
    # print(states)
    assert len(instructions) == 1
    ins = [int(op) for op in instructions[0].split(": ")[1].split(",")]
    # print(ins)
    # states['A'] = 2024
    # ins = [0,1,5,4,3,0]
    # Part 2
    # for val in range(1_000_000, 1_000_000_000):
    # for val in range(10**14, 10**16):  # range(2**45, 2**48)
    # 2,4,1,1,7,5,0,3,1,4,4,4,5,5,3,0
    start = 2**47 - 2**46 - 2**45 #- 2**40 + 2**16
    start = 2**45 + 2**44 + 2*43
    # start = 0b1_111_000_000_000_000_000_000_000_000_000_000_000_000_000_111
    start = 0b0011_1100_0000_0000_0000_0000_0000_0000_0000_0000_0000_0111
    # for val in range(start, start+10):
    # for val in range(start, start+2**47, 2**(42-26)):
    for i in range(2**16):
        # val = int(f"1_111_000_000_000_000_000_000_000_000_000_000_000_000_{format(i, '03b')}_011", 2)
        # 1101_0011 / 1101_0110 => 1110_0101_0110_0100
        # 1110_0111_1110_0101_0110_0100
        # val = int(f"0011_1100_0000_0000_0000_0000_{format(i, '016b')}_0110_0100", 2)
        # 110_0101_0110_0100
        # val = int(f"0011_1100_0000_0000_0{format(i, '016b')}110_0101_0110_0100", 2)
        # val = int(f"11_1100_0000_0000_{format(i, '016b')}_1110_0101_0110_0100", 2)
        val = int(f"{format(i, '016b')}_0000_0000_0000_0000_0000_0101_0110_0100", 2)
        # val = int(f"11_1100_0000_0000_0{format(i, '016b')}110_0101_0110_0100", 2)
        # val = int(f"1011_1000_{format(i, '016b')}_0000_0000_0000_0101_0110_0100", 2)
        # 101110001001101011010111000000000000010101100100 = [2,4,1,  7,5,5,5  ,1,1,4,4,4,5,5,3,0]
        # 101110001001101011010
        val = int(f"1011_1000_1001_1010_0000_{format(i, '016b')}_0101_0110_0100", 2)
        # 1011_1000_1001_1010_1101_0111_1011_1000_0000_0101_0110_0100
        val = int(f"1011_1000_1001_1010_1101_0111_{format(i, '016b')}_0110_0100", 2)
        #           1011_1000_1001_1010_1101_0111_1011_1000_0010_XXXX_0110_0100
        val = int(f"1011_1000_1001_1010_1101_0111_1011_1000_{format(i, '016b')}", 2)
        #           1011_1000_1001_1010_1101_0111_1011_1000_0010_1010_0010_1000
        val = int(f"1011_1000_1001_1010_1101_0111_1011_1000_{format(i, '016b')}", 2)
        new_states = dict(states)
        new_states['A'] = val
        output = compute(ins, new_states)
        if output == ins:
            print(val)
            break
        print(format(val, '047b'), output)
    print(states)
    print(len(output), "=", output)
    print(",".join([str(o) for o in output]))

# xor: 0,0=0 / 0,1=1 / 1,0=1 / 1,1=0
# 2,4 B = A % 8  [keep last 3 bits?]
# 1,1 B = B^1 (flip last bit -> if odd -1 else +1)
# 7,5 C = A/(2**B)  [left shift by 1 to 8]
# 0,3 A = A/(2**3)  [left shift 3]
# 1,4 B = B^4  [flip 3rd bit]
# 4,4 B = B^C  [B]
# 5,5 print B % 8 [last 3 bits of ((B^4)^(A/2**(A%8^1)))]
# 3,0 - while A != 0
# Loops ceil(log(A)/log(8)) times?

if __name__ == '__main__':
    main()
