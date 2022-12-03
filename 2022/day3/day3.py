#!/usr/bin/env python3
import fileinput
from collections import Counter

import sys; sys.path.append("../..")
from lib import *


def get_priority(val):
    if val.islower():
        return 1 + ord(val) - ord('a')
    if val.isupper():
        return 27 + ord(val) - ord('A')
    assert False


assert get_priority('a') == 1
assert get_priority('z') == 26
assert get_priority('A') == 27
assert get_priority('Z') == 52


def get_badge(group):
    assert len(group) == 3
    count_grp = Counter([*set(group[0]), *set(group[1]), *set(group[2])])
    badges = [item for item, count in count_grp.items() if count == 3]
    assert len(badges) == 1
    return get_priority(badges[0])


def get_dups(comp1, comp2):
    count = Counter([*set(comp1), *set(comp2)])
    dups = [item for item, cnt in count.items() if cnt > 1]
    assert len(dups) == 1
    return get_priority(dups[0])


# 8:07: 2788 - too low
def main():
    bags = [line.strip() for line in fileinput.input()]
    part1 = 0
    part2 = 0
    for idx, bag in enumerate(bags):
        sz = len(bag)
        comp1 = bag[0:sz//2]
        comp2 = bag[sz//2:]
        part1 += get_dups(comp1, comp2)
        # Part 2 looks only at groups of 3
        if idx % 3 == 0 and idx != 0:
            group = bags[idx-3:idx]
            part2 += get_badge(group)
    # Remember last group of bags
    idx += 1
    if idx % 3 == 0 and idx != 0:
        group = bags[idx-3:idx]
        part2 += get_badge(group)

    print(part1)
    print(part2)
    # Test
    # assert total1 == 157
    # assert total2 == 70
    # Input
    # assert part1 == 8185
    # assert part2 == 2817


if __name__ == '__main__':
    main()
