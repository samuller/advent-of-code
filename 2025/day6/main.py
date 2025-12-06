#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("../..")
from lib import *


def main():
    lines = [line for line in fileinput.input()]

    all_nums = None
    for line in lines[:-1]:
        nums = [int(num) for num in line.split()]
        if all_nums is None:
            all_nums = [[num] for num in nums]
        else:
            for idx in range(len(nums)):
                all_nums[idx].append(nums[idx])
        # if not '0' <= fields[0] <= '9':
        # print(nums)

    ops = lines[-1].split()
    # print(all_nums)
    # print(ops)

    p1 = 0
    for idx, op in enumerate(ops):
        if op == '+':
            p1 += sum(all_nums[idx])
        if op == '*':
            p1 += prod(all_nums[idx])

    p2 = 0
    ceph_nums = None
    prev_idx = 0
    prev_sym = lines[-1][0]
    for idx in range(1, len(lines[-1])+1):
        if idx != len(lines[-1]):
            sym = lines[-1][idx]
            if sym == ' ':
                continue
        ceph_nums = []
        # print(f"{prev_idx}:{idx-1}")
        for sub_idx in range(idx-1, prev_idx-1, -1):
            num_str = ""
            for line in lines[:-1]:
                dig_str = line[sub_idx]
                if dig_str == '':
                    continue
                num_str += dig_str
            if len(num_str.strip()) > 0:
                ceph_nums.append(int(num_str.strip()))
        # print(prev_sym, ceph_nums)
        if prev_sym == '+':
            p2 += sum(ceph_nums)
        if prev_sym == '*':
            p2 += prod(ceph_nums)
        # print(prev_nums)
        prev_idx = idx
        prev_sym = sym

    print(p1)
    print(p2)


if __name__ == '__main__':
    main()
