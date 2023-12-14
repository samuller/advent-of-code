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
    idx = 0
    while history.count(history[-1 + idx]) > 1:
        pass
    return idx


def tilt(walls, rocks, tilt_dir, limits):
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
                    if test_pos in walls or test_pos in rocks:
                        # print("break", test_pos in walls, test_pos in rocks)
                        break

            new_cc = old_cc
            if rolldir_cc != 0:
                for new_cc in range_to_limit(old_cc, outer_limits, rolldir_cc):
                    if new_cc == the_limit:
                        break
                    # Look one spot ahead
                    test_pos = (old_rr + rolldir_rr, new_cc + rolldir_cc)
                    if test_pos in walls or test_pos in rocks:
                        break

            diff_rr = abs(old_rr - new_rr)
            diff_cc = abs(old_cc - new_cc)
            moved += diff_rr
            moved += diff_cc
            # if diff_rr or diff_cc:
            #     print((old_rr, old_cc), '->', (new_rr, new_cc))
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
    # print(rocks)
    # print(walls)
    # rock_count = len(set(rocks))
    track = []
    for count in range(1_000_000_000):
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
        print(count+1, ans1)
        find_loops_at_end(track)
        # exit()


if __name__ == '__main__':
    main()
