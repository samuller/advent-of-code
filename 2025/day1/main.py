#!/usr/bin/env python3
import fileinput
# import sys; sys.path.append("../..")
# from lib import *


def part2_per_tick(lines):
    dial = 50
    ans = 0
    for line in lines:
        # print(line)
        num = int(line[1:])
        if line[0] == "L":
            # dial -= num
            while num > 0:
                dial -= 1
                num -= 1
                dial = dial % 100
                if dial == 0:
                    # print("L")
                    ans += 1
        elif line[0] == "R":
            # dial += num
            while num > 0:
                dial += 1
                num -= 1
                dial = dial % 100
                if dial == 0:
                    # print("R")
                    ans += 1
        # print(line, dial)
        # if dial == 0:
        #     ans += 1
    return ans


# ~7:15 (2) 12792 (1 + )
# 7:20 (3) 6219
# 7:27 (4) 5920
# 7:45 (5) 6335
# 7:53 correct
def main():
    lines = [line.strip() for line in fileinput.input()]

    dial = 50
    p1 = 0
    p2 = 0
    for line in lines:
        num = int(line[1:])
        if line[0] == "L":
            p2 += (num // 100)
            if (num % 100) >= dial and dial != 0:
                p2 += 1
            dial -= num
        elif line[0] == "R":
            p2 += (num // 100)
            if (dial + (num % 100)) >= 100:
                p2 += 1
            dial += num
        dial = dial % 100
        if dial == 0:
            p1 += 1
    print(p1)
    print(p2)
    # print(part2_per_tick(lines))


if __name__ == '__main__':
    main()
