#!/usr/bin/env python3
import fileinput
from itertools import permutations, combinations, product
# import sys; sys.path.append("../..")
# from lib import *


def main():
    # for perm in permutations(['+', '*'], 3):
    #     print(perm)
    # print(list(permutations(['+', '-']*2, 2)))
    # print(list(combinations(['+', '-']*2, 2)))
    # print()
    # print(list(combinations(range(2), 3)))
    # print(list(product(['+'], ['*'], repeat=1)))
    # print(set(combinations(['+', '-']*2, 2)))
    # print(set(combinations(['+', '-']*1, 1)))
    # print(list(combinations(['+', '*']*(2), (2))))
    # print(list(permutations(['+', '*']*(2), (2))))
    # print(list(combinations(['0', '1']*(2), (2))))
    # print(list(permutations(['0', '1']*(2), (2))))

    lines = [line.strip() for line in fileinput.input()]
    res1 = 0
    for progress, line in enumerate(lines):
        print(f"{progress}/{len(lines)}")
        fields = line.split(': ')
        total = int(fields[0])
        values = [int(v) for v in fields[1].split()]
        print(total, values)
        options = set(combinations(['+', '*', '||']*(len(values)-1), (len(values)-1)))
        # print(options)
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
