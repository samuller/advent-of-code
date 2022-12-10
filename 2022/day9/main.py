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

def move_rope(rope, dir, count):
    head, tail = rope
    visited = set()

    for _ in range(count):
        head = move(head, dir)
        tail = move_tail(tail, head)
        visited.add(tail)
        # print('T', tail)

    return (head, tail), visited

    # Before refactor for part 2
    # row, col = head
    # if dir == 'L':
    #     # head = (row, col-count)
    #     for _ in range(count):
    #         row, col = (row, col-1)
    #         head = row, col
    #         tail = move_tail(tail, head)
    #         visited.add(tail)
    #         print('T', tail)
    # elif dir == 'R':
    #     # head = (row, col+count)
    #     for _ in range(count):
    #         row, col = (row, col+1)
    #         head = row, col
    #         tail = move_tail(tail, head)
    #         visited.add(tail)
    #         print('T', tail)
    # elif dir == 'U':
    #     # head = (row-count, col)
    #     for _ in range(count):
    #         row, col = (row-1, col)
    #         head = row, col
    #         tail = move_tail(tail, head)
    #         visited.add(tail)
    #         print('T', tail, head)
    # elif dir == 'D':
    #     # head = (row+count, col)
    #     for _ in range(count):
    #         row, col = (row+1, col)
    #         head = row, col
    #         tail = move_tail(tail, head)
    #         visited.add(tail)
    #         print('T', tail)
    # else:
    #     assert False


def main():
    lines = [line.replace("\n", "") for line in fileinput.input()]
    # print(lines)

    # Part 1
    # top-left
    # head = (0, 0)
    # tail = head
    # visited = set()
    # for line in lines:
    #     dir, count = line.split()
    #     count = int(count)
    #     print(dir, count)
    #     rope, tail_visited = move_rope((head, tail), dir, count)
    #     head, tail = rope
    #     visited.update(tail_visited)
    #     print(head, tail)
    # print(len(visited))

    # Part 2
    rope = [(0, 0)]*10
    visited = set()
    for line in lines:
        dir, count = line.split()
        count = int(count)
        print(dir, count)
        for _ in range(count):
            # Move head by 1
            rope[0] = move(rope[0], dir)
            # Move tails in response
            for idx in range(len(rope)-1):
                curr_head, curr_tail = rope[idx], rope[idx+1]
                curr_tail = move_tail(curr_tail, curr_head)
                rope[idx+1] = curr_tail
            print(rope)
            visited.add(rope[-1])
    print(len(visited))


if __name__ == '__main__':
    main()
