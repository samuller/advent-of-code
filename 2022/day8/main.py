#!/usr/bin/env python3
import fileinput
from collections import Counter

import sys; sys.path.append("../..")
from lib import *


# Map2D()
def in_bounds(r, c, r_max, c_max):
    if (0 <= r < r_max) and (0 <= c < c_max):
        return True
    return False


def any_visible(arr, r, c):
    r_max = len(arr)
    c_max = len(arr[r])
    height = arr[r][c]

    # For each direction
    for dr, dc in [(0,1),(1,0),(0,-1),(-1,0)]:
        # Move further in that direction
        for dist in range(1, 1+max(r_max, c_max)):
            rr = r+dr*dist
            cc = c+dc*dist
            # If we reached the edge without any sight blockers
            if not in_bounds(rr, cc, r_max, c_max):
                return True
            # If our sight is blocked, stop considering this direction
            if arr[rr][cc] >= height:
                break
    return False


def get_scenic_score(arr, r, c):
    r_max = len(arr)
    c_max = len(arr[r])
    height = arr[r][c]

    score = 1
    # For each direction
    for dr, dc in [(-1,0),(0,-1),(1,0),(0,1)]:
        # Move further in that direction
        for dist in range(1, 1+max(r_max, c_max)):
            rr = r+dr*dist
            cc = c+dc*dist
            # If we reached the edge without any sight blockers
            if not in_bounds(rr, cc, r_max, c_max):
                dist -= 1
                break
            # If our sight is blocked, stop considering this direction
            if arr[rr][cc] >= height:
                break
        # print(dist, end=" ")
        score *= dist
    # print()
    return score


# 1224 - wrong
# 7:26
# 7:43
def main():
    lines = [line.replace("\n", "") for line in fileinput.input()]
    visible = 0
    arr = [[int(chr) for chr in line] for line in lines]

    best_score = 0
    best_pos = None

    r_max = len(arr)
    for r in range(0, r_max):
        row = arr[r]
        c_max = len(row)
        for c in range(c_max):
            visible += 1 if any_visible(arr, r, c) else 0
            curr_score = get_scenic_score(arr, r, c)
            if curr_score > best_score:
                best_score = curr_score
                best_pos = (r, c)

    print(visible)
    print(best_score, best_pos)


if __name__ == '__main__':
    main()
