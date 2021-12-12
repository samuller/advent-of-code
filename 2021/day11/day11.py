#!/usr/bin/env python3
import fileinput
import itertools
import sys; sys.path.append("../..")
from lib import *


def print_map(map):
    R, C = len(map), len(map[0])
    for r in range(R):
        for c in range(C):
            print(map[r][c], end="")
        print()
    print()


def int_map(str_map):
    return [[int(n) for n in line] for line in str_map.split()]


def str_map(int_map):
    return '\n'.join([''.join([str(n) for n in row]) for row in int_map])


# bugs:
# - tried to do single pass
# - new vs. newer -> forgot to continue on "in new_flashers"
def step(map):
    R, C = len(map), len(map[0])
    flash_count = 0
    new_flashers = set()
    for r in range(R):
        for c in range(C):
            curr = map[r][c]
            curr += 1
            if curr > 9:
                new_flashers.add((r,c))
            map[r][c] = curr

    all_flashers = set()
    while len(new_flashers) != 0:
        newer_flashers = set()
        for r,c in new_flashers:
            for dr, dc in itertools.product([-1,0,1],[-1,0,1]):
                rr,cc = r+dr, c+dc
                if (dr, dc) == (0,0) or (rr,cc) in new_flashers:
                    continue
                if rr < 0 or cc < 0 or rr >= R or cc >= C:
                    continue
                if (rr,cc) in all_flashers:
                    continue
                curr = map[rr][cc]
                curr += 1
                if curr > 9:
                    newer_flashers.add((rr,cc))
                map[rr][cc] = curr
        all_flashers = set.union(all_flashers, new_flashers)
        new_flashers = newer_flashers
        # print('[]', len(all_flashers), all_flashers)
        # print('->', len(newer_flashers), newer_flashers)

    # should be zero newer (unless we break early for debugging)
    all_flashers = set.union(all_flashers, new_flashers)

    for r,c in all_flashers:
        map[r][c] = 0
    return len(all_flashers)
    # all_flashers = set()


# Example
ex_step0 = int_map("""11111
19991
19191
19991
11111""")
step(ex_step0)
ex_step1 = [[n for n in row] for row in ex_step0]
step(ex_step0)
ex_step2 = [[n for n in row] for row in ex_step0]

# print_map(ex_step1)
assert str_map(ex_step1) == """34543
40004
50005
40004
34543"""
# print_map(ex_step2)
assert str_map(ex_step2) == """45654
51115
61116
51115
45654"""


def main():
    lines = [line.strip() for line in fileinput.input()]
    print(f'Lines: {len(lines)}')

    # map = Map2D()
    # map.load_from_data(lines)
    map = [[int(n) for n in line] for line in lines]
    print_map(map)

    # Part 1
    # flashes = 0
    # for i in range(100):
    #     flashes += step(map)
    #     print_map(map)
    #     print(flashes)
    # print(flashes)

    # Part 2
    steps = 0
    while True:
        step(map)
        steps += 1
        print_map(map)
        uniqs = set([n for row in map for n in row])
        if len(uniqs) == 1:
            print(uniqs)
            break
    print(steps)

if __name__ == '__main__':
    main()
