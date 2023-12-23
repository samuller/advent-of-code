#!/usr/bin/env python3
import fileinput
# import sys; sys.path.append("../..")
# from lib import *


NORTH = (-1, 0)
SOUTH = (1, 0)
WEST = (0, -1)
EAST = (0, 1)


class Classy:
    def __init__(self):
        pass


def move(loc, move_dir):
    loc = list(loc)
    for idx in range(len(loc)):
        loc[idx] += move_dir[idx]
    loc = tuple(loc)
    return loc


def print_grid(grid, highlight=None):
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


def main():
    lines = [line.strip() for line in fileinput.input()]

    R = len(lines)
    C = len(lines[0])
    grid = []
    for line in lines:
        row = [c for c in line]
        assert len(row) == C
        grid.append(row)
    # print(grid)

    start = (0, 1)
    end = (R-1, C-2)
    # loc, seen
    paths = [(start, set([start]))]
    longest = 0
    max_seen = set()
    while len(paths) > 0:
        loc, seen = paths.pop()
        if len(paths) > 0 and len(paths) % 1000 == 0:
            print(len(paths), len(seen), loc)
        for dir in [NORTH, SOUTH, EAST, WEST]:
            (rr, cc) = move(loc, dir)
            moved = set([(rr, cc)])
            if not (0 <= cc < C and 0 <= rr < R):
                continue
            if (rr, cc) in seen:
                continue
            if grid[rr][cc] == '#':
                continue
            elif grid[rr][cc] == '>':
                rr, cc = move((rr, cc), EAST)
            elif grid[rr][cc] == '<':
                rr, cc = move((rr, cc), WEST)
            elif grid[rr][cc] == 'v':
                rr, cc = move((rr, cc), SOUTH)
            elif grid[rr][cc] == '^':
                rr, cc = move((rr, cc), NORTH)
            else:
                assert grid[rr][cc] == '.'
            # Add location again in-case it is now new
            moved.add((rr, cc))
            if (rr, cc) in seen:
                continue
            new_seen = set(seen)
            new_seen = new_seen.union(moved)
            if (rr,cc) == end:
                # max_seen = set(seen.union(moved))
                # len(seen) + len(moved) ?
                # longest = max(longest, len(max_seen))
                if len(new_seen) > longest:
                    max_seen = new_seen
                    # Minus one because counting steps since start (i.e. not including start)
                    longest = len(max_seen) - 1
            else:
                new_seen = set(seen)
                new_seen = new_seen.union(moved)
                paths.append(((rr,cc), new_seen))
    # print_grid(grid, max_seen)
    print(longest, len(max_seen))



if __name__ == '__main__':
    main()
