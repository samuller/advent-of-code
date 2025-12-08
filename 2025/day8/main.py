#!/usr/bin/env python3
import fileinput
from math import *
import sys; sys.path.append("../..")
from lib import *


def calc_dist(pos1, pos2):
    dist = sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2 + (pos2[2] - pos1[2])**2)
    return dist


def main():
    lines = [line.strip() for line in fileinput.input()]

    junctions = []
    for line in lines:
        xyz_pos = tuple([int(dim) for dim in line.split(',')])
        assert xyz_pos not in junctions
        junctions.append(xyz_pos)

    distances = []
    seen = set()
    for pos1 in junctions:
        for pos2 in junctions:
            if pos1 == pos2:
                continue
            key = tuple(sorted([pos1, pos2]))
            if key not in seen:
                dist = calc_dist(pos1, pos2)
                distances.append((dist, key))
            seen.add(key)

    # circuits = []
    p1 = 0
    p2 = 0
    # Don't store which exact pairs are connected
    circuit_juncs = []
    distances.sort()
    count = 0
    for dist, (pos1, pos2) in distances:  # part1: distances[0:1000]:
        found = []
        for circ_idx, circ in enumerate(circuit_juncs):
            if pos1 in circ or pos2 in circ:
                found.append(circ_idx)
            # if connection in circuits:
            #     found = circ_idx
        assert len(found) < 3, found
        if len(found) == 0:
            # circuits.append([connection])
            circuit_juncs.append(set([pos1, pos2]))
        elif len(found) == 1:
            juncs1 = circuit_juncs[found[0]]
            juncs1.add(pos1)
            juncs1.add(pos2)
            if len(juncs1) == len(junctions):
                p2 = pos1[0] * pos2[0]
                break
        elif len(found) == 2:
            # Merge two connected sets of junctions
            juncs1 = circuit_juncs[found[0]]
            juncs2 = circuit_juncs[found[1]]
            for junc in juncs2:
                juncs1.add(junc)
            del circuit_juncs[found[1]]
            if len(juncs1) == len(junctions):
                p2 = pos1[0] * pos2[0]
                break
        count += 1
        if count == 10 or count == 1000:
            # for circ in circuit_juncs:
            #     print(len(circ))
            lengths = sorted([len(circ) for circ in circuit_juncs], reverse=True)
            p1 = prod(lengths[:3])

    print(p1)
    print(p2)


if __name__ == '__main__':
    main()
