#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("../..")
from lib import *
from copy import deepcopy


#[7:24]
# curr_mapping = generate_mapping(lines[1:], prev_mapping.values())
# if lines[0] == 'seed-to-soil map:':
#     # seed_to_soil = generate_mapping(lines[1:], seeds_to_plant)
#     new_mapping = {key: val for key, val in curr_mapping.items() if key in seeds_to_plant}
#     for seed in seeds_to_plant:
#         if seed not in new_mapping:
#             new_mapping[seed] = seed
#     curr_mapping = new_mapping
# else:
#     new_mapping = {key: val for key, val in curr_mapping.items() if key in prev_mapping.values()}
#     for val in prev_mapping.values():
#         if val not in new_mapping:
#             new_mapping[val] = val
#     curr_mapping = new_mapping
#[7:28]
# def generate_mapping(input, nums_to_keep):
#     mapping = dict()
#     for line in input:
#         dest_start, src_start, range_len = [int(val) for val in line.split()]
#         src = list(range(src_start, src_start + range_len))
#         dest = list(range(dest_start, dest_start + range_len))
#         assert len(src) == len(dest)
#         # print(src)
#         # print(dest)
#         for idx in range(len(src)):
#             assert src[idx] not in mapping, f"{idx} / {src[idx]} / {mapping[src[idx]]}"
#             mapping[src[idx]] = dest[idx]
#             # prev = seed_to_soil.get(src[idx], sys.maxsize)
#             # seed_to_soil[src[idx]] = min(dest[idx], prev)

#     new_mapping = {key: val for key, val in mapping.items() if key in nums_to_keep}
#     for val in nums_to_keep:
#         if val not in new_mapping:
#             new_mapping[val] = val
#     mapping = new_mapping
#     return mapping


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


def generate_mapping_ranges(input, ranges_to_keep):
    mapping = dict()
    for line in input:
        dest_start, src_start, range_len = [int(val) for val in line.split()]
        for rng in ranges_to_keep:
            bgn, end = rng
            old_size = end - bgn
            if src_start <= bgn < src_start + range_len:
                offset = bgn - src_start
                bgn = dest_start + offset
            if src_start <= end < src_start + range_len:
                offset = end - src_start
                # print(f"{num} => {dest_start + offset} ({dest_start}, {offset})")
                end = dest_start + offset
            # new_size = end - bgn
            # assert new_size <= old_size
            mapping[rng] = (bgn, end)
            # if new_size < old_size:
            #     pass
            # if new_size > old_size:
            #     pass

    new_mapping = deepcopy(mapping)
    for rng in mapping:
        bgn, end = rng
        size = end - bgn

        new_rng = mapping[rng]
        new_bgn, new_end = mapping[rng]
        new_size = new_end - new_bgn

        if new_size != size:
            print("missing", rng, new_rng)
            if new_bgn != bgn:
                assert new_end == end
                new_mapping[(bgn, new_bgn-1)] = (bgn, new_bgn-1)
            if new_end != end:
                assert new_bgn == bgn
                # new_mapping[[]]
                assert False
    mapping = new_mapping

    # for rng in ranges_to_keep:
    #     bgn, end = rng
    #     if num not in mapping:
    #         mapping[num] = num
    return mapping


def main():
    lines = [line.strip() for line in fileinput.input()]
    print(f'Lines: {len(lines)}')

    # Part 1 - 
    seeds_to_plant = [int(val) for val in lines[0].split(": ")[1].split()]

    # prev_mapping = dict()
    # curr_mapping = dict()
    # print(seeds_to_plant)
    # for lines in grouped(lines[1:]):
    #     if lines[0] == 'seed-to-soil map:':
    #         curr_mapping = generate_mapping(lines[1:], seeds_to_plant)
    #     else:
    #         curr_mapping = generate_mapping(lines[1:], prev_mapping.values())

    #     prev_mapping = curr_mapping
    #     # print(curr_mapping)
    #     # exit()           
    # # print(seed_to_soil)
    # print(min(curr_mapping.values()))

    # Part 2
    seed_ranges = []
    for idx in range(0, len(seeds_to_plant), 2):
        start, rng = seeds_to_plant[idx:idx+2]
        bgn, end = start, start + rng - 1
        seed_ranges.append((bgn, end))
    print(seed_ranges)

    prev_mapping = dict()
    curr_mapping = dict()
    for lines in grouped(lines[1:]):
        if lines[0] == 'seed-to-soil map:':
            curr_mapping = generate_mapping_ranges(lines[1:], seed_ranges)
        else:
            curr_mapping = generate_mapping_ranges(lines[1:], prev_mapping.values())

        prev_mapping = curr_mapping
        print(lines[0])
        print(curr_mapping)
        # exit()           
    # print(seed_to_soil)
    print(min(curr_mapping.values()))
    

if __name__ == '__main__':
    main()
