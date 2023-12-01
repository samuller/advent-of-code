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


def has_num_name(word):
    for val in NUMBERS:
        if val in word:
            return True
    return False


def get_num_name(word):
    for idx in range(len(word)):
        if word[idx:] in NUMBERS:
            return word[idx:]
    return None


def ending_num_name(word):
    for idx, val in enumerate(NUMBERS):
        if word.endswith(val):
            return idx
    return None


# 7:28 54623 [overlapping]
# 54591
def main():
    lines = [line.strip() for line in fileinput.input()]
    print(f'Lines: {len(lines)}')

    # Part 1
    values = []
    for line in lines:
        # fields = line.split(' ')
        line = "".join([a for a in line if isnum(a)])
        line = line[0] + line[-1]
        # print()
        values.append(int(line))
    print(sum(values))




if __name__ == '__main__':
    main()
