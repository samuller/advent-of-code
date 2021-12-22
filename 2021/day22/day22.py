#!/usr/bin/env python3
import itertools
import fileinput
from collections import defaultdict
# import sys; sys.path.append("../..")
# from lib import *


def count_cubes(xyz_rng):
    xs, ys, zs = xyz_rng
    diff_x = 1 + xs[1] - xs[0]
    diff_y = 1 + ys[1] - ys[0]
    diff_z = 1 + zs[1] - zs[0]
    return diff_x*diff_y*diff_z


def get_overlap(xyz_rng1, xyz_rng2):
    xs1, ys1, zs1 = xyz_rng1
    xs2, ys2, zs2 = xyz_rng2
    overlap = tuple([
        (max(xs1[0], xs2[0]), min(xs1[1], xs2[1])),
        (max(ys1[0], ys2[0]), min(ys1[1], ys2[1])),
        (max(zs1[0], zs2[0]), min(zs1[1], zs2[1])),
    ])
    # print(overlap)
    return overlap


# def count_ons(on_cubes):
#     count = 0
#     for idx in range(len(on_cubes)):
#         curr = on_cubes[idx]
#         new_count = count_cubes(curr)
#         # Subtract overlaps with previous "on" steps
#         for prev_idx in range(idx):
#             prev = on_cubes[prev_idx]
#             new_count -= count_cubes(get_overlap(curr, prev))
#         count += new_count
#     return count


def count_new_on(new_on_cube, on_cubes):
    count = count_cubes(new_on_cube)
    # Subtract overlaps with previous "on" steps
    for cube in on_cubes:
        count -= count_cubes(get_overlap(new_on_cube, cube))
    return count


def count_new_off(new_off_cube, on_cubes):
    count = 0
    # Count only overlaps with previous "on" steps
    for curr_on in on_cubes:
        count += count_cubes(get_overlap(new_off_cube, curr_on))
    # Subtract previous "on" steps that were double-counted due to overlaps
    for pair in itertools.combinations(on_cubes, 2):
        pair_overlap = get_overlap(pair[0], pair[1])
        count -= count_cubes(get_overlap(new_off_cube, pair_overlap))
    return count


def count_new_on_prev_off(new_on_cube, off_cubes):
    count = 0
    # Count parts of cube that have been put on after previously being put off
    for curr_off in off_cubes:
        count += count_cubes(get_overlap(new_on_cube, curr_off))
    # Subtract previous "off" steps that were double-counted due to overlaps
    for pair in itertools.combinations(off_cubes, 2):
        pair_overlap = get_overlap(pair[0], pair[1])
        count -= count_cubes(get_overlap(new_on_cube, pair_overlap))
    return count


def count_new_off_prev_off(new_off_cube, on_cubes, off_cubes, on_after_off_cubes):
    count = 0
    for curr_on in on_cubes:
        count += count_cubes(get_overlap(new_off_cube, curr_on))
    # for curr_off in off_cubes:
    #     count -= count_cubes(get_overlap(new_off_cube, get_overlap(curr_off, any previous on))

    count = count_new_off(new_off_cube, on_cubes)
    # count = count_new_off(new_off_cube, on_after_off_cubes)
    
    # Subtract previous "off" steps that were double-counted due to overlaps
    for pair in itertools.combinations(off_cubes, 2):
        pair_overlap = get_overlap(pair[0], pair[1])
        count -= count_cubes(get_overlap(new_off_cube, pair_overlap))
    return count


ex1 = ((10,12), (10,12), (10,12))  # on
ex2 = ((11,13), (11,13), (11,13))  # on
ex3 = ((9,11), (9,11), (9,11))  # off
ex4 = ((10,10), (10,10), (10,10))  # on
assert count_new_on(ex1, []) == 27
assert count_new_on(ex2, [ex1]) == 19
assert count_new_off(ex3, [ex1, ex2]) == 8
assert count_new_on_prev_off(ex4, [ex3]) == 1
assert count_new_on_prev_off(ex4, [ex3, ex3]) == 1

assert count_cubes(ex2) - count_cubes(get_overlap(ex1,ex2)) == 19
assert count_cubes(get_overlap(ex3,ex1)) \
    + count_cubes(get_overlap(ex3,ex2)) \
    - count_cubes(get_overlap(ex3, get_overlap(ex1,ex2))) == 8
assert count_cubes(ex4) == 1


def count_diff_on(new_on_cube, steps):
    overlap_history = []
    for step in steps:
        state, cube = step
        overlap_history.append((state, get_overlap(curr_cube, new_on_cube)))
    count = 0
    for idx in range(len(overlap_history)):
        state, overlap_cube = overlap_history[idx]
    # for overlap in overlap_history:
        # state, overlap_cube = overlap
        # for pair in itertools.combinations(overlap_history[:idx], 2):
    return count


def count_all(steps):
    counter = 0
    for idx in range(len(steps)):
        status, xyz_rng = steps[idx]
        if status == 'on':
            prev_ons = [cube for state, cube in steps[:idx] if state == 'on']
            counter += count_new_on(xyz_rng, prev_ons)
            prev_offs = [cube for state, cube in steps[:idx] if state == 'off']
            counter += count_new_on_prev_off(xyz_rng, prev_offs)
        else:
            prev_ons = [cube for state, cube in steps[:idx] if state == 'on']
            counter -= count_new_off(xyz_rng, prev_ons)
    return counter


tst1 = ((10,15), (10,15), (10,15))
assert count_all([('on', tst1)]) == 6**3
tst2 = ((11,14), (11,14), (11,14))
assert count_all([('on', tst1), ('off', tst2)]) == 6**3 - 4**3
tst3 = ((13,17), (13,17), (13,17))
assert count_all([('on', tst1), ('on', tst3)]) == 6**3 + (5**3 - 3**3)
assert count_all([('on', tst1), ('off', tst2), ('on', tst3)]) == 6**3 - 4**3 \
    + (5**3 - (3**3 - count_cubes(get_overlap(tst3, tst2))))
assert count_all([('on', tst1), ('off', tst2), ('on', tst3), ('off', tst2)]) == \
    6**3 - 4**3 + (5**3 - (3**3 - count_cubes(get_overlap(tst3, tst2)))) \
    - count_cubes(get_overlap(tst3, tst2))
# assert count_all([('on', tst1), ('on', tst3), ('off', tst2)]) == (6**3 + 4**3 - 3**3)
# assert count_new_off(tst2, [tst1]) == 4**3
# assert count_cubes(get_overlap(tst1, tst2)) == (6**3 - 4**3)


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


def ranges_overlap(xyz_rng1, xyz_rng2):
    xs1, ys1, zs1 = xyz_rng1
    xs2, ys2, zs2 = xyz_rng2
    valid_x = xs1[0]<=xs2[0]<=xs1[1] or xs2[0]<=xs1[0]<=xs2[1]
    valid_y = ys1[0]<=ys2[0]<=ys1[1] or ys2[0]<=ys1[0]<=ys2[1]
    valid_z = zs1[0]<=zs2[0]<=zs1[1] or zs2[0]<=zs1[0]<=zs2[1]
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

    real_steps = []
    for line in lines:
        fields = line.split(' ')
        assert len(fields) == 2
        status = fields[0]
        xyz_str = fields[1].split(',')
        assert len(xyz_str) == 3
        xs = tuple([int(n) for n in xyz_str[0][2:].split('..')])
        ys = tuple([int(n) for n in xyz_str[1][2:].split('..')])
        zs = tuple([int(n) for n in xyz_str[2][2:].split('..')])
        real_steps.append((status, (xs, ys, zs)))

    # normalise steps:
    # - prevent double-counting overlapping "on" steps
    #  - by adding fake "off" steps for overlapping region
    # - prevent over-counting (subtracting) non-overlapping "off" steps
    #  - by splitting "off" step into only overlapping regions
    # - prevent double-counting overlapping "off" steps
    #  - by adding fake "on" steps for overlapping regions
    norm_steps = [real_steps[0]]
    for idx in range(1, len(real_steps)):
        status, xyz_rng = real_steps[idx]
        if status == 'on':
            # add extra "off" steps to prevent double-counting "on"
            # consider overlaps with all previous real "on" steps
            fake_offs = []
            for prev in real_steps[0:idx]:
                if prev[0] == 'off':
                    continue
                # add extra "off" steps to prevent double-counting "on"
                ## - but prevent it from overlapping with previous "off"s?
                ## (but only where new "on" overlaps with previous... while
                ## also accounting for previously generated "off" steps...)
                overlap = get_overlap(prev[1], xyz_rng)
                if count_cubes(overlap) != 0:
                    fake_offs.append(('off', overlap))

            norm_steps.append(real_steps[idx])
            norm_steps.extend(fake_offs)
        # adjust "off" to only consider parts that overlap with previous "on" steps
        # (i.e. remove irrelevant portions too prevent over-counting "off" steps)
        else:
            adjusted_offs = []
            # replace it with a generated "off" for each overlap with a previous real "on"
            for prev in real_steps[0:idx]:
                if prev[0] == 'off':
                    continue
                overlap = get_overlap(prev[1], xyz_rng)
                if count_cubes(overlap) != 0:
                    adjusted_offs.append(('off', overlap))
            # fix overlaps with previous real "offs"
            fake_ons = []
            for prev in real_steps[0:idx]:
                if prev[0] == 'on':
                    continue
                overlap = get_overlap(prev[1], xyz_rng)
                if count_cubes(overlap) != 0:
                    fake_ons.append(('on', overlap))

            norm_steps.extend(adjusted_offs)
            norm_steps.extend(fake_ons)
    print(len(real_steps), '->', len(norm_steps))
    # for step in real_steps:
    #     print('real', step)
    # for step in norm_steps:
    #     print('norm', step)

    # merged_steps = []
    # status, xyz_rng = steps[0]
    # curr_status = status
    # curr_ranges = set([xyz_rng])
    # for step in steps[1:]:
    #     status, xyz_rng = step
    #     if status != curr_status:
    #         merged_steps.append((curr_status, curr_ranges))
    #         curr_status = status
    #         curr_ranges = set([xyz_rng])
    #     else:
    #         curr_ranges.add(xyz_rng)
    # merged_steps.append((curr_status, curr_ranges))
    # print("merged")
    # for idx in range(len(merged_steps)):
    #     status, xyz_rngs = merged_steps[idx]
    #     xyz_rngs = merge_ranges(xyz_rngs)
    #     merged_steps[idx] = (status, xyz_rngs)
    #     print(merged_steps[idx])

    # Part 1
    # counter = 0
    # for x in range(-50, 50+1):
    #     for y in range(-50, 50+1):
    #         for z in range(-50, 50+1):
    #             last_status = 'off'
    #             for step in steps:
    #                 status, xyz_rng = step
    #                 # for xyz_rng in xyz_rngs:
    #                 if not valid_xyz_range(xyz_rng):
    #                     continue
    #                 if in_range((x,y,z), xyz_rng):
    #                     last_status = status
    #             if last_status == 'on':
    #                 # print(x,y,z)
    #                 counter += 1
    # print(counter)

    # Part 2 - normalised
    # counter = 0
    # for step in norm_steps:
    #     status, xyz_rng = step
    #     # print(counter, step)
    #     if status == 'on':
    #         counter += count_cubes(xyz_rng)
    #     else:
    #         counter -= count_cubes(xyz_rng)
    # print(counter)

    # Part 2 - direct counts
    counter = count_all(real_steps)
    print(counter)


if __name__ == '__main__':
    main()
