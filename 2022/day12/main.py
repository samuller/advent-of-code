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


# 7:56 - accidentally implemented depth-recursive first (while thinking it was BFS...)
# def dfs(grid_val, grid_seen_at, start, end, path):
#     assert (start[0], start[1]) in path
#     max_r = len(grid_val)
#     max_c = len(grid_val[0])
#     DR = [-1,0,1,0]
#     DC = [0,-1,0,1]
#     curr_val = grid_val[start[0]][start[1]]
#     # for c in range(len(grid[0])):
#     #     for r in range(len(row)):
#     shortest_path = None
#     for i in range(4):
#         rr = start[0] + DR[i]
#         cc = start[1] + DC[i]
#         # print(len(path), rr, cc)
#         if cc < 0 or cc >= max_c:
#             continue
#         if rr < 0 or rr >= max_r:
#             continue
#         # If we backtrack or get to a location in a slower way
#         if (rr, cc) in path or grid_seen_at[rr][cc] <= len(path):
#             continue
#         next_val = grid_val[rr][cc]
#         if abs(next_val - curr_val) > 1:
#             continue

#         path.append((rr, cc))
#         grid_seen_at[rr][cc] = len(path)
#         if (rr, cc) == end:
#             return path
#         pathfound = dfs(grid_val, grid_seen_at, start=(rr, cc), end=end, path=deepcopy(path))
#         assert pathfound is None or len(pathfound) >= len(path)
#         if pathfound is None or len(pathfound) == len(path):
#             # length shouldn't have become smaller
#             continue
#         if shortest_path is None or len(pathfound) < len(shortest_path):
#             shortest_path = pathfound
#     return shortest_path

# def bfs(grid, start, end):
#     max_r = len(grid)
#     max_c = len(grid[0])
#     DR = [-1,0,1,0]
#     DC = [0,-1,0,1]
#     max_val = max_r * max_c
#     grid_seen_at = [[max_val for _ in row] for row in grid]

#     curr_loc = start
#     curr_val = grid[curr_loc[0]][curr_loc[1]]
#     depth = 1
#     grid_seen_at[curr_loc[0]][curr_loc[1]] = depth
#     while True:
#         depth += 1
#         next_locs = []
#         for i in range(4):
#             rr = curr_loc[0] + DR[i]
#             cc = curr_loc[1] + DC[i]
#             # print(len(path), rr, cc)
#             if cc < 0 or cc >= max_c:
#                 continue
#             if rr < 0 or rr >= max_r:
#                 continue
#             # If we backtrack or get to a location in a slower way
#             # if (rr, cc) in path:
#             if grid_seen_at[rr][cc] <= depth:
#                 continue
#             next_val = grid[rr][cc]
#             if abs(next_val - curr_val) > 1:
#                 continue
            
#             next_locs.append((rr, cc))

#         print(next_locs)
#         if len(next_locs) == 0:
#             break

#         for rr, cc in next_locs:
#             # path.append((rr, cc))
#             grid_seen_at[rr][cc] = depth
#             if (rr, cc) == end:
#                 break
#         if (rr, cc) == end:
#             break
#             # pathfound = dfs(grid_val, grid_seen_at, start=(rr, cc), end=end, path=deepcopy(path))
#             # assert pathfound is None or len(pathfound) >= len(path)
#             # if pathfound is None or len(pathfound) == len(path):
#             #     # length shouldn't have become smaller
#             #     continue
#             # if shortest_path is None or len(pathfound) < len(shortest_path):
#             #     shortest_path = pathfound
#         if depth == 3:
#             exit()
#     return grid_seen_at[end[0]][end[1]], grid_seen_at

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

# Sabqponm
# abcryxxl
# accszExk
# acctuvwj
# abdefghi

# v..v<<<<
# >v.vv<<^
# .>vv>E^^
# ..v>>>^^
# ..>>>>>^

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
    # print(start, end)
    print()

    # grid_seen_at = [[max_val for ch in line] for line in lines]
    # path = [(start)]
    # grid_seen_at[start[0]][start[1]] = 1
    # path = dfs(grid, grid_seen_at, start, end, path)
    # print(path)
    # print(len(path))
    # print_grid(grid_seen_at)

    path_len, grid_seen_at = bfs(grid, start, end)
    print(path_len-1)
    # print_grid(grid_seen_at)
    # print_grid([['#' if val == 7011000 else '_' for val in row] for row in grid_seen_at])
    # Part 2
    starts = find_all_starts(grid)
    # print(starts)
    shortest = None
    for start in starts:
        path_len, _ = bfs(grid, start, end)
        if shortest is None or path_len < shortest:
            shortest = path_len
    print(shortest-1)


if __name__ == '__main__':
    main()
