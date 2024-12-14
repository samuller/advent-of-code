#!/usr/bin/env python3
import fileinput
# import sys; sys.path.append("../..")
# from lib import *


def is_safe(nums):
    if nums[0] == nums[1]:
        return False
    curr_dir = (nums[0] - nums[1])/abs(nums[0] - nums[1])
    for i in range(len(nums)-1):
        a, b = nums[i], nums[i+1]
        if a == b:
            return False
        dir = (a - b)/abs(a - b)
        # print(dir, abs(a-b), a, b)
        if curr_dir != dir:
            return False
            # print(dir)
        if 3 < abs(a - b):
            # print(abs(a - b))
            return False
    return True


# 10:08-10:23
#
def main():
    lines = [line.strip() for line in fileinput.input()]
    p1 = 0
    for line in lines:
        nums = [int(n) for n in line.split(' ')]
        safe = is_safe(nums)
        print(safe, nums)
        if safe:
            p1 += 1
    print(p1)


if __name__ == '__main__':
    main()
