#!/usr/bin/env python3
import math
import fileinput
import itertools
from collections import defaultdict, namedtuple
import sys; sys.path.append("../..")
from lib import *


Location = namedtuple('Location', ['x', 'y', 'z'])

MATCHES_NEEDED = 12
class RelID:
    def __init__(self, ids=None):
        self.ids = ids
        if ids is None:
            self.ids = set()

    def add(value):
        self.ids.add(value)
    
    def __eq__(self, other_id):
        count = 0
        for id in self.ids:
            if id in other_id.ids:
                count += 1
        return count >= MATCHES_NEEDED or count == len(self.ids)
    
    def __repr__(self):
        return str(self.ids)

def location(x,y,z=0):
    return Location(x=x, y=y, z=z)


def distance(loc1, loc2):
    dx = loc2.x - loc1.x
    dy = loc2.y - loc1.y
    dz = loc2.z - loc1.z
    return math.sqrt(dx**2 + dy**2 + dz**2)


def angles(loc1, loc2):
    dx = loc2.x - loc1.x
    dy = loc2.y - loc1.y
    dz = loc2.z - loc1.z
    return (math.atan2(dx,dy), math.atan2(dy,dz))


def abs_diff(loc1, loc2):
    dx = abs(loc1.x - loc2.x)
    dy = abs(loc1.y - loc2.y)
    dz = abs(loc1.z - loc2.z)
    return location(dx, dy, dz)


def calc_id(origin, neighbours):
    id = set()
    for neighbour in neighbours:
        id.add(abs_diff(origin, neighbour))
    return RelID(id)


def calc_ids(beacons):
    ids = []
    for beacon in beacons:
        bid = calc_id(beacon, beacons)
        ids.append(bid)
    return ids


def match_ups(beacons1, beacons2):
    ids1 = calc_ids(beacons1)
    ids2 = calc_ids(beacons2)
    # print(scanner, ids)
    match_up = []
    for id in ids2:
        # assert id in ref_ids
        if id in ids1:
            match_up.append(ids1.index(id))
        else:
            match_up.append(None)
    return match_up
    


def main():
    lines = [line.strip() for line in fileinput.input()]
    print(f'Lines: {len(lines)}')

    # scanner: don't know position or 90-degree rotation
    # 24 directions (6 facing, 4 up):
    # - facing x: +-, y: +-, z: +-
    # - up
    # x,y,z (3) * rotations (4) * negative/positive

    count_valid = 0
    beacons = defaultdict(list)
    for lines in grouped(lines):
        name = int(lines[0].split()[2])
        for line in lines[1:]:
            # print(line)
            xy = [int(n) for n in line.split(',')]
            # beacons[name].append(tuple(xy))
            beacons[name].append(location(*xy))
        # print(name, '->', len(beacons[name]))
    # print(beacons)
  
    # 0,0 4,-1 3,1 / -4,1 0,0 -1,2 / -3,-1 1,-2 0,0
    # 0,0 -4,1 -1,2 / 4,-1 0,0 3,1 / 1,-2 -3,-1 0,0
    # 3,1 4,1 1,2
    ref_ids = calc_ids(beacons[0])
    # print('ref', ref_ids)
    for scanner in beacons.keys():
        # rel_beacon = beacons[scanner][0]
        # id = calc_id(rel_beacon, beacons[scanner])
        # print(id)
        match_up = match_ups(beacons[0], beacons[scanner])
        # print(scanner, match_up)

    # print(list(itertools.product(['x','y','z'], [-1, 1], [0,90,180,270])))
    # exit()
    uniq_count = 0
    for scanner1, scanner2 in itertools.combinations(beacons.keys(), 2):
        print(f'compare {scanner1} and {scanner2}')
        beacons1 = beacons[scanner1]
        beacons2 = beacons[scanner2]
        match_up = match_ups(beacons1, beacons2)
        uniq_count += len([match for match in match_up if match is not None])
        print(uniq_count, match_up)
        # for orientation in itertools.product(['x','y','z'], [-1, 1], [0,90,180,270]):
        #     axis, sign, rot = orientation
        #     face = f'-{axis}' if sign < 0 else axis
        #     print(face, rot)
        # print(beacons1)
        # print(beacons2)
        # exit()


if __name__ == '__main__':
    main()
