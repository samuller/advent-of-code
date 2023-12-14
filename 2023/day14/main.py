#!/usr/bin/env python3
import fileinput
# import sys; sys.path.append("../..")
# from lib import *


class Classy:
    def __init__(self):
        pass


def function(input):
    return False

# equals instead of assignment
def main():
    lines = [line.strip() for line in fileinput.input()]
    print(f'Lines: {len(lines)}')

    walls = set()
    rocks = []
    R = len(lines)
    C = len(lines[0])
    for rr in range(R):
        row = [ch for ch in lines[rr]]
        assert len(row) == C
        print(row)
        for cc in range(C):
            if row[cc] == 'O':
                rocks.append((rr, cc))
            if row[cc] == '#':
                walls.add((rr, cc))
    print(rocks)
    print(walls)

    # Roll north
    moved = 1
    while moved:
        moved = 0
        for idx in range(len(rocks)):
            rock = rocks[idx]
            old_rr = rock[0]
            cc = rock[1]
            # print(rock)
            new_rr = old_rr
            for new_rr in range(old_rr, -1, -1):
                # print(new_rr)
                # Look at next spot
                test_pos = (new_rr-1, cc)
                if new_rr == 0:
                    break
                if test_pos in walls or test_pos in rocks:
                    # print("break", test_pos in walls, test_pos in rocks)
                    break
            moved += abs(old_rr - new_rr)
            rocks[idx] = (new_rr, cc)
            # print(moved, rocks)
            # if idx == 5:
            #     exit()
        print(moved)
        # exit()
    
    ans1 = 0
    for idx, rock in enumerate(rocks):
        ans1 += (R-rock[0])
    print(ans1)


if __name__ == '__main__':
    main()
