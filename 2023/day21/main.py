#!/usr/bin/env python3
import fileinput
from collections import Counter
# import sys; sys.path.append("../..")
# from lib import *

NORTH = (-1, 0)
SOUTH = (1, 0)
WEST = (0, -1)
EAST = (0, 1)


class Classy:
    def __init__(self):
        pass


def get_non_zeroes(grid):
    R = len(grid)
    C = len(grid[0])
    values = Counter()
    for rr in range(R):
        for cc in range(C):
            val = grid[rr][cc]
            values[val] += 1
    return values


def print_grid(grid, highlight=None, space=2):
    if highlight is None:
        highlight = []
    R = len(grid)
    C = len(grid[0])
    for rr in range(R):
        for cc in range(C):
            if (rr, cc) in highlight:
                print(f"O", end="")
            else:
                print(f"{grid[rr][cc]}", end="")
                # print(f"{grid[rr][cc]:2}", end=" ")
        print()
    print()

# [7:23] 265
def main():
    lines = [line.strip() for line in fileinput.input()]
    print(f'Lines: {len(lines)}')

    grid = []
    for line in lines:
        row = [c for c in line]
        grid.append(row)
    # print(grid)

    start = None
    R = len(grid)
    C = len(grid[0])
    for rr in range(R):
        for cc in range(C):
            if grid[rr][cc] == 'S':
                assert start is None
                start = (rr, cc)

    # Attempt 3
    dist = 0
    paths = set([(start)])
    ans1 = 0
    while dist < 64:
        dist += 1
        new_paths = set()
        for (sr, sc) in paths:
            for (dr, dc) in [NORTH, EAST, SOUTH, WEST]:
                rr, cc = sr + dr, sc + dc
                if not (0 <= rr < R and 0 <= cc < C ):
                    continue
                if grid[rr][cc] == '#':
                    continue
                new_paths.add((rr, cc))
        paths = new_paths
        print(len(paths), paths)
        # print_grid(grid, [loc for loc in new_paths], space=1)
    print(len(paths))

    # # Attempt 2
    # dist = 0
    # paths = [(start, 0)]
    # ans1 = 0
    # while len(paths) > 0:
    #     (sr, sc), dist = paths.pop()
    #     if dist >= 3:
    #         # print('.')
    #         ans1 += 1
    #         continue
    #     for (dr, dc) in [NORTH, EAST, SOUTH, WEST]:
    #         rr, cc = sr + dr, sc + dc
    #         if not (0 <= rr < R and 0 <= cc < C ):
    #             continue
    #         if grid[rr][cc] == '#':
    #             continue
    #         paths.append(((rr, cc), dist + 1))
    #     # if dist == 64:
    #     print(ans1, len(paths), paths)
    #     print_grid(grid, [loc for loc, _ in paths], space=1)
    #     # if len(paths) > 60:
    #     #     print(paths)
    #     # print(get_non_zeroes(grid_dist))
    # print(ans1)

    # grid_dist = []
    # for _ in range(R):
    #     grid_dist.append([0 for _ in range(C)])

    # Attempt 1
    # dist = 0
    # paths = [start]
    # while len(paths) > 0:
    #     lr, lc = paths.pop(0)
    #     dist = grid_dist[lr][lc]
    #     dist += 1
    #     for (dr, dc) in [NORTH, EAST, SOUTH, WEST]:
    #         rr, cc = lr + dr, lc + dc
    #         if not (0 <= cc < C and 0 <= rr < R):
    #             continue
    #         loc = grid[rr][cc]
    #         if loc == '#':
    #             continue
    #         if grid_dist[rr][cc] == 0 or grid_dist[rr][cc] > dist:
    #             grid_dist[rr][cc] = dist
    #             paths.append((rr, cc))
    #     # if dist == 64:
    #     print(len(paths))
    #     # print(get_non_zeroes(grid_dist))
    # print_grid(grid_dist)

    # ans1 = 0
    # for rr in range(R):
    #     for cc in range(C):
    #         if grid_dist[rr][cc] == 64:
    #             ans1 += 1
    # print(ans1)

if __name__ == '__main__':
    main()
