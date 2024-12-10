#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("../..")
from lib import *


def search(map, r, c, from_height, peeks_seen):
    height = map.get(r, c)
    if height == '.':
        return 0
    height = int(height)
    if (height - from_height) != 1:
        return 0
    if height == 9:
        # Part 2
        return 1
        # Part 1
        if (r,c) not in peeks_seen:
            peeks_seen.add((r,c))
            return 1
        else:
            return 0
    # print(r,c)
    DR=[-1,0,1,0]
    DC=[0,-1,0,1]
    valid_routes = 0
    for i in range(4):
        rr, cc = r+DR[i], c+DC[i]
        if 0 <= rr < map.rows and 0 <= cc < map.cols:
            valid_routes += search(map, rr, cc, height, peeks_seen)
    return valid_routes


def main():
    lines = [line.strip() for line in fileinput.input()]
    map = Map2D()
    map.load_from_data(lines)
    print(map)
    p1 = 0
    for r in range(map.rows):
        for c in range(map.cols):
            height = map.get(r, c)
            if height == '0':
                p1 += search(map, r, c, -1, set())
    print(p1)

if __name__ == '__main__':
    main()
