#!/usr/bin/env python3
import fileinput
from collections import Counter

import sys; sys.path.append("../..")
from lib import *


def get_sight_line(arr, r, c):
    r_max = len(arr)
    c_max = len(arr[r])
    height = arr[r][c]

    col = [rrow[c] for rrow in arr]

    # LRTB
    is_visible = [True]*4
    # left
    for cc in range(c-1, -1, -1):
        # print(" ", cc)
        if arr[r][cc] >= height:
            is_visible[0] = False
            break
    # right
    for cc in range(c+1, c_max):
        # print(" ", cc)
        if arr[r][cc] >= height:
            is_visible[1] = False
            break
    # top
    for rr in range(r-1, -1, -1):
        if arr[rr][c] >= height:
            is_visible[2] = False
            break
        # print(" ", rr)
    # bottom
    for rr in range(r+1, r_max):
        if arr[rr][c] >= height:
            is_visible[3] = False
            break
        # print(rr)
    # print(height, r, c, is_visible, any(is_visible))
    # exit()
    # print(lines[r][c], end="")
    # if any(is_visible):
    #     if r not in [0, r_max-1] and c not in [0, c_max-1]:
    #         print(r, c, '=', height, arr[r][c], arr[r], is_visible)
    return is_visible


def get_scenic_score(arr, r, c):
    r_max = len(arr)
    c_max = len(arr[r])
    height = arr[r][c]

    view_dist = [1] * 4
    # left
    for cc in range(c-1, -1, -1):
        # print(" ", cc)
        if arr[r][cc] >= height or cc == 0:
            view_dist[0] = abs(c - cc)
            break
    # right
    for cc in range(c+1, c_max):
        # print(" ", cc)
        if arr[r][cc] >= height or cc == c_max - 1:
            view_dist[1] = abs(c - cc)
            break
    # top
    for rr in range(r-1, -1, -1):
        if arr[rr][c] >= height or rr == 0:
            view_dist[2] = abs(r - rr)
            break
        # print(" ", rr)
    # bottom
    for rr in range(r+1, r_max):
        if arr[rr][c] >= height or rr == r_max - 1:
            view_dist[3] = abs(r - rr)
            break

    # 1 2 1 2
    # 2 2 2 1
    print(prod(view_dist), '=', view_dist, '/', height, r, c)
    return prod(view_dist)

# 1224 - wrong
# 7:26
# 7:43
# 30373
# 25512
# 65332
# 33549
# 35390
def main():
    lines = [line.replace("\n", "") for line in fileinput.input()]
    # print(lines)
    visible = 0
    arr = [[int(chr) for chr in line] for line in lines]
    print(arr)

    best_score = 0
    best_pos = None

    r_max = len(arr)
    for r in range(0, r_max):
        row = arr[r]
        c_max = len(row)
        for c in range(c_max):
            is_visible = get_sight_line(arr, r, c)
            if any(is_visible):
                visible += 1
            curr_score = get_scenic_score(arr, r, c)
            if curr_score > best_score:
                best_score = curr_score
                best_pos = (r, c)
            # print(height, r, c, is_visible, any(is_visible))
            # exit()
            # print(lines[r][c], end="")
        # print()

    # print(get_scenic_score(arr, 1, 2))
    # print(get_scenic_score(arr, 3, 2))
    print(visible)
    print(best_score, best_pos)


if __name__ == '__main__':
    main()
