#!/usr/bin/env python3
import fileinput

import sys; sys.path.append("../..")
from lib import *

EMPTY = (None, None)
DEBUG = False


def delete_nones(merged_ranges):
    to_delete = []
    for idx in range(len(merged_ranges)):
        if merged_ranges[idx] == EMPTY:
            to_delete.append(idx)
    for delete_idx in sorted(to_delete, reverse=True):
        del merged_ranges[delete_idx]


# part 2:
# 7:42 350962167667295
# 8:14 while True 350779870097238 too high
# 8:18 also sort before each
def main():
    lines = grouped([line.strip() for line in fileinput.input()])

    p1 = 0
    fresh = next(lines)
    ranges = []
    for line in fresh:
        beg, end = line.split("-")
        beg, end = int(beg), int(end)
        ranges.append((beg, end))
    # print(ranges)
    ingredients = next(lines)
    for id in ingredients:
        fresh = False
        for beg, end in ranges:
            if beg <= int(id) <= end:
                fresh = True
        if fresh:
            p1 += 1
    print(p1)

    p2 = 0
    # while True:
    #     rnd_range = merged_ranges.pop()
    merged_ranges = sorted(ranges)
    loops = 0
    while True:
        changes = 0
        # Delete Nones so we can sort
        delete_nones(merged_ranges)
        merged_ranges = sorted(merged_ranges)
        # print("START")
        for idx in range(len(merged_ranges)-1):
            beg1, end1 = merged_ranges[idx]
            beg2, end2 = merged_ranges[idx+1]
            if (beg1, end1) == EMPTY or (beg2, end2) == EMPTY:
                continue
            # Check individual ranges are consistent
            assert end1 >= beg1 and end2 >= beg2 and end2-beg2 >= 0 and end1-beg1 >= 0
            # If 2nd range covers 1st
            if beg2 <= beg1 and end1 <= end2:
                # print(idx, "2nd")
                # Clear 1st with empty sentinel value
                merged_ranges[idx] = EMPTY
                changes += 1
                continue
            # If 1st range covers 2nd
            if beg1 <= beg2 and end2 <= end1:
                # print(idx, "1st")
                # Remove 1st and have it repplace 2nd (swap ranges?)
                merged_ranges[idx] = EMPTY
                merged_ranges[idx+1] = beg1, end1
                changes += 1
                continue
            # If order is now wrong?
            if beg2 <= beg1 and end2 <= end1:
                # print(idx, "swap", f"{beg1},{end1} vs. {beg2},{end2}")
                # Then swap (bubble sort?)
                # ... leads to requiring more iterations
                tmp = tuple((beg2, end2))
                beg2, end2 = beg1, end1
                beg1, end1 = tmp
                changes += 1
                # print("    ", f"{beg1},{end1} vs. {beg2},{end2}")
            assert beg2 >= beg1, f"{beg1},{end1} vs. {beg2},{end2} ({beg1 <= beg2 and end2 <= end1})"
            # Double check
            assert end1 >= beg1 and end2 >= beg2 and end2-beg2 >= 0 and end1-beg1 >= 0
            # if beg2 - end2 == 0:
            # If no overlap
            if end1 < beg2:
                assert end1 >= beg1 and end2 >= beg2 and end2-beg2 >= 0 and end1-beg1 >= 0
                # print(beg2-end1)
                merged_ranges[idx] = beg1, end1
                merged_ranges[idx+1] = beg2, end2
                continue
            beg2 = end1 + 1
            if end2 < beg2:
                end2 = beg2
            changes += 1
            merged_ranges[idx] = beg1, end1
            merged_ranges[idx+1] = beg2, end2
            assert not (beg2 <= beg1 <= end2) and not (beg2 <= end1 <= end2) and not (beg1 <= beg2 <= end1) and not (beg1 <= end2 <= end1)

        loops += 1
        if changes == 0:
            break
    print(loops, "loops")

    # Delete Nones so we can sort
    delete_nones(merged_ranges)
    # Sort so we can make sure consecutive checks are working
    # assert merged_ranges == sorted(merged_ranges)
    # merged_ranges.sort()
    # Do second check that order was maintained
    for idx in range(len(merged_ranges)-1):
        beg1, end1 = merged_ranges[idx]
        # print(beg1, end1)
        beg2, end2 = merged_ranges[idx+1]
        if (beg1, end1) == EMPTY or (beg2, end2) == EMPTY:
            continue
        assert end1 >= beg1 and end2 >= beg2 and end2-beg2 >= 0 and end1-beg1 >= 0
        assert (beg1, end1) < (beg2, end2)
        assert not (beg2 <= beg1 <= end2) and not (beg2 <= end1 <= end2) and not (beg1 <= beg2 <= end1) and not (beg1 <= end2 <= end1)
    # print(merged_ranges[-1])

    # print(merged_ranges)
    for beg, end in merged_ranges:
        # print(beg, end)
        if (beg, end) == EMPTY:
            continue
        p2 += 1 + (end - beg)
    print(p2)


if __name__ == '__main__':
    main()
