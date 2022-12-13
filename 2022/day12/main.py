#!/usr/bin/env python3
import fileinput
from copy import deepcopy
from collections import Counter
from collections import namedtuple

import sys; sys.path.append("../..")
from lib import *


def print_grid(grid, as_letters=False):
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            val = grid[r][c]
            if as_letters:
                val = chr(val + ord('a')) 
            print(f"{val} ", end="")
        print()


def find_start_end(grid):
    start = None
    end = None
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            val = grid[r][c]
            if val >= 0:
                continue
            if val == ord('S')-ord('a'):
                assert start is None
                start = (r,c)
                grid[r][c] = 0
            if val == ord('E')-ord('a'):
                assert end is None
                end = (r,c)
                grid[r][c] = 25
    return start, end


def find_all_starts(grid):
    starts = []
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            val = grid[r][c]
            if val == 0:
                starts.append((r,c))
    return starts


def bfs(grid, start, end):
    max_r = len(grid)
    max_c = len(grid[0])
    DR = [-1,0,1,0]
    DC = [0,-1,0,1]
    max_val = max_r * max_c * 1000
    # print("max_val", max_val)
    grid_seen_at = [[max_val for _ in row] for row in grid]

    curr_loc = start
    grid_seen_at[curr_loc[0]][curr_loc[1]] = 1

    queue = [start]
    highest = 0
    while len(queue) > 0:
        curr_loc = queue.pop(0)
        # print(curr_loc)
        curr_val = grid[curr_loc[0]][curr_loc[1]]

        depth = grid_seen_at[curr_loc[0]][curr_loc[1]] + 1
        for i in range(4):
            rr = curr_loc[0] + DR[i]
            cc = curr_loc[1] + DC[i]
            # print(len(path), rr, cc)
            if cc < 0 or cc >= max_c:
                continue
            if rr < 0 or rr >= max_r:
                continue
            # If we backtrack or get to a location in a slower way
            # if (rr, cc) in path:
            if grid_seen_at[rr][cc] <= depth:
                continue
            next_val = grid[rr][cc]
            if next_val > highest:
                highest = next_val
                # print(highest)
            if next_val > curr_val + 1:
                continue

            grid_seen_at[rr][cc] = depth 
            queue.append((rr, cc))

    return grid_seen_at[end[0]][end[1]], grid_seen_at


# 7:56 - accidentally implemented depth-recursive first (while thinking it was BFS...)
# 8:17 - 7010 too high
# 8:31 - stop for now
# 11:50 - 12:13 (part-time)
# 12:18 - complete
def main():
    lines = [line.replace("\n", "") for line in fileinput.input()]
    grid = [[ord(ch)-ord('a') for ch in line] for line in lines]
    max_r = len(grid)
    max_c = len(grid[0])
    max_val = max_r * max_c

    start = None
    end = None
    start, end = find_start_end(grid)
    # print_grid(grid)  #, as_letters=True)

    # Part 1
    path_len, grid_seen_at = bfs(grid, start, end)
    print(path_len-1)
    # Part 2
    starts = find_all_starts(grid)
    shortest = None
    for start in starts:
        path_len, _ = bfs(grid, start, end)
        if shortest is None or path_len < shortest:
            shortest = path_len
    print(shortest-1)


if __name__ == '__main__':
    main()
