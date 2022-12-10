#!/usr/bin/env python3
import fileinput
from collections import Counter

import sys; sys.path.append("../..")
from lib import *


def sgn(val):
    if val < 0:
        return -1
    elif val > 0:
        return 1
    else:
        return 0


def move_tail(tail, head):
    hr, hc = head
    tr, tc = tail
    dr, dc = hr-tr, hc-tc
    if abs(dr) >= 2 or abs(dc) >= 2:
        tail = (tr + 1*sgn(dr), tc + 1*sgn(dc))
    elif abs(dr) > 1:
        tail = (tr + 1*sgn(dr), tc)
    elif abs(dc) > 1:
        tail = (tr, tc + 1*sgn(dc))
    return tail


def move(loc, dir):
    row, col = loc
    if dir == 'L':
        row, col = (row, col-1)
    elif dir == 'R':
        row, col = (row, col+1)
    elif dir == 'U':
        row, col = (row-1, col)
    elif dir == 'D':
        row, col = (row+1, col)
    else:
        assert False
    return row, col


def move_rope(long_rope, dir, count):
    visited = set()
    for _ in range(count):
        # Move head by 1
        long_rope[0] = move(long_rope[0], dir)
        # Move tails in response
        for idx in range(len(long_rope)-1):
            curr_head, curr_tail = long_rope[idx], long_rope[idx+1]
            curr_tail = move_tail(curr_tail, curr_head)
            long_rope[idx+1] = curr_tail
        # print(rope)
        visited.add(long_rope[-1])
    return long_rope, visited


def main():
    lines = [line.replace("\n", "") for line in fileinput.input()]
    # (0, 0) is top-left (row, col)
    short_rope = [(0, 0)]*2
    long_rope = [(0, 0)]*10
    visited = [set(), set()]
    for line in lines:
        dir, count = line.split()
        count = int(count)
        # Part 1
        short_rope, tail_visited = move_rope(short_rope, dir, count)
        visited[0].update(tail_visited)
        # Part 2
        long_rope, tail_visited = move_rope(long_rope, dir, count)
        visited[1].update(tail_visited)

    print(len(visited[0]))
    print(len(visited[1]))


if __name__ == '__main__':
    main()
