#!/usr/bin/env python3
import fileinput
import itertools
import sys; sys.path.append("../..")
from lib import *


def print_grid(grid, found=None):
    if found is None:
        found = []
    # for row in grid:
    #     print(row)
    for rr in range(len(grid)):
        row = grid[rr]
        for cc in range(len(row)):
            sym = grid[rr][cc]
            if (rr, cc) in found:
                print("x", end="")
            else:
                print(sym, end="")
        print()


def count_neightbours(grid, r, c):
    # print(r, c)
    count = 0
    for dr, dc in itertools.product([-1,0,1],[-1,0,1]):
        rr, cc = r+dr,c+dc
        if (dr, dc) == (0, 0) or not (0 <= rr < len(grid)) or not (0 <= cc < len(grid[0])):
            continue
        if grid[rr][cc] == "@":
            count += 1
    return count


def find_removable(grid):
    found = []
    for rr in range(len(grid)):
        row = grid[rr]
        for cc in range(len(row)):
            cnt = count_neightbours(grid, rr, cc)
            if cnt < 4 and grid[rr][cc] == "@":
                found.append((rr, cc))
    return found


def remove_found(grid, found):
    for rr, cc in found:
        grid[rr][cc] = '.'


def main():
    lines = [line.strip() for line in fileinput.input()]
    grid = []
    for line in lines:
        row = list(line)
        grid.append(row)

    found = find_removable(grid)
    p1 = len(found)
    p2 = p1
    while len(found) > 0:
        print(f"Removing {len(found)}")
        remove_found(grid, found)
        found = find_removable(grid)
        p2 += len(found)
    print(p1)
    print(p2)


if __name__ == '__main__':
    main()
