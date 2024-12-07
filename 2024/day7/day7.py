#!/usr/bin/env python3
import fileinput
from itertools import permutations, combinations, product
# import sys; sys.path.append("../..")
# from lib import *



def main():
    lines = [line.strip() for line in fileinput.input()]
    res1 = 0
    for progress, line in enumerate(lines):
        print(f"{progress}/{len(lines)}")
        fields = line.split(': ')
        total = int(fields[0])
        values = [int(v) for v in fields[1].split()]
        print(total, values)
        options = product(['+', '*', '||'], repeat=len(values)-1)
        matches = 0
        for option in options:
            result = values[0]
            for idx, op in enumerate(option):
                if op == '+':
                    result += values[idx+1]
                elif op == '*':
                    result *= values[idx+1]
                elif op == '||':
                    result = int(str(result) + str(values[idx+1]))
                else:
                    assert False
            if result == total:
                matches += 1
        if matches > 0:
            res1 += total
        # print(matches)
    print(res1)


if __name__ == '__main__':
    main()
