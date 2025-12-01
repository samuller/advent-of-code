#!/usr/bin/env python3
import fileinput
# import sys; sys.path.append("../..")
# from lib import *

def part1(lines):
    dial = 50
    ans = 0
    for line in lines:
        # print(line)
        num = int(line[1:])
        if line[0] == "L":
            dial -= num
        elif line[0] == "R":
            dial += num
        dial = dial % 100
        if dial == 0:
            ans += 1
    return ans

def part2(lines):
    dial = 50
    ans = 0
    for line in lines:
        # print(line)
        num = int(line[1:])
        if line[0] == "L":
            # (3)
            if num > dial: # and dial != 0
                print("  ", line, dial, (num // 100))
                ans += 1 + (num // 100)
                # (5)
                if dial == 0 or (num % 100) == dial:
                    ans -= 1
            dial -= num
        elif line[0] == "R":
            # (4)
            ans += num//100
            num %= 100
            # (3)
            if (num + dial) > 100:
                print("  ", line, dial, 1 + num//100)
                ans += 1 # (4) + num//100
            dial += num
        #(2)
        # while dial < 0:
        #     dial += 100
        #     print("+")
        #     p2 += 1
        # old_dial = dial
        dial = dial % 100
        print(line, dial)
        if dial == 0:
            ans += 1
        #(1)
        # if (old_dial != dial and old_dial < 0) or dial == 0:
        #     p2 += 1
        #     print(line)
    return ans


def part2correct(lines):
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

    # dial = 50
    # p1 = 0
    # p2 = 0
    # for line in lines:
    #     # print(line)
    #     num = int(line[1:])
    #     if line[0] == "L":
    #         pass
    #     elif line[0] == "R":
    #         pass
    print(part1(lines))
    # print(part2(lines))
    print(part2correct(lines))


if __name__ == '__main__':
    main()
