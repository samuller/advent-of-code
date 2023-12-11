#!/usr/bin/env python3
import fileinput
import itertools


def examples(g1, g2, dist):
    if (g1, g2) == ((5, 1), (9, 4)):
        # 1st example
        assert dist == 9, dist
    if (g1, g2) == ((0, 3), (8, 7)):
        # 2nd example
        assert dist == 15, dist
    if (g1, g2) == ((2, 0), (6, 9)):
        # 3nd example
        assert dist == 17, dist
    if (g1, g2) == ((9, 0), (9, 4)):
        # 4th example
        assert dist == 5, dist


# Part 1:
# - delayed with typo in expansion ("< col <" was row)
#   - but I investigated adding 1 to Manhattan distances...
#   - had to add all example data as asserts
# Part 2:
# [7:41] not 779033026240 [multiplication vs addition]
def main():
    lines = [line.strip() for line in fileinput.input()]
    print(f'Lines: {len(lines)}')

    R = len(lines)
    C = len(lines[0])
    galaxies = []
    empty_rows = set()
    empty_cols = set()
    for rr in range(R):
        assert len(lines[rr]) == C
        if all([c == "." for c in lines[rr]]):
            empty_rows.add(rr)
    for cc in range(C):
        col = [lines[rr][cc] for rr in range(R)]
        if all([c == "." for c in col]):
            empty_cols.add(cc)
    # print(empty_rows)
    # print(empty_cols)

    for rr in range(R):
        row = [c for c in lines[rr]]
        for cc in range(C):
            if row[cc] == '#':
                galaxies.append((rr, cc))
                continue
            assert row[cc] == '.', f"Val: '{row[cc]}'"
    # print(galaxies)

    ans1 = 0
    ans2 = 0
    expansion = [2, 1000000]
    for g1, g2 in itertools.combinations(galaxies, 2):
        assert g1 != g2
        # Manhattan distance
        dist = abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])
        dist2 = dist
        for row in empty_rows:
            if min(g1[0], g2[0]) < row < max(g1[0], g2[0]):
                dist += (expansion[0] - 1)
                dist2 += (expansion[1] - 1)
                # print("Row", row)
        for col in empty_cols:
            if min(g1[1], g2[1]) < col < max(g1[1], g2[1]):
                dist += (expansion[0] - 1)
                dist2 += (expansion[1] - 1)
                # print("Col", col)
        # print(g1, g2, dist)
        # examples(g1, g2, dist)
        ans1 += dist
        ans2 += dist2
    print(ans1)
    print(ans2)


if __name__ == '__main__':
    main()
