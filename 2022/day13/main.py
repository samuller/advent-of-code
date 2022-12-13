#!/usr/bin/env python3
import json
import fileinput
from functools import cmp_to_key

import sys; sys.path.append("../..")
from lib import *


def is_packet_sorted(left, right):
    # print('sort', left, right)
    for idx in range(min(len(left), len(right))):
        lf, rt = left[idx], right[idx]
        tp1, tp2 = type(left[idx]), type(right[idx])
        if (tp1, tp2) == (int, int):
            if lf < rt:
                return True
            if lf > rt:
                return False
            continue
        if (tp1, tp2) == (int, list):
            res = is_packet_sorted([lf], rt)
            if res is None:
                continue
            return res
        if (tp1, tp2) == (list, int):
            res = is_packet_sorted(lf, [rt])
            if res is None:
                continue
            return res
        if (tp1, tp2) == (list, list):
            res = is_packet_sorted(lf, rt)
            if res is None:
                continue
            return res
    if len(left) < len(right):
        return True
    elif len(left) > len(right):
        return False
    return None


def cmp_packet_sorted(left, right):
    _sorted = is_packet_sorted(left, right)
    if _sorted is None:
        return 0
    if _sorted:
        return -1
    else:
        return 1


def main():
    lines = [line.replace("\n", "") for line in fileinput.input()]
    part1 = 0
    for idx, group in enumerate(grouped(lines)):
        assert len(group) == 2
        # group = [eval(line) for line in group]
        # Prefer JSON parsing over eval() which is too Python specific
        left = json.loads(group[0])
        right = json.loads(group[1])
        _sorted = is_packet_sorted(left, right)
        # print(_sorted, idx, left, 'vs', right)
        # print()
        if _sorted:
            part1 += idx + 1
    print(part1)

    lines = [eval(line) for line in lines if line != ""]
    lines.append([[2]])
    lines.append([[6]])
    # print(lines)
    sorted_lines = sorted(lines, key=cmp_to_key(cmp_packet_sorted))
    part2 = 1
    for idx, line in enumerate(sorted_lines):
        if line == [[2]]:
            part2 *= (idx+1)
        if line == [[6]]:
            part2 *= (idx+1)
        # print(line)
    print(part2)


if __name__ == '__main__':
    main()
