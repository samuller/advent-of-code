#!/usr/bin/env python3
import fileinput
from collections import Counter

import sys; sys.path.append("..")
from lib import *


def get_priority(val):
    if val.islower():
        return 1 + ord(val) - ord('a')
    if val.isupper():
        return 27 + ord(val) - ord('A')
    assert False

# print('A', get_priority('A'))
# print('Z', get_priority('Z'))
# print('a', get_priority('a'))
# print('z', get_priority('z'))

def get_badge(group):
    count_grp = Counter([*set(group[0]), *set(group[1]), *set(group[2])])
    print(group)
    print(count_grp)
    summ2 = 0
    for val2 in count_grp:
        if count_grp[val2] == 3:
            assert summ2 == 0
            print(val2)
            summ2 = get_priority(val2)
    return summ2


# 8:07: 2788 - too low
def main():
    lines = [line.strip() for line in fileinput.input()]
    total1 = 0
    total2 = 0
    for idx, bag in enumerate(lines):
        # print(line)
        sz = len(bag)
        # print(sz, sz//2)
        comp1 = bag[0:sz//2]
        comp2 = bag[sz//2:]
        # print(comp1, comp2)
        count = Counter([*set(comp1), *set(comp2)])
        summ = 0
        for val in count:
            if count[val] > 1:
                assert summ == 0
                summ = get_priority(val)
        # print(summ)
        total1 += summ
        # Part 2
        if idx % 3 == 0 and idx != 0:
            group = lines[idx-3:idx]
            total2 += get_badge(group)
    idx += 1
    if idx % 3 == 0 and idx != 0:
        group = lines[idx-3:idx]
        total2 += get_badge(group)
    print(total1)
    print(total2)
    assert total1 == 157
    assert total2 == 70
    # assert total1 == 8185
    # assert total2 == 2817


if __name__ == '__main__':
    main()
