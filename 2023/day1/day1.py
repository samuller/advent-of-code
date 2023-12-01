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
    # values = []
    # for line in lines:
    #     # fields = line.split(' ')
    #     line = "".join([a for a in line if isnum(a)])
    #     line = line[0] + line[-1]
    #     # print()
    #     values.append(int(line))
    # print(sum(values))

    # Part 2 wrong
    # values = []
    # for line in lines:
    #     nums = []
    #     curr_word = ""
    #     for char in line:
    #         if has_num_name(curr_word):
    #             curr_num = NUMBERS.index(get_num_name(curr_word))
    #             nums.append(curr_num)
    #             curr_word = ""
    #         if isnum(char):
    #             nums.append(int(char))
    #             curr_word = ""
    #         else:
    #             curr_word += char

    #     if has_num_name(curr_word):
    #         curr_num = NUMBERS.index(get_num_name(curr_word))
    #         nums.append(curr_num)
    #         curr_word = ""
    #     else:
    #         curr_word += char

    #     print(nums)
    #     values.append(int(f"{nums[0]}{nums[-1]}"))
    # print(sum(values))

    # Part 2
    values = []
    for line in lines:
        nums = []
        for idx in range(len(line)):
            num_name = ending_num_name(line[:idx+1])
            if num_name is not None:
                nums.append(num_name)
            if isnum(line[idx]):
                nums.append(int(line[idx]))
        print(nums)
        values.append(int(f"{nums[0]}{nums[-1]}"))
    print(sum(values))





if __name__ == '__main__':
    main()
