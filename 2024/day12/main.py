#!/usr/bin/env python3
from collections import namedtuple
import fileinput
import sys; sys.path.append("../..")
from lib import *


def remap(map, lines):
    unique_id = 0
    curr_region = None
    new_map = Map2D()
    new_map.load_from_data(lines)
    for rr in range(map.rows):
        for cc in range(map.cols):
            new_region = map[rr, cc]
            if curr_region is None:
                curr_region = new_region
            if new_region != curr_region:
                unique_id += 1
            new_map.set(rr, cc, str(unique_id))
            curr_region = new_region
    print(new_map)


seen_area = set()
seen_boundary = set()
def grow_out(map, rr, cc):
    global seen_area, seen_boundary
    region_id = map[rr, cc]
    DR=[-1,0,1,0]
    DC=[0,-1,0,1]
    area = 1
    boundaries = 0
    seen_area.add((rr, cc))
    for i in range(4):
        nr, nc = rr+DR[i], cc+DC[i]
        if (nr, nc) not in seen_boundary and (not map.in_bounds(nr, nc) or map[nr, nc] != region_id):
            boundaries += 1
            seen_boundary.add((rr, cc))
        if (nr, nc) not in seen_area and map.in_bounds(nr, nc) and map[nr, nc] == region_id:
            new_area, new_boundaries = grow_out(map, nr, nc)
            area += new_area
            boundaries += new_boundaries
    return area, boundaries


def main():
    lines = [line.strip() for line in fileinput.input()]
    map = Map2D()
    map.load_from_data(lines)
    print(map)

    # remap(map, lines)
    unseen = set()
    for rr in range(map.rows):
        for cc in range(map.cols):
            unseen.add((rr, cc))
    regions = {}
    global seen_area, seen_boundary
    while len(unseen) > 0:
        loc = unseen.pop()
        rr, cc = loc
        region_id = map[rr, cc]
        if region_id not in regions:
            area, perimeter = grow_out(map, rr, cc)
        regions[loc] = (area, perimeter)
        for seen in seen_area:
            if seen in unseen:
                unseen.remove(seen)
        seen_area = set()
        seen_boundary = set()
        print(loc, region_id, area, perimeter)

    p1 = 0
    # # count, same_neighbours
    # Region = namedtuple('Region', ['area', 'diff_neighbours'])
    # regions = defaultdict(Region)
    # for rr in range(map.rows):
    #     for cc in range(map.cols):
    #         region_id = map[rr, cc]
    #         diff_neighbours = 0
    #         DR=[-1,0,1,0]
    #         DC=[0,-1,0,1]
    #         for i in range(4):
    #             dr, dc = rr+DR[i], cc+DC[i]
    #             if not map.in_bounds(dr, dc) or map[dr, dc] != region_id:
    #                 diff_neighbours += 1
    #         if region_id not in regions:
    #             regions[region_id] = Region(area=1, diff_neighbours=diff_neighbours)
    #         else:
    #             prev_area, prev_diffs = regions[region_id]
    #             regions[region_id] = Region(area=prev_area + 1, diff_neighbours=prev_diffs + diff_neighbours)

    for region in regions:
        area, diff_neighbours = regions[region]
        perimeter = diff_neighbours
        print(region, area, perimeter, area * perimeter)
        p1 += area * perimeter
    print(p1)


if __name__ == '__main__':
    main()
