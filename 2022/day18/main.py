#!/usr/bin/env python3
import fileinput

import sys; sys.path.append("../..")
from lib import *


def count_sides(cubes):
    side_count = 0
    minuses = defaultdict(int)
    for cube in cubes:
        side_count += 6
        x,y,z = cube
        # itertools.product([-1, 1], repeat=3):
        for dx, dy, dz in [(-1,0,0), (1,0,0), (0,-1,0), (0,1,0), (0,0,-1), (0,0,1)]:
            if (x+dx,y+dy,z+dz) in cubes:
                side_count -= 1
                minuses[(x,y,z)] -= 1
    print("minuses")
    for xyz in sorted(minuses.keys()):
        print(f"{xyz}: {minuses[xyz]}")
    return side_count


# 7:40: 1-off-error - Limits were not fully outside cubes
# 8:00: 1-off-error - typo in limit max(limits[0], x+1, y+1, z+1)
def main():
    lines = [line.replace("\n", "") for line in fileinput.input()]
    # Example #1
    # lines = ['1,1,1', '2,1,1']

    cubes = set()
    limits = None
    for line in lines:
        x,y,z = [int(num) for num in line.split(',')]
        cubes.add((x,y,z))
        # Part 2
        if limits is None:
            limits = (x-1,x+1,y-1,y+1,z-1,z+1)
        limits = (min(limits[0], x-1, y-1, z-1), max(limits[1], x+1, y+1, z+1))
        # limits = (
        #     min(limits[0], x-1), max(limits[1], x+1),
        #     min(limits[2], y-1), max(limits[3], y+1),
        #     min(limits[4], z-1), max(limits[5], z+1),
        # )
    print(limits)

    # Part 1
    print(count_sides(cubes))

    # Part 2
    shell = set()
    # start = (limits[0]-1, limits[2]-1, limits[4]-1)
    start = (limits[0], limits[0], limits[0])
    queue = [start]
    visited = set()
    count_visits = defaultdict(int)
    while len(queue) > 0:
        # print(queue)
        x,y,z = queue.pop(0)
        # if (x,y,z) in [(0,1,1), (2,1,1), (1,0,1), (1,2,1), (1,1,0), (1,1,2)]:
        #     #           **       **       **                ***
        #     print("           !!!")
        # print(x,y,z)
        if not (limits[0] <= x <= limits[1] and limits[0] <= y <= limits[1] and limits[0] <= z <= limits[1]):
            # print('outside')
            continue
        # if not (limits[0] <= x < limits[1] and limits[2] <= y < limits[3] and limits[4] <= z < limits[5]):
        #     print('outside')
        #     continue
        # if not (limits[0]-1 <= x < limits[1]+1 and limits[2]-1 <= y < limits[3]+1 and limits[4]-1 <= z < limits[5]+1):
        #     print('outside')
        #     continue

        if (x,y,z) in cubes:
            # print(x,y,z)
            count_visits[(x,y,z)] += 1
        # else:
        #     print(x,y,z, '*')

        if (x,y,z) in visited:
            # print('seen')
            continue
        visited.add((x,y,z))
        if (x,y,z) in cubes:
            shell.add((x,y,z))
            continue
        # Expand outwards
        for dx, dy, dz in [(-1,0,0), (1,0,0), (0,-1,0), (0,1,0), (0,0,-1), (0,0,1)]:
            xx, yy, zz = x+dx, y+dy, z+dz
            queue.append((xx, yy, zz))
            # if (xx,yy,zz) == (1, -1, 0) or (x,y,z) == (1, -1, 0):
            #     print("!!!")
            # if (xx,yy,zz) in cubes:
            #     print(f"{x,y,z} -> {xx,yy,zz}")
            #     count_visits[(xx,yy,zz)] += 1
            # else:
            #     print(f"{xx,yy,zz}")

    print(f"{len(shell)}/{len(cubes)}")
    print("visits")
    # for xyz in sorted(count_visits.keys()):
    #     near_225 = [(1,2,5),(3,2,5),(2,1,5),(2,3,5),(2,2,4),(2,2,6)]
    #     print(f"{xyz}: {count_visits[xyz]}" + ("*" if xyz in near_225 else ""))
    print(sum([val for _, val in count_visits.items()]))

if __name__ == '__main__':
    main()
