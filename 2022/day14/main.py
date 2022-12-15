#!/usr/bin/env python3
import fileinput
import itertools
from collections import defaultdict

import sys; sys.path.append("../..")
from lib import *


def from_to(from_, to_):
    if from_ < to_:
        return list(range(from_, to_+1, 1))
    else:
        return list(range(from_, to_-1, -1))


def fall_down(location, objects, lowest_point = None):
    # New location to be simulated
    xx, yy = location
    # Shortcut if on floor.
    if lowest_point is not None and yy+1 == lowest_point:
        return None
    # Fall instantly to highest point beneath it, if any.
    highest_below = None
    for i in range(100):
        obj_y = yy + i
        if obj_y in objects[xx]:
            highest_below = obj_y
            break
    # for obj_y in objects[xx]:
    #     # print("  ", obj)
    #     # Check is beneath and then check if current highest (y value increase downward).
    #     if obj_y > yy and (highest_below is None or obj_y < highest_below):
    #         # print("highest_below = ", obj_y)
    #        highest_below = obj_y
    if highest_below is None:
        # print("Sand falling onto nothing!")
        return None
    # y value decreases upward
    yy = highest_below - 1
    return xx, yy


# Slow, but 178*178... thus < 32000
# 8:28 - profile with: time python3 -m cProfile -s time main.py < input.txt
# start simulation close to where it ended last?
# 8:40 - idea: dynamic programming!
# 8:45 - break
# 8:47 - idea: store highest at each X (9:00 - won't work)
# 9:05 - back from break
# 9:11 - long running sim completes (4020 $SECONDS ?)
# 9:18 break again
# ~12:00 - back again
# new data structure, set() per X ?
# 12:50 - completes in 15 seconds
# 13:23 think about 2D array/matrix?
# 13:45 realise that I should'nt have skipped my falls...
def main():
    lines = [line.replace("\n", "") for line in fileinput.input()]
    # print(lines)
    rocks = set()
    for line in lines:
        scan = line.split(" -> ")
        points = []
        for point in scan:
            x,y = point.split(",")
            x,y = int(x),int(y)
            points.append((x,y))
        for p1, p2 in zip(points[0:-1], points[1:]):
            x1, y1, x2, y2 = *p1, *p2
            assert x1 == x2 or y1 == y2
            for xx, yy in itertools.product(from_to(x1, x2), from_to(y1, y2)):
                rocks.add((xx,yy))

    sand_start = 500,0
    # sand = set()
    objects = defaultdict(set)
    for rock in rocks:
        xx, yy = rock
        objects[xx].add(yy)
    # print(len(rocks.union(sand)))

    # Part 1
    lowest_point = None
    # Part 2
    for rock in rocks:
        _, yy = rock
        if lowest_point is None or yy > lowest_point:
            lowest_point = yy
    lowest_point += 2
    print("lowest_point =", lowest_point)

    # Simulate
    count = 1
    not_infinite = True
    last_sand = sand_start
    new_start = None
    while not_infinite and sand_start[1] not in objects[sand_start[0]]:
        # if new_start == last_sand and last_sand != sand_start:
        #     print("FAILED SS", new_start)
        #     exit()
        new_start = sand_start  #last_sand[0], last_sand[1]-1  #last_sand # Part2: start simulation close to where it ended last
        result = fall_down(new_start, objects)
        if result is None:
            if lowest_point is None:
                print(f"Infinity at {count}")
                not_infinite = False
                break
            # Part 2
            result = new_start[0], lowest_point-1
        if result != new_start:
            last_sand = new_start
        # Slide
        while not_infinite and sand_start[1] not in objects[sand_start[0]]:
            xx, yy = result
            # Part 2 - If on floor
            if yy+1 == lowest_point:
                # last_sand = result[0], result[1] - 1
                # sand.add(result)
                objects[result[0]].add(result[1])
                break
            # Slide to left.
            if yy+1 not in objects[xx-1]:
                # if last_sand == (xx, yy):
                #     print("FAIL 1", last_sand)
                #     exit()
                # last_sand = xx, yy
                xx -= 1
                result = fall_down((xx,yy+1), objects)
                if result != (xx,yy+1):
                    last_sand = xx+1, yy
            # Slide to right.
            elif yy+1 not in objects[xx+1]:
                # if last_sand == (xx, yy):
                #     print("FAIL 2", last_sand)
                #     exit()
                # last_sand = xx, yy
                xx += 1
                result = fall_down((xx,yy+1), objects)
                if result != (xx,yy+1):
                    last_sand = xx-1, yy
            # Stand still
            else:
                # if last_sand == result:
                #     last_sand = result[0], result[1] - 1
                    # print("FAIL 3", last_sand)
                    # exit()
                # last_sand = result[0], result[1] - 1
                # sand.add(result)
                objects[result[0]].add(result[1])
                break
            if result is None:
                if lowest_point is None:
                    print(f"Infinity at {count} after sliding")
                    not_infinite = False
                    break
                # Part 2
                result = xx, lowest_point-1
        count += 1
        # if count % 1000 == 0:
        #     print(count, len(rocks), len(objects[sand_start[0]]))
        #     print("closest to top =", min(objects[sand_start[0]]))
    # print(len(sand))

    for rock in rocks:
        xx, yy = rock
        objects[xx].remove(yy)
    # print(objects)
    print(sum(len(col) for _, col in objects.items()))


if __name__ == '__main__':
    main()
