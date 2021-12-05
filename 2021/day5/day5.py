#!/usr/bin/env python3
import fileinput
import itertools
from collections import Counter


def path(x1, y1, x2, y2):
    adder_x = 1 if x2 >= x1 else -1
    adder_y = 1 if y2 >= y1 else -1

    horz = list(range(x1, x2 + adder_x, adder_x))
    vert = list(range(y1, y2 + adder_y, adder_y))

    max_len = max(len(horz), len(vert))
    if abs(x2-x1) == abs(y2-y1):
        max_len = abs(x2-x1)
        print(horz, vert, max_len)
    # print(horz*max_len, vert*max_len)
    if len(horz) == 1:
        horz = horz * max_len
    if len(vert) == 1:
        vert = vert * max_len

    # if x1 == x2 or y1 == y2:
    # comb = [(x,y) for x in horz for y in vert]
    # comb = list(itertools.product(horz, vert))

    comb = []
    for idx in range(len(horz)):
        comb.append((horz[idx], vert[idx]))
    # for x in horz:
    #     for y in vert:
    #         comb.append((x,y))

    print(horz, vert, comb)
    return comb


assert path(2,2,2,1) == [(2,2), (2,1)]
assert path(1,1,1,3) == [(1,1), (1,2), (1,3)]
assert path(9,7,7,7) == [(9,7), (8,7), (7,7)]
assert path(9,7,7,9) == [(9,7), (8,8), (7,9)], path(9,7,7,9)
assert path(1,1,3,3) == [(1,1), (2,2), (3,3)], path(1,1,3,3)


# 7:24 102120
# bugs:
# - wrong order of function params
# - key, value (on tuple key) without counts.items()
def main():
    lines = [line.strip() for line in fileinput.input()]
    print(f'Lines: {len(lines)}')

    vents = []
    for line in lines:
        start, _, end = line.split(' ')
        x1, y1 = start.split(',')
        x1, y1 = int(x1), int(y1)
        x2, y2 = end.split(',')
        x2, y2 = int(x2), int(y2)
        assert x1 == x2 or y1 == y2 or (abs(x2-x1) == abs(y2-y1)), line

        # Part 1
        # if x1 != x2 and y1 != y2:
        #     # print(line)
        #     continue

        comb = path(x1, y1, x2, y2)
        print(line)
        print(comb)
        vents.append(comb)
    
    all_locs = []
    for vent in vents:
        all_locs.extend(vent)
    counts = Counter(all_locs)
    print(counts)

    count_2_pluses = 0
    for loc, count in counts.items():
        # print(count, loc)
        if count >= 2:
            count_2_pluses += 1
    print(count_2_pluses)



if __name__ == '__main__':
    main()

