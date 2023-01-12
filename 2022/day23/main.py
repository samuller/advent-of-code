#!/usr/bin/env python3
import itertools
import fileinput

import sys; sys.path.append("../..")
from lib import *


def get_limits(elves):
    any_r, any_c = next(iter(elves))
    min_r, max_r = any_r, any_r
    min_c, max_c = any_c, any_c
    for elf in elves:
        r, c, = elf
        min_r = min(min_r, r)
        max_r = max(max_r, r)
        min_c = min(min_c, c)
        max_c = max(max_c, c)
    # print(f"{min_r}-{max_r}, {min_c}-{max_c}")
    return ((min_r, max_r), (min_c, max_c))


def count_fields(elves):
    ((min_r, max_r), (min_c, max_c)) = get_limits(elves)
    empty_fields = 0
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if (r, c) not in elves:
                empty_fields += 1
    return empty_fields


def print_elves(elves):
    ((min_r, max_r), (min_c, max_c)) = get_limits(elves)
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if (r, c) in elves:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print()


# 7:24 - wrong 2886
# 7:38 - wrong 3890
# 7:55 - pt2. wrong 15902 (looked at wrong output value)
def main():
    lines = [line.replace("\n", "") for line in fileinput.input()]
    # print(lines)

    elves = set()
    for row, line in enumerate(lines):
        for col, chr in enumerate(line):
            val = lines[row][col]
            if val == '#':
                elves.add((row, col))
                continue
            assert val == '.'
    # print_elves(elves)

    offsets = {
        'N': [(-1, 0), (-1, 1), (-1,-1)],
        'S': [( 1, 0), ( 1, 1), ( 1,-1)],
        'W': [( 0,-1), ( 1,-1), (-1,-1)],
        'E': [( 0, 1), ( 1, 1), (-1, 1)],
    }
    ordering = ['N', 'S', 'W', 'E']
    count_at_start = len(elves)
    # for round in range(10):  # part1
    round = 0
    while True:
        round += 1
        # print(round, ordering)
        # first half of round
        proposed_moves = {}
        for elf in elves:
            r, c, = elf
            # print(elf)
            has_neighbour = False
            for dr, dc in itertools.product([-1,0,1],[-1,0,1]):
                if (dr, dc) == (0, 0):
                    continue
                if (r+dr, c+dc) in elves:
                    has_neighbour = True
                    break
            if not has_neighbour:
                # print("nomove", elf)
                continue

            for dir in ordering:
                # print(dir)
                is_empty = True
                for dr, dc in offsets[dir]:
                    if (r+dr, c+dc) in elves:
                        is_empty = False
                if is_empty:
                    dr, dc = offsets[dir][0]
                    proposed_moves[elf] = (r+dr, c+dc)
                    break
        # second half of round
        # print(proposed_moves)
        all_moves = list(proposed_moves.values())
        move_count = 0
        for elf, new_pos in proposed_moves.items():
            # print(f"[] {elf} -> {new_pos}")
            if all_moves.count(new_pos) == 1:
                move_count += 1
                elves.remove(elf)
                elves.add(new_pos)
                # print(f"{elf} -> {new_pos}")
        assert len(elves) == count_at_start
        # print_elves(elves)
        if move_count == 0:
            part2 = round
            break
        dir = ordering.pop(0)
        ordering.append(dir)
        if round == 10:
            part1 = count_fields(elves)

    # print_elves(elves)
    print(part1)
    print(part2)


if __name__ == '__main__':
    main()
