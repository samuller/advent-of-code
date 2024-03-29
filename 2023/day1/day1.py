#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("../..")
from lib import *


# zero is not actually one of the words so we shouldn't accidentally detect it
NUMBERS = ["_ZERO_X", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]


def ending_num_name(word):
    for idx, val in enumerate(NUMBERS):
        if word.endswith(val):
            return idx
    return None


# [7:28] wrong submission - 54623 [overlapping - test with 4threeight7]
def main():
    lines = [line.strip() for line in fileinput.input()]

    values1 = []
    values2 = []
    for line in lines:
        # Part 1
        only_nums = "".join([ch for ch in line if ch.isdecimal()])
        if len(only_nums) != 0:
            values1.append(int(only_nums[0] + only_nums[-1]))
        # Part 2
        nums = []
        for idx in range(len(line)):
            num_name = ending_num_name(line[:idx+1])
            if num_name is not None:
                nums.append(num_name)
            # https://stackoverflow.com/questions/44891070/whats-the-difference-between-str-isdigit-isnumeric-and-isdecimal-in-pyth
            if line[idx].isdecimal():
                nums.append(int(line[idx]))
        values2.append(int(f"{nums[0]}{nums[-1]}"))
    print(sum(values1))
    print(sum(values2))


if __name__ == '__main__':
    main()
