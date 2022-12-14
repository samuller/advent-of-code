#!/usr/bin/env python3
import fileinput
import itertools
# from functools import lru_cache  # 8:43

import sys; sys.path.append("../..")
from lib import *


def from_to(from_, to_):
    if from_ < to_:
        return list(range(from_, to_+1, 1))
    else:
        return list(range(from_, to_-1, -1))


# @lru_cache(maxsize=None)
def fall_down(location, objects):
    # New location to be simulated
    xx, yy = location
    # Fall instantly to highest point beneath it, if any.
    highest_below = None
    for obj in objects:
        obj_x, obj_y = obj
        # print(obj)
        if obj_x != xx:
            continue
        # print("  ", obj)
        # Check is beneath and then check if current highest (y value increase downward).
        if obj_y > yy and (highest_below is None or obj_y < highest_below):
            # print("highest_below = ", obj_y)
            highest_below = obj_y
    if highest_below is None:
        # print("Sand falling onto nothing!")
        return None
    # y value decreases upward
    yy = highest_below - 1
    return xx, yy
    # for i in range(2):
        # # new_sand = sand_start
        # # New sand location to be simulated
        # xx, yy = sand_start
        # # Fall instantly to highest point beneath it, if any.
        # highest_below = None
        # for obj in rocks.union(sand):
        #     obj_x, obj_y = obj
        #     # print(obj)
        #     if obj_x != xx:
        #         continue
        #     # print("  ", obj)
        #     # Check is beneath and then check if current highest (y value increase downward).
        #     if obj_y > yy and (highest_below is None or obj_y < highest_below):
        #         # print("highest_below = ", obj_y)
        #         highest_below = obj_y
        # if highest_below is None:
        #     print("Sand falling onto nothing!")
        #     break
        # # y value decreases upward
        # yy = highest_below - 1
        # sand.add((xx,yy))


# profile at 8:28
# time python3 -m cProfile -s time main.py < input.txt
# 8:40 - idea: dynamic programming!
# 8:45 - break
# 8:47 - idea: store highest at each X (9:00 - won't work)
# 9:05 - back from break
# 9:11 - long running sim completes (4020 $SECONDS ?)
# 9:18 break
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
        # print(points)
        for p1, p2 in zip(points[0:-1], points[1:]):
            # print(p1, p2)
            x1, y1, x2, y2 = *p1, *p2
            assert x1 == x2 or y1 == y2
            # print(x1, y1, x2, y2)
            # print(from_to(x1, x2))
            # print(from_to(y1, y2))
            # print(list(itertools.product(from_to(x1, x2), from_to(y1, y2))))
            for xx, yy in itertools.product(from_to(x1, x2), from_to(y1, y2)):
            # for xx, yy in zip((from_to(x1, x2+1)), (from_to(y1, y2+1))):
                # print(xx,yy)
                rocks.add((xx,yy))
            # for xx in from_to(x1, x2+1):
            #     for yy in from_to(y1, y2+1):
            #    print(xx,yy)
    # print(rocks)
    sand_start = 500,0
    sand = set()  #set([sand_start])
    # print(len(rocks.union(sand)))

    # Part 2
    lowest_point = None
    # for rock in rocks:
    #     _, yy = rock
    #     if lowest_point is None or yy > lowest_point:
    #         lowest_point = yy
    # lowest_point += 2
    print("lowest_point =", lowest_point)

    # Simulate
    count = 1
    not_infinite = True
    last_sand = sand_start
    highest_slide_count = 0 #part 2
    highest_sand = {} # part 2
    # while not_infinite: # Part 1
    while not_infinite and sand_start not in sand:  # Part 2
        new_start = sand_start  #last_sand # Part2: start simulation close to where it ended last
        all_objects = rocks.union(sand)  # Part 2 - increase performance?
        result = fall_down(new_start, all_objects)
        if result is None:
            if lowest_point is None:
                print(f"Infinity at {count}")
                not_infinite = False
                break
            result = new_start[0], lowest_point-1  # Part 2
        # Slide
        # while not_infinite: # Part 1
        slide_count = 0 # part 2
        while not_infinite and sand_start not in sand: # Part 2
            xx, yy = result
            # Part 2 - If on floor
            if yy+1 == lowest_point:
                # last_sand = result[0], result[1] - 1
                sand.add(result)
                break
            # Slide to left.
            if (xx-1,yy+1) not in all_objects:
                last_sand = xx, yy
                xx -= 1
                result = fall_down((xx,yy+1), all_objects)
            # Slide to right.
            elif (xx+1,yy+1) not in all_objects:
                last_sand = xx, yy
                xx += 1
                result = fall_down((xx,yy+1), all_objects)
            # Stand still
            else:
                # last_sand = result[0], result[1] - 1
                sand.add(result)
                break
            if result is None:
                if lowest_point is None:
                    print(f"Infinity at {count} after sliding")
                    not_infinite = False
                    break
                result = xx, lowest_point-1  # Part 2
            slide_count += 1
        if slide_count > highest_slide_count:
            highest_slide_count = slide_count
        count += 1
        # Part 2
        if count % 1000 == 0:
            print(count, len(rocks), len(sand))
            print(f"Slide stopped at {slide_count} (highest: {highest_slide_count})")
            lowest = 200
            for snd in sand:
                if snd[0] != sand_start[0]:
                    continue
                if snd[1] < lowest:
                    lowest = snd[1]
            print("lowest =", lowest)
    # print(sand)
    # print(count-2)  # part 1
    print(count-1)  # part 2
    print("?", len(sand))
    # 178*178... thus < 32000


if __name__ == '__main__':
    main()
