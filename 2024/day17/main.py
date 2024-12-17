#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("../..")
from lib import *


class Classy:
    def __init__(self):
        pass


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
    pointer = 0
    output = []
    # A, B, C
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
        print(pointer, ":", opcode, literal_operand, states)
    print(states)
    print(output)
    print(",".join([str(o) for o in output]))


if __name__ == '__main__':
    main()
