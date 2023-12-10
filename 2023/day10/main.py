#!/usr/bin/env python3
import fileinput


NORTH = (-1, 0)
SOUTH = (1, 0)
WEST = (0, -1)
EAST = (0, 1)

DRDC = [NORTH, EAST, SOUTH, WEST]

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
            break
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
            # pipe = grid[rr][cc]
            # if pipe == ".":
            if (rr,cc) in path:
                continue
            point = Point(rr, cc)
            # print(rr, cc)
            if polygon.contains(point):
                enclosed += 1
    # 9:54 - wrong:  67
    print(enclosed)
    # https://stackoverflow.com/questions/217578/how-can-i-determine-whether-a-2d-point-is-within-a-polygon


if __name__ == '__main__':
    main()
