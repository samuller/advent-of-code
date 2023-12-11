#!/usr/bin/env python3
import fileinput


NORTH = (-1, 0)
SOUTH = (1, 0)
WEST = (0, -1)
EAST = (0, 1)

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
    # We initially might be connected in any direction
    look_dirs = [NORTH, EAST, SOUTH, WEST]
    while True:
        r1, c1 = path[-1]
        locs_found = []
        for dr, dc in look_dirs:
            # look
            # lr, lc = r1+dr, c1+dc
            lr, lc = rel_to_abs((r1, c1), (dr, dc))
            # If out of bounds
            if not ((0 <= lr < R) and (0 <= lc < C)):
                continue
            # Only look/move in directions we haven't been to yet
            if (lr, lc) in path:
                continue

            pipe1 = grid[lr][lc]
            # Get relative connected locations for this ype of pipe
            rel_conn = PIPE_CONNECT[pipe1]
            # Convert to absolute connected locations
            abs_conn = [rel_to_abs((lr, lc), conn) for conn in rel_conn]
            # Ignore pipes not connected to us (only relevant at start due to look_dirs?)
            if not path[-1] in abs_conn:
                continue
            abs_conn.remove(path[-1])
            assert len(abs_conn) == 1
            # Get next location connected to via pipe
            nr, nc = abs_conn[0]
            # If out of bounds, leave it
            if not ((0 <= nr < R) and (0 <= nc < C)):
                continue
            # If we've looped back to the start, then we're done
            if (nr, nc) == start:
                path.append((lr, lc))
                return path
            # Path should not have crazy loops, etc.
            assert (nr, nc) not in path
            # Add the look location and the next location to the path
            path.append((lr, lc))
            path.append((nr, nc))
            # Next round we should only look in directions connected to the "next" location we've now moved to
            new_pipe = grid[nr][nc]
            look_dirs = PIPE_CONNECT[new_pipe]

            locs_found.append((lr, lc))
            break
        # Check that at least one valid path is found
        assert len(locs_found) != 0, (lr, lc)
        # print(path)


def find_start(grid):
    for rr, row in enumerate(grid):
        if 'S' in row:
            return (rr, row.index('S'))
    return None


def main():
    lines = [line.strip() for line in fileinput.input()]
    grid = [[c for c in line] for line in lines]

    count_empty = 0
    for row in grid:
        # print(row)
        assert len(row) == len(grid[0])
        count_empty += row.count(".")
    # print(count_empty)

    # S is the starting position of the animal;
    # there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
    start = find_start(grid)
    path = follow_path(grid, start)
    # print(path)
    # print(len(path))
    halfway_dist = len(path)//2
    assert halfway_dist == len(path)/2
    print(halfway_dist)

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
