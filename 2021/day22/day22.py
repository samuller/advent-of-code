#!/usr/bin/env python3
import itertools
import fileinput
from collections import defaultdict
# import sys; sys.path.append("../..")
# from lib import *


class Classy:
    def __init__(self):
        pass


def in_range(xyz, xyz_rng):
    xs, ys, zs = xyz_rng
    x,y,z = xyz
    valid_x = xs[0]<=x<=xs[1]
    valid_y = ys[0]<=y<=ys[1]
    valid_z = zs[0]<=z<=zs[1]
    return valid_x and valid_y and valid_z


def valid_xyz_range(xyz_rng):
    xs, ys, zs = xyz_rng
    valid_x = -50<=xs[0] and xs[1]<=50
    valid_y = -50<=ys[0] and ys[1]<=50
    valid_z = -50<=zs[0] and zs[1]<=50
    return valid_x and valid_y and valid_z


# def range_inside_range(xyz_rng1, xyz_rng2):
#     xs1, ys1, zs1 = xyz_rng1
#     xlim, ylim, zlim = xyz_rng2
#     valid_x = xlim[0]<=xs1[0] and xs1[1]<=xlim[1]
#     valid_y = ylim[0]<=ys1[0] and ys1[1]<=ylim[1]
#     valid_z = zlim[0]<=zs1[0] and zs1[1]<=zlim[1]
#     return valid_x and valid_y and valid_z


def ranges_overlap(xyz_rng1, xyz_rng2):
    xs1, ys1, zs1 = xyz_rng1
    xs2, ys2, zs2 = xyz_rng2
    valid_x = xs1[0]<=xs2[0]<=xs1[1] or xs2[0]<=xs1[0]<=xs2[1]
    valid_y = ys1[0]<=ys2[0]<=ys1[1] or ys2[0]<=ys1[0]<=ys2[1]
    valid_z = zs1[0]<=zs2[0]<=zs1[1] or zs2[0]<=zs1[0]<=zs2[1]
    # print(valid_x, valid_y, valid_z, ys1[1]>ys2[0], ys2[1]>ys1[0],
    #     ys1, ys2, ys1[1], ys2[0], ys2[1], ys1[0])
    return valid_x and valid_y and valid_z


def merge_range(xyz_rng1, xyz_rng2):
    xs1, ys1, zs1 = xyz_rng1
    xs2, ys2, zs2 = xyz_rng2
    new_rng = tuple([
        (min(xs1[0], xs2[0]), max(xs1[1], xs2[1])),
        (min(ys1[0], ys2[0]), max(ys1[1], ys2[1])),
        (min(zs1[0], zs2[0]), max(zs1[1], zs2[1])),
    ])
    return new_rng


def merge_ranges(ranges):
    rng_idxs = range(len(ranges))

    print('before', len(ranges))
    while True:
        overlap_found = None
        # for pair in itertools.combinations(list(range(len(ranges))), 2):
        for pair in itertools.combinations(ranges, 2):
            assert pair[0] != pair[1]
            xyz_rng1, xyz_rng2 = pair[0], pair[1]
            if ranges_overlap(xyz_rng1, xyz_rng2):
                # print('merge?', pair)
                # exit()
                overlap_found = pair
                break
        if overlap_found is None:
            break
        ranges.remove(pair[0])
        ranges.remove(pair[1])
        # print('merged', pair, merge_range(pair[0], pair[1]))
        ranges.add(merge_range(pair[0], pair[1]))
    print('after', len(ranges))

    # to_merge = []
    # merged = []
    # for pair in itertools.product(list(rng_idxs), list(rng_idxs)):
    #     if pair[0] == pair[1]:
    #         continue
    #     xyz_rng1 = ranges[pair[0]]
    #     xyz_rng2 = ranges[pair[1]]
    #     if ranges_overlap(xyz_rng1, xyz_rng2):
    #         to_merge.append(pair)
    #         print('overlap', xyz_rng1, xyz_rng2)
    #         xs1, ys1, zs1 = xyz_rng1
    #         xs2, ys2, zs2 = xyz_rng2
    #         new_rng = [
    #             (min(xs1, xs2), max(xs1, xs2)),
    #             (min(ys1, ys2), max(ys1, ys2)),
    #             (min(zs1, zs2), max(zs1, zs2)),
    #         ]
    #         merged.append(new_rng)
    # print('to_merge', to_merge)
    # new_ranges = []

    # for idx in rng_idxs:
    #     if 
    return ranges # new_ranges


def main():
    lines = [line.strip() for line in fileinput.input()]
    print(f'Lines: {len(lines)}')

    # cubes = set()
    steps = []
    # ranges = defaultdict(set)
    for line in lines:
        fields = line.split(' ')
        assert len(fields) == 2
        status = fields[0]
        xyz_str = fields[1].split(',')
        assert len(xyz_str) == 3
        xs = tuple([int(n) for n in xyz_str[0][2:].split('..')])
        ys = tuple([int(n) for n in xyz_str[1][2:].split('..')])
        zs = tuple([int(n) for n in xyz_str[2][2:].split('..')])
        # ranges[status].add((xs, ys, zs))
        steps.append((status, (xs, ys, zs)))
        # counter += []
        print(xs, ys, zs)
        # curr_cubes = itertools.product(
        #     list(range(min(-50, xs[0]), max(50, xs[1])+1)),
        #     list(range(min(-50, ys[0]), max(50, ys[1])+1)),
        #     list(range(min(-50, zs[0]), max(50, zs[1])+1)))
        # # print(len(list(curr_cubes)))
        # for cube in curr_cubes:
        #     cubes.add(cube)
        # print(len(cubes))
    print(steps)
    merged_steps = []
    status, xyz_rng = steps[0]
    curr_status = status
    curr_ranges = set([xyz_rng])
    for step in steps[1:]:
        status, xyz_rng = step
        if status != curr_status:
            merged_steps.append((curr_status, curr_ranges))
            curr_status = status
            curr_ranges = set([xyz_rng])
        else:
            curr_ranges.add(xyz_rng)
    merged_steps.append((curr_status, curr_ranges))
    print("merged")
    for idx in range(len(merged_steps)):
        status, xyz_rngs = merged_steps[idx]
        xyz_rngs = merge_ranges(xyz_rngs)
        merged_steps[idx] = (status, xyz_rngs)
        print(merged_steps[idx])

    # ranges['off'] = merge_ranges(ranges['off'])
    # ranges['on'] = merge_ranges(ranges['on'])
    # print(ranges)

    counter = 0
    for x in range(-50, 50+1):
        for y in range(-50, 50+1):
            for z in range(-50, 50+1):
                last_status = 'off'
                for step in steps:
                    status, xyz_rng = step
                    # for xyz_rng in xyz_rngs:
                    if not valid_xyz_range(xyz_rng):
                        continue
                    if in_range((x,y,z), xyz_rng):
                        last_status = status
                if last_status == 'on':
                    # print(x,y,z)
                    counter += 1

                # for xyz_rng in ranges['on']:
                #     if not valid_xyz_range(xyz_rng):
                #         # print(xyz_rng)
                #         continue
                #     if in_range((x,y,z), xyz_rng):
                #         counter += 1
                # for xyz_rng in ranges['off']:
                #     if not valid_xyz_range(xyz_rng):
                #         # print(xyz_rng)
                #         continue
                #     if in_range((x,y,z), xyz_rng):
                #         counter -= 1
                # exit()
    print(counter)
    # print(len(cubes))


if __name__ == '__main__':
    main()
