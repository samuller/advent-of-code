#!/usr/bin/env python3
import fileinput
from dataclasses import dataclass
from collections import Counter, defaultdict
from typing import List, Tuple


# @dataclass
# class Coord:
#     x: int
#     y: int
#     z: int


# @dataclass
# class Brick:
#     start: Tuple[int, int, int]
#     end: Tuple[int, int, int]


Index = int
Coord = Tuple[int, int, int]
Brick = Tuple[Coord, Coord]


# Day 5
def overlap_interval(int1: Tuple[int, int], int2: Tuple[int, int]):
    start = max(int1[0], int2[0])
    end = min(int1[1], int2[1])
    return (start, end)


def drop_brick(brick):
    if brick_on_floor(brick):
        return brick
    bs, be = brick
    bs, be = list(bs), list(be)
    bs[2] -=1
    be[2] -=1
    return (tuple(bs), tuple(be))


def brick_on_floor(brick):
    st, en = brick
    if st[2] == 1 or en[2] == 1:
        return True
    return False


def brick_overlap(brick1, brick2):
    s1, e1 = brick1  #.start, brick.end
    s2, e2 = brick2  #.start, other.end
    overlap_region = []
    overlap = True
    for i in range(3):
        new_int = overlap_interval((s1[i], e1[i]), (s2[i], e2[i]))
        # If not an overlapping/valid interval
        if new_int[0] > new_int[1]:
            overlap = False
            break
        overlap_region.append(new_int)
        # if s2[i] <= s1[i] <= e2[i] or s2[i] <= e1[i] <= e2[i] \
        #     or s1[i] <= s2[i] <= e1[i] or s1[i] <= e2[i] <= e1[i]:
        #     overlap = True
        #     break

    # if overlap:
    #     print(overlap_region)
    return overlap, overlap_region


def find_first_overlap(bricks):
    for idx1, brick1 in enumerate(bricks):
        # Only need to consider (a,b), not also (b,a)
        # TODO: only consider those that even have x or y overlap (since they won't be changing)
        # TODO: only consider "neighbours"???
        for idx2 in range(idx1+1, len(bricks)):
            brick2 = bricks[idx2]
            overlap, overlap_region = brick_overlap(brick1, brick2)
            if overlap:
                print(overlap_region)
                # return (idx, idx2)
                return (brick1, brick2)
    return None



def does_overlap(brick1, bricks, ignore_idx=-1):
    for idx2, brick2 in enumerate(bricks):
        if idx2 == ignore_idx:
            continue
        overlap, overlap_region = brick_overlap(brick1, brick2)
        if overlap:
            # print(ignore_idx, idx2, overlap_region)
            return idx2
    return None


def get_overlaps(brick1, bricks, ignore_idx=-1):
    overlaps = []
    for idx2, brick2 in enumerate(bricks):
        if idx2 == ignore_idx:
            continue
        overlap, overlap_region = brick_overlap(brick1, brick2)
        if overlap:
            # print(ignore_idx, idx2, overlap_region, f"| {brick1} vs {brick2}")
            overlaps.append(idx2)
    return overlaps



def brick_xy_overlap(brick1, brick2) -> Tuple[bool, List[Tuple[int, int]]]:
    s1, e1 = brick1  #.start, brick.end
    s2, e2 = brick2  #.start, other.end
    overlap_region = []
    overlap = True
    # Only look in x & y dimensions
    for i in range(2):
        new_int = overlap_interval((s1[i], e1[i]), (s2[i], e2[i]))
        # If not an overlapping/valid interval
        if new_int[0] > new_int[1]:
            overlap = False
            break
        overlap_region.append(new_int)
    return overlap, overlap_region


def find_xy_overlaps(brick1, bricks, ignore_idx=-1) -> List[Index]:
    overlaps = []
    for idx2, brick2 in enumerate(bricks):
        if idx2 == ignore_idx:
            continue
        overlap, _ = brick_xy_overlap(brick1, brick2)
        if overlap:
            overlaps.append(idx2)
    return overlaps


def apply_gravity(bricks: List[Brick]):
    # Group bricks into columns of possible interaction since xy-coords never change
    xy_overlaps = {}
    for idx, brick in enumerate(bricks):
        overlaps = find_xy_overlaps(brick, bricks, ignore_idx=idx)
        # print(f"{idx} => {len(overlaps)}")
        # Have to use indexes since brick positions will be changing as they fall
        xy_overlaps[idx] = overlaps
        # print("no xy overlap", idx)

    # Drop all bricks
    settled_bricks = [brick_on_floor(b) for b in bricks]
    held_up_by: List[List[Index]] = [[] for _ in bricks]
    next_idx = 0
    stable_count = Counter(settled_bricks)[True]
    while not all(settled_bricks):
        # print(Counter(stable_bricks))
        # print(stable_count)

        # print(stable_bricks)
        # next_idx is a counter so that we're never stuck checking the same brick after each iteration
        try:
            idx = next_idx + settled_bricks[next_idx:].index(False)
        except ValueError:
            # print("reset next_idx")
            next_idx = 0
            continue
        # print(idx)
        # pre_drop = bricks[idx]
        post_drop = drop_brick(bricks[idx])

        # overlap_idx = does_overlap(post_drop, bricks, ignore_idx=idx)
        xy_bricks = [bricks[oidx] for oidx in xy_overlaps[idx]]
        xy_overlap_idx = does_overlap(post_drop, xy_bricks)
        if xy_overlap_idx is None:
            # print(post_drop, overlap_idx)
            bricks[idx] = post_drop
            if brick_on_floor(post_drop):
                settled_bricks[idx] = True
                stable_count += 1
        else:
            # Get index in original list
            overlap_idx = xy_overlaps[idx][xy_overlap_idx]
            # bricks.index(xy_overlaps[idx][xy_overlap_idx])
            # print(post_drop, overlap_idx, bricks[overlap_idx])
            if settled_bricks[overlap_idx]:
                settled_bricks[idx] = True
                stable_count += 1
                held_up_by[idx].append(overlap_idx)
            else:
                # next_idx = overlap_idx
                next_idx = (idx + 1) % len(settled_bricks)
    return bricks


# [9:11] 603 too high (dropping bricks takes 4min!) - didn't count cant_be_shared
# [10:34] part 2: 1434 too low [didn't account for shared also falling when multiple consequently removed]
# [11:29] 42152 too low [didn't account for multi-layer affects, e.g. parts of "shared" getting removed at different steps]
def main():
    lines = [line.strip() for line in fileinput.input()]
    bricks = []
    for line in lines:
        start, end = line.split('~')
        start = [int(c) for c in start.split(',')]
        end = [int(c) for c in end.split(',')]
        bricks.append((start, end))

    # check all bricks are single block lines
    for brick in bricks:
        st, en = brick
        assert st[0] == en[0] or st[1] == en[1] or st[2] == en[2]

    # bricks[1] = drop_brick(bricks[1])
    # assert find_first_overlap(bricks) is None, find_first_overlap(bricks)
    # print(bricks)

    bricks = apply_gravity(bricks)
    # pre-calced fallen

    # Determine which bricks we can remove
    shared_support = set()
    doesnt_supports_others = set(range(len(bricks)))
    cant_be_shared = set()
    keeps_up = defaultdict(set)
    for idx, brick in enumerate(bricks):
        assert brick[0][2] > 0 and brick[1][2] > 0
        post_drop = drop_brick(brick)
        overlaps = get_overlaps(post_drop, bricks, ignore_idx=idx)
        if len(overlaps) > 1:
            for br in overlaps:
                shared_support.add(br)
        if len(overlaps) == 1:
            cant_be_shared.add(overlaps[0])
        if len(overlaps) == 0:
            # Extra check that bricks have fallen correctly
            assert brick_on_floor(brick)
        keeps_up[frozenset(overlaps)].add(idx)
        for br in overlaps:
            # keeps_up[br].add(idx)
            if br in doesnt_supports_others:
                doesnt_supports_others.remove(br)
        # print(idx, overlaps)
    # Remove shared blocks that are also holding up other non-shared blocks
    shared_support = shared_support.difference(cant_be_shared)
    assert len(cant_be_shared.intersection(shared_support)) == 0
    assert len(shared_support.intersection(doesnt_supports_others)) == 0
    can_be_removed = shared_support.union(doesnt_supports_others)
    assert len(can_be_removed) == len(shared_support) + len(doesnt_supports_others)
    print(len(can_be_removed))

    # Part 2
    # print(keeps_up)
    ans2 = 0
    for idx in range(len(bricks)):
        if idx in can_be_removed:
            continue
        would_fall = set()
        next_to_fall = keeps_up[frozenset([idx])]
        # while we've detected new falling blocks
        while not next_to_fall.issubset(would_fall):
            would_fall = would_fall.union(next_to_fall)
            new_next_to_fall = set()
            for combo in keeps_up:
                if len(combo) == 0:
                    continue
                if combo.issubset(would_fall):
                    new_next_to_fall = new_next_to_fall.union(keeps_up[combo])
            next_to_fall = new_next_to_fall
        ans2 += len(would_fall)
    print(ans2)


if __name__ == '__main__':
    main()
