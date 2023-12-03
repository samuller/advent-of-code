#!/usr/bin/env python3
from collections import defaultdict
import fileinput
import itertools


def find_adjacent(schematic, row_idx, start, end):
    # How I should've detected the 2nd & 3rd bugs
    assert "".join(schematic[row_idx][start:end]).isdecimal(), schematic[row_idx][start:end]

    adjacent = dict()
    for col_idx in range(start, end):
        for dr, dc in itertools.product([-1,0,1],[-1,0,1]):
            if [dr, dc] == [0, 0]:
                continue
            if not 0 <= row_idx + dr < len(schematic):
                continue
            if not 0 <= col_idx + dc < len(schematic[row_idx]):
                continue
            neigh = schematic[row_idx + dr][col_idx + dc]
            # How I detected the third bug
            if neigh.isdecimal():
                assert dr == 0, f"[{start}:{end}] {row_idx} + {dr} => {neigh}"

            if neigh != '.' and not neigh.isdecimal():
                adjacent[(row_idx + dr, col_idx + dc)] = neigh
    return adjacent


# [7:20] 530002 [end of line]
# [7:27] 533040 [end of line offsets end]
# [7:27-7:34] delay 
# [8:03] ponder
# [8:20] 531167 [end of line offsets start]
# [8:25] finally
def main():
    lines = [line.strip() for line in fileinput.input()]

    schematic = []
    for line in lines:
        schematic.append(list(line))
        assert len(schematic[-1]) == len(schematic[0])

    ans1 = 0
    gear_ratios = defaultdict(list)
    for row_idx in range(len(schematic)):
        line = schematic[row_idx]
        curr_number = ""
        for col_idx, val in enumerate(line):
            if val.isdecimal():
                curr_number += val
            # If possible end of number
            if not val.isdecimal() or col_idx == len(line) - 1:
                end_idx = col_idx
                # Workaround for bugs
                if val.isdecimal() and col_idx == len(line) - 1:
                    end_idx = col_idx + 1
                if len(curr_number) > 0:
                    adj = find_adjacent(schematic, row_idx, end_idx - len(curr_number), end_idx)
                    # print(curr_number, adj)
                    if len(adj) > 0:
                        ans1 += int(curr_number)
                    # Part 2
                    for key, val in adj.items():
                        if val == '*':
                            gear_ratios[key].append(int(curr_number))
                    curr_number = ""
    print(ans1)

    # Part 2
    # print(gear_ratios)
    ans2 = 0
    for key, gears in gear_ratios.items():
        if len(gears) != 2:
            continue
        ans2 += gears[0]*gears[1]
    print(ans2)


if __name__ == '__main__':
    main()
