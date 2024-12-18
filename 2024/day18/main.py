#!/usr/bin/env python3
from collections import deque
import fileinput
import sys; sys.path.append("../..")
from lib import *


def shortest_path(start, end, map):
    DR=[-1,0,1,0]
    DC=[0,-1,0,1]
    queue = deque([(start, 0)])
    seen = set([start])
    steps = 0
    while len(queue) > 0:
        curr, steps = queue.popleft()
        for i in range(4):
            nr, nc = curr[0]+DR[i], curr[1]+DC[i]
            if (nr, nc) == end:
                return steps + 1
            if not ((0 <= nr < map.rows) and (0 <= nc < map.cols)):
                continue
            if map[nr, nc] == '#':
                continue
            if (nr, nc) in seen:
                continue
            if (nr, nc) == end:
                return steps + 1
            seen.add((nr, nc))
            queue.append(((nr, nc), steps + 1))
        # print(steps)
        # print(queue, seen)
        # print_map(map, {loc: 'O' for loc in seen})
        # if steps == 2:
        #     exit()
    # steps_needed = shortest_path((nr, nc), exit, map, steps=steps+1)
    return None


def print_map(map, extras):
    for rr in range(map.rows):
        for cc in range(map.cols):
            if (rr, cc) in extras:
                print(extras[rr, cc], end="")
            else:
                print(map[rr, cc], end="")
        print()


def print_mem(size, bytes):
    for rr in range(size):
        for cc in range(size):
            if (rr, cc) in bytes:
                print('#', end="")
            else:
                print('.', end="")
        print()


def to_map(size, bytes):
    rows = []
    for rr in range(size):
        row = []
        for cc in range(size):
            if (rr, cc) in bytes:
                row.append('#')
            else:
                row.append('.')
        rows.append(row)
    map = Map2D()
    map.load_from_data(rows)
    return map


def main():
    lines = [line.strip() for line in fileinput.input()]
    # size = 7  # 71
    # first_n = 12  # 1024
    size = 71
    first_n = 1024
    start = (0, 0)
    end = (size-1, size-1)
    bytes = []
    for line in lines:
        fields = [int(f) for f in line.split(',')]
        # Swap X,Y to R,C
        bytes.append((fields[1], fields[0]))
    bytes = bytes[:first_n]
    print(bytes)
    print_mem(size, bytes)
    # for step in range(12):
    #     for idx in range(len(bytes)):
    #         byte = bytes[idx]
    #         bytes[idx] = (byte[0], byte[1]+1)
    # print(f"After {step}:")
    # print_mem(size, bytes)
    map = to_map(size, bytes)
    p1 = shortest_path(start, end, map)
    print(p1)


if __name__ == '__main__':
    main()
