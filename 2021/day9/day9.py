#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("../..")
from lib import *
import itertools


def measure_basin(map, r,c, region=None):
    if region is None:
        region = set([(r,c)])
    # print(r,c,region)
    for dr,dc in [(-1,0),(0,-1),(1,0),(0,1)]:
        if not map.in_bounds(r+dr, c+dc):
            continue
        elif int(map.get(r+dr, c+dc)) == 9:
            continue
        elif (r+dr, c+dc) in region:
            continue
        else:
            region.add((r+dr, c+dc))
            # add to 'region' since its passed by reference
            measure_basin(map, r+dr, c+dc, region)
    return region


def main():
    lines = [line.strip() for line in fileinput.input()]
    print(f'Lines: {len(lines)}')

    count_valid = 0
    for line in lines:
        fields = line.split(' ')
    
    map = Map2D()
    map.load_from_data(lines)
    p1 = 0
    low_points = []
    basins = []
    # 513 @ 7:46 (start ~7:30)
    # 1568
    # 508 @ 7:52 (<=)
    for r in range(map.rows):
        for c in range(map.cols):
            height = int(map.get(r,c))
            is_lowest = True
            # print(map.get(r, c))
            for dr,dc in [(-1,0),(0,-1),(1,0),(0,1)]: #itertools.product([-1,0,1],[-1,0,1]):
                # if (dr, dc) == (0,0):
                #     continue
                if map.in_bounds(r+dr, c+dc):
                    if int(map.get(r+dr, c+dc)) <= height:
                        is_lowest = False
                    # print(map.get(r+dr, c+dc))
            if is_lowest:
                low_points.append((r,c))
                region = measure_basin(map, r,c)
                basins.append(region)
                # print(r,c,"=",len(region))
                risk_level = height+1
                # print(risk_level)
                # print(r,c,":", height)
                p1 += risk_level
    # print(low_points)
    print('p1:', p1)
    print('p2:', prod(sorted([len(b) for b in basins])[-3:]))
    # Remove low points from basins so they can be colored separately
    for b in basins:
        for l in low_points:
            if l in b:
                b.remove(l)
    map_str = map.to_str_col(
        [low_points, *basins],
        [ANSIColor.RED, *[ANSIColor.DARKCYAN for _ in basins]],
        replace_chars={
            '9': '█',
            '8': '▓',
            '7': '▓',
            '6': '▒',
            '5': '▒',
            '4': '▒',
            '3': '░',
            '2': '░',
            '1': '░',
            '0': '.',
        }
    )
    print(map_str)


if __name__ == '__main__':
    main()
