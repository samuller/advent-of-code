#!/usr/bin/env python3
import fileinput
from itertools import permutations, combinations, product
from math import log10
# import sys; sys.path.append("../..")
# from lib import *


def has_match(total, values, operators=['+', '*']):
    options = product(operators, repeat=len(values)-1)
    for option in options:
        result = values[0]
        for idx, op in enumerate(option):
            next_value = values[idx+1]
            # # We assume all numbers are positive
            # assert next_value > 0
            if op == '+':
                result += next_value
            elif op == '*':
                result *= next_value
            elif op == '||':
                # result = int(str(result) + str(next_value))
                strlen = int(log10(next_value)) + 1  # len(str(next_value))
                result = (result * 10**strlen) + next_value
            else:
                assert False
            # Do early exit as we know all operators are only additive/increasing
            # if result > total:
            #     break
        if result == total:
            return True
    return False


# first slow run took 15.5 minutes
# after fixing permutation generation then took 35sec
def main():
    lines = [line.strip() for line in fileinput.input()]
    p1 = 0
    p2 = 0
    for progress, line in enumerate(lines):
        print(f"{progress}/{len(lines)}")
        fields = line.split(': ')
        total = int(fields[0])
        values = [int(v) for v in fields[1].split()]
        print(total, values)
        if has_match(total, values, operators=['+', '*']):
            p1 += total
        if has_match(total, values, operators=['+', '*', '||']):
            p2 += total
    print(p1)
    print(p2)


if __name__ == '__main__':
    main()
