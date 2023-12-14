#!/usr/bin/env python3
import fileinput
from collections import deque

ROLL_NORTH = (-1, 0)
ROLL_SOUTH = ( 1, 0)
ROLL_WEST = (0, -1)
ROLL_EAST = (0,  1)


def range_to_limit(start, limits, steps):
    if steps < 0:
        return range(start, limits[0], steps)
    else:
        return range(start, limits[1], steps)


def print_rocks(rocks, walls, R, C):
    for rr in range(R):
        for cc in range(C):
            if (rr, cc) in rocks:
                assert (rr, cc) not in walls
                print('O', end="")
            elif (rr, cc) in walls:
                print('#', end="")
            else:
                print('.', end="")
        print()
    print()


def find_loops_at_end(history):
    # min_loop_len = len(history)
    # max_loop_len = 0
    for loop_len in range(1, len(history)//2):
        part1 = history[-loop_len:]
        part2 = history[-2*loop_len:-loop_len]
        assert len(part1) == len(part2), len(history)
        if part1 == part2:
            return loop_len
            # min_loop_len = min(min_loop_len, loop_len)
            # max_loop_len = max(max_loop_len, loop_len)
    return None


def tilt(walls, rocks, tilt_dir, limits):
    rock_set = set(rocks)
    outer_limits = (limits[0] - 1, limits[1] + 1)
    rolldir_rr, rolldir_cc = tilt_dir
    the_limit = min(limits) if rolldir_rr < 0 or rolldir_cc < 0 else max(limits)
    moved = 1
    total_move_count = 0
    while moved:
        moved = 0
        for idx in range(len(rocks)):
            rock = rocks[idx]
            old_rr = rock[0]
            old_cc = rock[1]
            # print(rock)
            new_rr = old_rr
            if rolldir_rr != 0:
                # print(old_rr, outer_limits, rolldir_rr)
                for new_rr in range_to_limit(old_rr, outer_limits, rolldir_rr):
                    # print(new_rr)
                    if new_rr == the_limit:
                        break
                    # Look one spot ahead
                    test_pos = (new_rr + rolldir_rr, old_cc + rolldir_cc)
                    if test_pos in walls or test_pos in rock_set:
                        # print("break", test_pos in walls, test_pos in rocks)
                        break

            new_cc = old_cc
            if rolldir_cc != 0:
                for new_cc in range_to_limit(old_cc, outer_limits, rolldir_cc):
                    if new_cc == the_limit:
                        break
                    # Look one spot ahead
                    test_pos = (old_rr + rolldir_rr, new_cc + rolldir_cc)
                    if test_pos in walls or test_pos in rock_set:
                        break

            diff_rr = abs(old_rr - new_rr)
            diff_cc = abs(old_cc - new_cc)
            moved += diff_rr
            moved += diff_cc
            # if diff_rr or diff_cc:
            #     print((old_rr, old_cc), '->', (new_rr, new_cc))
            rock_set.remove((old_rr, old_cc))
            rock_set.add((new_rr, new_cc))
            rocks[idx] = (new_rr, new_cc)
            # print(moved, rocks)
            # if idx == 5:
            #     exit()
        # print(moved)
        # exit()
        total_move_count += moved

    return rocks, total_move_count


# Part 1 - equals instead of assignment
# (1_000_000_000 - 102) % 42 = 16
# 89845 = 89803 + 16 steps
def main():
    lines = [line.strip() for line in fileinput.input()]

    walls = set()
    rocks = []
    R = len(lines)
    C = len(lines[0])
    for rr in range(R):
        row = [ch for ch in lines[rr]]
        assert len(row) == C
        # print(row)
        for cc in range(C):
            if row[cc] == 'O':
                rocks.append((rr, cc))
            if row[cc] == '#':
                walls.add((rr, cc))

    new_rocks, _ = tilt(walls, list(rocks), ROLL_NORTH, limits=(0, R-1))
    ans1 = 0
    for rock in new_rocks:
        ans1 += (R - rock[0])
    print(ans1)

    # print(rocks)
    # print(walls)
    # rock_count = len(set(rocks))
    track = []
    max_count = 1_000_000_000
    for count in range(max_count):
        move_count = 0
        rocks, moves = tilt(walls, rocks, ROLL_NORTH, limits=(0, R-1))
        move_count += moves
        # print_rocks(rocks, walls, R, C)
        rocks, moves = tilt(walls, rocks, ROLL_WEST, limits=(0, C-1))
        move_count += moves
        # print_rocks(rocks, walls, R, C)
        rocks, moves = tilt(walls, rocks, ROLL_SOUTH, limits=(0, R-1))
        move_count += moves
        # print_rocks(rocks, walls, R, C)
        rocks, moves = tilt(walls, rocks, ROLL_EAST, limits=(0, C-1))
        move_count += moves
        # print_rocks(rocks, walls, R, C)
        # assert len(set(rocks)) == len(rocks)

        ans1 = 0
        for rock in rocks:
            ans1 += (R-rock[0])
        track.append(ans1)
        loops = find_loops_at_end(track)
        # print(count, ans1, loops)
        # Ignore small possible loops caused by coincidental repititions within loops
        if loops is not None and loops > 4:
            # Convert max_count from counter (1-indexed) to index (0-indexed) since we prefer to do all
            # math in 0-indexed notations...
            max_count_idx = max_count - 1
            loop_start = 1 + count - 2*loops
            loop_offset = (max_count_idx - loop_start) % loops
            # print(loop_start, loop_offset)
            print(track[loop_start + loop_offset])
            exit()


if __name__ == '__main__':
    main()
