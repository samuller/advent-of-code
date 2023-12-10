#!/usr/bin/env python3
import itertools
import fileinput
from enum import Enum
# import sys; sys.path.append("../..")
# from lib import *


NORTH = (-1, 0)
SOUTH = (1, 0)
WEST = (0, -1)
EAST = (0, 1)


# DR=[-1,0,1,0]
# DC=[0,-1,0,1]
DRDC = [(1, 0), (0, 1), (-1, 0), (0, -1)]

PIPE_CONNECT = {
    # | is a vertical pipe connecting north and south.
    '|': (NORTH, SOUTH),
    # - is a horizontal pipe connecting east and west.
    '-': (EAST, WEST),
    # L is a 90-degree bend connecting north and east.
    'L': (NORTH, EAST),
    # J is a 90-degree bend connecting north and west.
    'J': (NORTH, WEST),
    # 7 is a 90-degree bend connecting south and west.
    '7': (SOUTH, WEST),
    # F is a 90-degree bend connecting south and east.
    'F': (SOUTH, EAST),

}


def rel_to_abs(abs_ref, rel):
    return abs_ref[0] + rel[0], abs_ref[1] + rel[1]


def get_next(pipe, dr, dc):
    # | is a vertical pipe connecting north and south.
    # - is a horizontal pipe connecting east and west.
    # L is a 90-degree bend connecting north and east.
    # J is a 90-degree bend connecting north and west.
    # 7 is a 90-degree bend connecting south and west.
    # F is a 90-degree bend connecting south and east.
    # North
    if (dr, dc) == (-1, 0):
        if pipe in ['|', 'J', 'L']:
            match pipe:
                case '|':
                    return (-2, 0)
                case 'J':
                    return (-1, -1)
                case 'L':
                    return (-1,  1)
        else:
            return None
    # South
    elif (dr, dc) == (1, 0):
        if pipe in ['|', '7', 'F']:
            match pipe:
                case '|':
                    return (2,  0)
                case '7':
                    return (1, -1)
                case 'F':
                    return (1,  1)
        else:
            return None
    # West
    elif (dr, dc) == (0, -1):
        if pipe in ['-', 'L', 'F']:
            match pipe:
                case '-':
                    return ( 0, -2)
                case 'L':
                    return (-1, -1)
                case 'F':
                    return ( 1, -1)
        else:
            return None
    # East
    elif (dr, dc) == (0, 1):
        if pipe in ['-', 'J', '7']:
            match pipe:
                case '-':
                    return ( 0, 2)
                case 'J':
                    return (-1, 1)
                case '7':
                    return ( 1, 1)
        else:
            return None
    else:
        assert False


def follow_path(grid, start):
    R = len(grid)
    C = len(grid[0])
    path = [start]
    look_dirs = DRDC
    while True:
        r1, c1 = path[-1]
        added = []
        for dr, dc in look_dirs:
            # dr, dc = DRDC[i] #DR[i], DC[i]
            # look
            lr, lc = r1+dr, c1+dc
            # print(f"{(r1, c1)} + {(dr, dc)} = {(lr, lc)}")
            # If out of bounds
            if not ((0 <= lr < R) and (0 <= lc < C)):
                continue
            # Take first direction we haven't been to yet
            if (lr, lc) in path:
                continue

            pipe1 = grid[lr][lc]
            # if pipe1 == 'S'
            connects = PIPE_CONNECT[pipe1]
            abs_conn = [rel_to_abs((lr, lc), conn) for conn in connects]
            # print('----')
            # print(path[-1])
            # print(lr, lc, pipe1)
            # print(connects, '->', abs_conn)
            # Ignore pipes not connected to us (only relevant at start due to look_dirs?)
            if not path[-1] in abs_conn:
                continue
            abs_conn.remove(path[-1])
            nr, nc = abs_conn[0]
            # If out of bounds
            if not ((0 <= nr < R) and (0 <= nc < C)):
                continue
            if (nr, nc) == start:
                path.append((lr, lc))
                return path
            # Take first direction we haven't been to yet
            if (nr, nc) in path:
                continue

            path.append((lr, lc))
            path.append((nr, nc))
            new_pipe = grid[nr][nc]
            # Next round we should only look in connected directions
            look_dirs = PIPE_CONNECT[new_pipe]

            added.append((lr, lc))
            # if len(path) > 10:
            #     exit()
            break

            # nxt = get_next(pipe1, dr, dc)
            # print(f"{(dr, dc)} / {pipe1} -> {nxt}")
            # if nxt is not None:
            #     nr, nc = r1 + nxt[0], c1 + nxt[1]
            #     if (nr, nc) == start:
            #         path.append((lr, lc))
            #         return path
            #     # If out of bounds
            #     if not ((0 <= nr < R) and (0 <= nc < C)):
            #         continue
            #     # Take first direction we haven't been to yet
            #     if (nr, nc) in path:
            #         continue
            #     path.append((lr, lc))
            #     path.append((nr, nc))
            #     added.append((lr, lc))
            #     break
        assert len(added) != 0, (lr, lc)
        # print(path)


def find_start(grid):
    for rr, row in enumerate(grid):
        if 'S' in row:
            return (rr, row.index('S'))
    return None


def main():
    lines = [line.strip() for line in fileinput.input()]
    grid = [[c for c in line] for line in lines]

    empty = 0
    for row in grid:
        # print(row)
        assert len(row) == len(grid[0])
        empty += row.count(".")
    print(empty)

    # S is the starting position of the animal;
    # there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
    start = find_start(grid)
    path = follow_path(grid, start)
    # print(path)
    print(len(path))
    print(len(path)/2)

    # Part 2
    # Idea was:
    # - split path/polygon into convex hull polygons
    # - count areas within those polygons
    # But now:
    # https://stackoverflow.com/questions/36399381/whats-the-fastest-way-of-checking-if-a-point-is-inside-a-polygon-in-python
    # pip install shapely
    from shapely.geometry import Point
    from shapely.geometry.polygon import Polygon

    polygon = Polygon(path)

    enclosed = 0
    for rr in range(len(grid)):
        for cc in range(len(grid[rr])):
            pipe = grid[rr][cc]
            if pipe not in path:
            # if pipe == ".":
                point = Point(rr, cc)
                # print(rr, cc)
                if polygon.contains(point):
                    enclosed += 1
    # 9:54 - wrong:  67
    print(enclosed)



    # # seen = set(start)
    # path1 = [start]
    # # path2 = [start]
    # while True:
    #     two_paths = []
    #     r1, c1 = path1[-1]
    #     r2, c2 = path2[-1]
    #     # next1 = [get_next(grid[r1+dr][c1+dc], dr, dc) for (dr, dc) in DRDC]
    #     # next2 = [get_next(grid[r2+dr][c2+dc], dr, dc) for (dr, dc) in DRDC]
    #     # print(next1)
    #     # print(next2)
    #     for i in range(4):
    #         dr, dc = DRDC[i] #DR[i], DC[i]
    #         # look
    #         lr, lc = r1+dr, c1+dc
    #         if (lr, lc) == start:
    #             exit()
    #         pipe1 = grid[lr][lc]
    #         nxt1 = get_next(pipe1, dr, dc)
    #         print(f"{(dr, dc)} / {pipe1} -> {nxt1}")
    #         if nxt1 is not None:
    #             nr, nc = nxt1
    #             nxt_abs = r1 + nr, c1 + nc
    #             assert nxt_abs not in path1
    #             path1.append((lr, lc))
    #             path1.append(nxt_abs)
    #             break
    #             # seen.add(nxt)
    #         # pipe2 = grid[r2+dr][c2+dc]
    #         # nxt2 = get_next(pipe2, dr, dc)
    #         # if nxt2 is not None:
    #         #     assert nxt2 not in path2
    #         #     path1.append((dr, dc))
    #         #     path1.append(nxt2)
    #     print(path1)
    #     print(path2)

    #     # for i in range(4):
    #     #     dr, dc = DR[i], DC[i]
    #     #     # if (dr, dc) == (0, 0):
    #     #     #     continue
    #     #     if (dr, dc) in seen:
    #     #         continue
    #     #     pipe = grid[r1+dr][c1+dc]
    #     #     # . is ground; there is no pipe in this tile.
    #     #     if pipe == '.':
    #     #         continue
    #     #     nxt1 = get_next(pipe, r1 + dr, c1 + dc)
    #     #     nxt2 = get_next(pipe, r2 + dr, c2 + dc)
    #     #     if nxt1 is not None:
    #     #         curr1 = nxt1
    #     #     if nxt2 is not None:
    #     #         curr2 = nxt2
    #         # match (dr, dc), val:
    #         #     case ()
    #         # If connected to current:
    #     # seen.add(curr1)
    #     # seen.add(curr2)


if __name__ == '__main__':
    main()
