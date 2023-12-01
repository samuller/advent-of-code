#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("../..")
from lib import *


def isnum(input):
    try:
        int(input)
    except:
        return False
    return True


# zero is not acvtually one of the words so we shouldn't accidentally detect it
NUMBERS = ["_ZERO_X", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]


def ending_num_name(word):
    for idx, val in enumerate(NUMBERS):
        if word.endswith(val):
            return idx
    return None


# 7:28 54623 [overlapping - test with 4threeight7]
def main():
    lines = [line.strip() for line in fileinput.input()]

    values1 = []
    values2 = []
    for line in lines:
        # Part 1
        only_nums = "".join([a for a in line if isnum(a)])
        values1.append(int(only_nums[0] + only_nums[-1]))
        # Part 2
        nums = []
        for idx in range(len(line)):
            num_name = ending_num_name(line[:idx+1])
            if num_name is not None:
                nums.append(num_name)
            if isnum(line[idx]):
                nums.append(int(line[idx]))
        values2.append(int(f"{nums[0]}{nums[-1]}"))
    print(sum(values1))
    print(sum(values2))


if __name__ == '__main__':
    main()
