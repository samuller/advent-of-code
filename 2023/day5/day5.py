#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("../..")
from lib import *
from copy import deepcopy
from dataclasses import dataclass
import itertools


# @dataclass
# class Interval:
#     start: int
#     end: int


# def overlap(int1: Interval, int2: Interval):
#     start = max(int1.start, int2.start)
#     end = min(int1.end, int2.end)
#     return Interval(start, end)


def overlap(int1: Tuple[int, int], int2: Tuple[int, int]):
    start = max(int1[0], int2[0])
    end = min(int1[1], int2[1])
    return (start, end)


def missing_overlaps(int1: Tuple[int, int], int2: Tuple[int, int]):
    assert int_within_int(int2, int1)
    missing = []
    if int2[0] > int1[0]:
        missing.append((int1[0], int2[0]-1))
    if int2[1] < int1[1]:
        missing.append((int2[1]+1, int1[1]))
    return missing


def any_overlap(int1: Tuple[int, int], int2: Tuple[int, int]):
    if int2[0] <= int1[0] <= int2[1] or int2[0] <= int1[1] <= int2[1] \
        or int1[0] <= int2[0] <= int1[1] or int1[0] <= int2[1] <= int1[1]:
        return True
    return False


assert any_overlap((1857474741, 1913571382), (1857095529, 2671679898)) == True
assert any_overlap((1857095529, 2671679898), (1857474741, 1913571382)) == True


def int_within_int(int1: Tuple[int, int], int2: Tuple[int, int]):
    if int1[0] >= int2[0] and int1[1] <= int2[1]:
        return True
    return False


def overlap_mapping(prev: Tuple[int, int], src: Tuple[int, int], dest: Tuple[int, int]):
    # print("OVERMAP", prev, src, dest)
    # if not int_within_int(prev, src):
    #     return src, dest
    if not any_overlap(prev, src):
        return src, dest

    src = list(src)
    dest = list(dest)
    # print("before", prev, src, dest)
    diff = prev[0] - src[0]
    if diff > 0:
        # Cutt off start
        src[0] += diff
        dest[0] += diff
    diff = src[1] - prev[1]
    if diff > 0:
        # Cutt off end
        src[1] -= diff
        dest[1] -= diff
    # print("after", prev, src, dest)
    assert src[0] <= src[1], src
    assert dest[0] <= dest[1], dest
    return tuple(src), tuple(dest)


def create_missing_ranges(interval, overlaps):
    for rng1, rng2 in itertools.product(overlaps, overlaps):
        if rng1 == rng2:
            continue
        assert not any_overlap(rng1, rng2), f"{rng1}, {rng2}"

    # print("      LAPS", interval, overlaps)
    missing = []
    overlaps = sorted(overlaps)
    curr = interval[0]
    while curr <= interval[1]:
        # print("y", curr, overlaps)

        # if curr < overlaps[0][0]:
        #     missing.append((interval[0], overlaps[0][0]-1))
        #     curr = overlaps[0][0]
        #     del overlaps[0]
        #     continue

        # print(curr, interval[1])
        jump_forward = 0
        for lap in overlaps:
            if lap[0] <= curr <= lap[1]:
                curr = lap[1] + 1
                jump_forward += 1
        if jump_forward > 0:
            # print("z")
            for _ in range(jump_forward):
                del overlaps[0]
            # print("jump", overlaps)
            continue

        if len(overlaps) == 0:
            # print("B")
            missing.append((curr, interval[1]))
            curr = interval[1] + 1
        elif curr < overlaps[0][0]:
            # print("A")
            missing.append((curr, overlaps[0][0]-1))
            curr = overlaps[0][0]
            # del overlaps[0]

    # print("      LAPS -->", missing)
    return missing

assert create_missing_ranges((0, 36), [(0, 6), (11, 52)]) == [(7, 10)]


# Part 1
def generate_mapping(input, nums_to_keep):
    mapping = dict()
    for line in input:
        dest_start, src_start, range_len = [int(val) for val in line.split()]
        for num in nums_to_keep:
            if src_start <= num < src_start + range_len:
                offset = num - src_start
                # print(f"{num} => {dest_start + offset} ({dest_start}, {offset})")
                mapping[num] = dest_start + offset

    for num in nums_to_keep:
        if num not in mapping:
            mapping[num] = num
    return mapping


# Part 2
def generate_mapping_ranges(input, ranges_to_keep):
    mapping = dict()
    for line in input:
        dest_start, src_start, range_len = [int(val) for val in line.split()]
        src_rng = (src_start, src_start + range_len - 1)
        dest_rng = (dest_start, dest_start + range_len - 1)
        mapping[src_rng] = dest_rng

    # remove non-overlaps
    for rng in list(mapping.keys()):
        has_overlap = False
        for keep_rng in ranges_to_keep:
            if any_overlap(keep_rng, rng):
                has_overlap = True
                break
        if not has_overlap:
            del mapping[rng]
    # print("CLEANUP", mapping)
    # shrink to overlaps
    new_mapping = dict()
    for keep_rng in ranges_to_keep:
        for rng in list(mapping.keys()):
            if not any_overlap(keep_rng, rng):
                continue
            src, dest = overlap_mapping(keep_rng, rng, mapping[rng])
            new_mapping[src] = dest
    mapping = new_mapping
    # print("BREAKUP", mapping)

    # handle non-overlap identity-mappings
    for keep_rng in ranges_to_keep:
        overlaps = []
        for rng in list(mapping.keys()):
            if any_overlap(keep_rng, rng):
                overlaps.append(rng)
        if len(overlaps) == 0:
            mapping[keep_rng] = keep_rng
        elif len(overlaps) == 1 and overlaps[0] == keep_rng:
            pass
        else:
            missing = create_missing_ranges(keep_rng, overlaps)
            for miss in missing:
                mapping[miss] = miss
    # print("IDS", mapping)

    # BUG:!!!return new_mapping
    return mapping


def check_mapping_keys(mapping):
    assert (0, 0) not in mapping
    for rng in mapping.keys():
        assert rng[0] <= rng[1]
    for rng1, rng2 in itertools.product(mapping.keys(), mapping.keys()):
        if rng1 == rng2:
            continue
        assert not any_overlap(rng1, rng2), f"{rng1}, {rng2}"


def generate_mapping_ranges2(input, ranges_to_keep):
    mapping = dict()
    for line in input:
        dest_start, src_start, range_len = [int(val) for val in line.split()]
        src_rng = (src_start, src_start + range_len - 1)
        dest_rng = (dest_start, dest_start + range_len - 1)
        mapping[src_rng] = dest_rng
    print("INPUT", mapping, ranges_to_keep)

    check_mapping_keys(mapping)

    # print("HUh?", mapping.keys())
    for keep_rng in ranges_to_keep:
        overlaps = []
        for rng in list(mapping.keys()):
            if any_overlap(keep_rng, rng):
                overlaps.append(rng)
        if len(overlaps) == 0:
            # Add identity mapping
            mapping[keep_rng] = keep_rng
            check_mapping_keys(mapping)
        elif len(overlaps) == 1 and overlaps[0] == keep_rng:
            # Ignore perfect mapping
            pass
        else:
            # split_overlaps_and_create_missing(keep_rng, overlaps)
            # print()
            missing = create_missing_ranges(keep_rng, overlaps)
            for miss in missing:
                # for the_rng in mapping.keys():
                #     assert not any_overlap(miss, the_rng), f"MISS: {miss} / {the_rng}"
                mapping[miss] = miss
            check_mapping_keys(mapping)

    # print(mapping)
    check_mapping_keys(mapping)

    return mapping


def in_first(value, ranges):
    first_range = ranges[0]
    start, end = first_range
    return start <= value <= end


def traverse_mapping_ranges(new_mapping, ranges_to_keep):
    print("traverse", new_mapping, "/", ranges_to_keep)
    check_mapping_keys(new_mapping)
    new_ranges = sorted(list(new_mapping.keys()))
    ranges_to_keep = sorted(list(ranges_to_keep))

    change_points = []
    for edges in [*new_ranges, *ranges_to_keep]:
        change_points.append(edges[0])
        change_points.append(edges[1])
    change_points = sorted(change_points)
    print("change_points", change_points)

    mapping = dict()
    for idx in range(len(change_points)-1):
        curr = change_points[idx]
        next_ = change_points[idx+1]
        if curr == next_:
            continue
        next_ -= 1

        if len(new_ranges) == 0:
            mapping[(curr, next_)] = (curr, next_)
            check_mapping_keys(mapping)
            continue
        if len(ranges_to_keep) == 0:
            break

        range_to_keep = ranges_to_keep[0]
        while range_to_keep[1] < curr:
            ranges_to_keep.pop(0)
            if len(ranges_to_keep) == 0:
                range_to_keep = None
                break
            range_to_keep = ranges_to_keep[0]

        new_range = new_ranges[0]
        while new_range[1] < curr:
            new_ranges.pop(0)
            if len(new_ranges) == 0:
                new_range = None
                break
            new_range = new_ranges[0]

        if len(new_ranges) == 0:
            mapping[(curr, next_)] = (curr, next_)
            check_mapping_keys(mapping)
            continue
        if len(ranges_to_keep) == 0:
            break

        print("->", curr, new_range, range_to_keep)
        if curr < range_to_keep[0]:
            # Jump to next change-point until 
            print("A")
            # ranges_to_keep.pop(0)
            continue
        elif range_to_keep[0] <= curr <= range_to_keep[1]:
            print("B")
            if curr < new_range[0]:
                print("a")
                mapping[(curr, next_)] = (curr, next_)
                check_mapping_keys(mapping)
            elif new_range[0] <= curr <= new_range[1]:
                src, dest = overlap_mapping((curr, next_), new_range, new_mapping[new_range])
                print('b()', (curr, next_), new_range, new_mapping[new_range])
                print("b", src, dest)
                mapping[src] = dest
                check_mapping_keys(mapping)
                # mapping[(range_to_keep[0], curr)] = (range_to_keep[0], curr)

        # if new_range[0] <= curr <= new_range[1]:
        # if not in_first(curr, ranges_to_keep):
        #     continue
    print(mapping)
    check_mapping_keys(mapping)
    return mapping


# [13:46] 15147306 - too low
# bugs: return new_mapping, has_overlap not checking outer overlap (where 2nd arg fully covers 1st), rewrote create_missing_ranges
# Attempt other approach & found bugs in underlying functions
# [21:21] got answer after reverting back to first approach
def main():
    lines = [line.strip() for line in fileinput.input()]

    # Part 1
    seeds_to_plant = [int(val) for val in lines[0].split(": ")[1].split()]
    prev_mapping = dict()
    curr_mapping = dict()
    for group in grouped(lines[1:]):
        if group[0] == 'seed-to-soil map:':
            curr_mapping = generate_mapping(group[1:], seeds_to_plant)
        else:
            curr_mapping = generate_mapping(group[1:], prev_mapping.values())

        prev_mapping = curr_mapping
    print(min(curr_mapping.values()))

    # Part 2
    seed_ranges = []
    for idx in range(0, len(seeds_to_plant), 2):
        start, rng = seeds_to_plant[idx:idx+2]
        bgn, end = start, start + rng - 1
        seed_ranges.append((bgn, end))

    prev_mapping = dict()
    curr_mapping = dict()
    for group in grouped(lines[1:]):
        # Attempt 1 (seemed to work but answer was intially wrong)
        if group[0] == 'seed-to-soil map:':
            curr_mapping = generate_mapping_ranges(group[1:], seed_ranges)
        else:
            curr_mapping = generate_mapping_ranges(group[1:], prev_mapping.values())

        # Attempt 2 - incomplete
        # if group[0] == 'seed-to-soil map:':
        #     curr_mapping = generate_mapping_ranges2(group[1:], seed_ranges)
        # else:
        #     curr_mapping = generate_mapping_ranges2(group[1:], prev_mapping.values())

        # Attempt 3 - thought it would simplify - but still incomplete
        # new_mapping = dict()
        # for line in group[1:]:
        #     dest_start, src_start, range_len = [int(val) for val in line.split()]
        #     src_rng = (src_start, src_start + range_len - 1)
        #     dest_rng = (dest_start, dest_start + range_len - 1)
        #     new_mapping[src_rng] = dest_rng
        # if group[0] == 'seed-to-soil map:':
        #     curr_mapping = traverse_mapping_ranges(new_mapping, seed_ranges)
        # else:
        #     curr_mapping = traverse_mapping_ranges(new_mapping, prev_mapping.values())

        prev_mapping = curr_mapping
        # print(group[0])
        # print(curr_mapping)
        # print(len(curr_mapping))
        # exit()           
    # print(seed_to_soil)
    print(min(curr_mapping.values())[0])


if __name__ == '__main__':
    main()
