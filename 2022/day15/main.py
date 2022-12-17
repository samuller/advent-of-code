#!/usr/bin/env python3
import itertools
import fileinput

import sys; sys.path.append("../..")
from lib import *


def get_manhattan_rim(center, radius):
    center_x, center_y = center
    # Ways of summing to dist_beyond with integers
    for dx, dy in zip(range(0, radius), range(radius, -1, -1)):
        for sgn_x, sgn_y in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            xx = center_x + dx*sgn_x
            yy = center_y + dy*sgn_y
            # print('  ', xx, yy)
            yield xx, yy


def search_any_overlap(location, sensors, ranges):
    loc_x, loc_y = location
    is_seen = False
    for idx in range(len(sensors)):
        xs, ys = sensors[idx]
        xc, yc = ranges[idx]
        range_dist = abs(xs - xc) + abs(ys - yc)
        dist_to_loc = abs(xs - loc_x) + abs(ys - loc_y)
        if dist_to_loc <= range_dist:
            is_seen = True
            break
    return is_seen


# 14:19 - move around the edges
def main():
    lines = [line.replace("\n", "") for line in fileinput.input()]
    # Edited input files to add argument to first line
    yy = int(lines[0].replace("y = ", ""))
    # Parse rest of input
    sensors = []
    seen_beacon = []
    max_dist = 0
    min_x = 2**30
    min_y = 2**30
    max_x = -2**30
    max_y = -2**30
    # Skip the first custom line we added
    for line in lines[1:]:
        xs, ys = line.split()[2:4]
        xs = int(xs.replace("x=", "").replace(",", ""))
        ys = int(ys.replace("y=", "").replace(":", ""))
        sensors.append((xs, ys))

        xc, yc = line.split()[8:10]
        xc = int(xc.replace("x=", "").replace(",", ""))
        yc = int(yc.replace("y=", "").replace(":", ""))
        seen_beacon.append((xc, yc))
        # Find data limits
        dist = abs(xs - xc) + abs(ys - yc)
        max_dist = max(dist, max_dist)
        min_x = min(xs, xc, min_x)
        min_y = min(ys, yc, min_y)
        max_x = max(xs, xc, max_x)
        max_y = max(ys, yc, max_y)
        # print(f"{sensors[-1]} -> {seen_beacon[-1]} = {dist}")

    # Part 1
    is_seen_count = 0
    # print((max_x + max_dist) - (min_x - max_dist))
    for xx in range(min_x - max_dist, max_x + max_dist):
        # Where beacon's cannot possibly exist
        if (xx, yy) in seen_beacon:
            continue
        is_seen = False
        for idx in range(len(sensors)):
            xs, ys = sensors[idx]
            xc, yc = seen_beacon[idx]
            dist_close = abs(xs - xc) + abs(ys - yc)
            dist_sensor = abs(xs - xx) + abs(ys - yy)
            if dist_sensor <= dist_close:
                is_seen = True
        if is_seen:
            is_seen_count += 1
        if (1 + xx - (min_x - max_dist)) % 100_000 == 0:
            print(".", end="", flush=True)
    print()
    print(is_seen_count)
    exit()

    # # Part 1++
    # is_seen_count = 0
    # for xx in range(min_x - max_dist, max_x + max_dist): # part1
    # # for xx in range(-10, 30): # part1
    # # for xx in range(0, 20): # part2
    #     # where beacon's cannot possibly exist
    #     if (xx, yy) in seen_beacon:
    #         continue
    #     is_seen = search_any_overlap((xx, yy), sensors, seen_beacon)
    #     if is_seen:
    #         is_seen_count += 1
    #     if xx % 100000 == 0:
    #         print("progress", xx)
    #     # seen_x.append(is_seen)
    # # print(seen_x)
    # # print(sum([1 if s else 0 for s in seen_x]))
    # print(is_seen_count)
    # exit()

    # Party 2
    # max_search = 20
    max_search = 4000000
    is_seen_count = 0
    # print(max_search)
    found = None
    count = 0
    for curr_idx in range(len(sensors)):
        xs, ys = sensors[curr_idx]
        xc, yc = seen_beacon[curr_idx]
        dist_beyond = abs(xs - xc) + abs(ys - yc) + 1
        print(f"{curr_idx} ({dist_beyond})")
        # print(f"{xs},{ys} / {xc},{yc} -> {dist_beyond}")
        for xx, yy in get_manhattan_rim((xs, ys), dist_beyond):
            if (xx, yy) in seen_beacon:
                continue
            if not (0 <= xx <= max_search and 0 <= yy <= max_search):
                continue
            count += 1
            is_seen = search_any_overlap((xx, yy), sensors, seen_beacon)
            # print((xx, yy))
            if not is_seen:
                # print((xx, yy))
                found = (xx, yy)
                break
        if found:
            break
        # # dist_sensor = abs(xs - xx) + abs(ys - yy)
        # # Ways of summing to dist_beyond with integers
        # for dx, dy in zip(range(0,dist_beyond+1), range(dist_beyond, -1, -1)):
        #     for sgn_x, sgn_y in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        #         # print('  ', xs+dx*sgn_x, ys+dy*sgn_y)
        #         xx = xs + dx*sgn_x
        #         yy = ys + dy*sgn_y
        #         if (xx, yy) in seen_beacon:
        #             continue
        #         is_seen = False
        #         for idx2 in range(len(sensors)):
        #             xs2, ys2 = sensors[idx2]
        #             xc2, yc2 = seen_beacon[idx2]
        #             dist_close = abs(xs2 - xc2) + abs(ys - yc2)
        #             dist_sensor = abs(xs2 - xx) + abs(ys - yy)
        #             if idx2 == idx and not (dist_sensor == dist_beyond - 1):
        #                 print('  ', xs+dx*sgn_x, ys+dy*sgn_y)
        #                 assert dist_sensor == dist_beyond - 1, f"{idx}, {dist_sensor}, {dist_beyond}"
        #             if dist_sensor <= dist_close:
        #                 is_seen = True
        #         if is_seen:
        #             is_seen_count += 1
        #         if not is_seen:
        #             found = xx, yy
        #             print(xx, yy)
        #             break
        # if found:
        #     break
        
        # exit()

    # print(count)
    print(found)
    print(4000000*found[0] + found[1])


if __name__ == '__main__':
    main()
