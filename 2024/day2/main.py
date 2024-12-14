#!/usr/bin/env python3
import fileinput


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


def is_p2_safe(nums):
    if is_safe(nums):
        return True
    for idx in range(len(nums)):
        new_nums = nums[0:idx] + nums[idx+1:]
        if is_safe(new_nums):
            return True
    return False

# -10:30 mistake
# def count_errors(nums):
#     errors = 0
#     idx = 0
#     a, b = nums[idx], nums[idx+1]
#     while a == b:
#         errors += 1
#         idx += 1
#         if idx == len(nums):
#             return errors
#         a, b = nums[idx], nums[idx+1]
#     curr_dir = (a - b)/abs(a - b)
#     for i in range(len(nums)-1):
#         a, b = nums[i], nums[i+1]
#         if a == b:
#             errors += 1
#             continue
#         dir = (a - b)/abs(a - b)
#         # print(dir, abs(a-b), a, b)
#         if curr_dir != dir:
#             errors += 1
#             continue
#             # print(dir)
#         if 3 < abs(a - b):
#             # print(abs(a - b))
#             errors += 1
#             continue
#     return errors

# Part1: 10:08-10:23
# Part2: 10:23-10:33
# - with doing wrong idea from 10:23-10:30
def main():
    lines = [line.strip() for line in fileinput.input()]
    p1 = 0
    p2 = 0
    for line in lines:
        nums = [int(n) for n in line.split(' ')]
        safe = is_safe(nums)
        print(safe, nums)
        if safe:
            p1 += 1
        if is_p2_safe(nums):
            p2 += 1
    print(p1)
    print(p2)


if __name__ == '__main__':
    main()
