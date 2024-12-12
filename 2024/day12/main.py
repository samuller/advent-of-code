#!/usr/bin/env python3
from collections import namedtuple
import fileinput
import sys; sys.path.append("../..")
from lib import *


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
        if (not map.in_bounds(nr, nc) or map[nr, nc] != region_id):
            boundaries += 1
            # rr, cc -> nr, nc
            # print(map[rr, cc], rr, cc, DR[i], DC[i])
            seen_boundary.add((rr, cc, DR[i], DC[i]))
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
    # Region = namedtuple('Region', ['area', 'diff_neighbours'])
    # regions = defaultdict(Region)
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
            # Part 2
            print(seen_boundary)
            straight_bounds = 0
            while len(seen_boundary) > 0:
                # bound: rr, cc, dr, dc
                brr, bcc, bdr, bdc = seen_boundary.pop()
                connected_bounds = set()
                # look for neighbour bounds vertically
                # if bdr == 0:
                diff = 1
                while True:
                    possible_neighbour = (brr - diff, bcc, bdr, bdc)
                    if possible_neighbour not in seen_boundary:
                        break
                    connected_bounds.add(possible_neighbour)
                    diff += 1
                diff = 1
                while True:
                    possible_neighbour = (brr + diff, bcc, bdr, bdc)
                    if possible_neighbour not in seen_boundary:
                        break
                    connected_bounds.add(possible_neighbour)
                    diff += 1
                # look for neighbour bounds horizontally
                # if bdc == 0:
                diff = 1
                while True:
                    possible_neighbour = (brr, bcc - diff, bdr, bdc)
                    if possible_neighbour not in seen_boundary:
                        break
                    connected_bounds.add(possible_neighbour)
                    diff += 1
                diff = 1
                while True:
                    possible_neighbour = (brr, bcc + diff, bdr, bdc)
                    if possible_neighbour not in seen_boundary:
                        break
                    connected_bounds.add(possible_neighbour)
                    diff += 1
                for bound in connected_bounds:
                    seen_boundary.remove(bound)
                straight_bounds += 1
            print(straight_bounds)
        # regions[loc] = (area, perimeter)  # Part 1
        regions[loc] = (area, straight_bounds)  # Part 2
        for seen in seen_area:
            if seen in unseen:
                unseen.remove(seen)
        seen_area = set()
        seen_boundary = set()
        print(loc, region_id, area, perimeter)

    p1 = 0
    for region in regions:
        area, diff_neighbours = regions[region]
        perimeter = diff_neighbours
        # print(region, area, perimeter, area * perimeter)
        p1 += area * perimeter
    print(p1)


if __name__ == '__main__':
    main()
