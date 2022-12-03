#!/usr/bin/env python3
import fileinput
from copy import copy
from collections import defaultdict


# bugs:
# - kept strings & order instead of just pair counts
# - had loop counting down -1 (each with dictionary writes), instead of full subtraction
def main():
    lines = [line.strip() for line in fileinput.input()]
    print(f'Lines: {len(lines)}')

    polymer = None
    steps = {}
    for line in lines:
        if polymer is None:
            polymer = line #list(line)
            continue
        if not line:
            continue
        frm,to = line.split(' -> ')
        assert len(frm) == 2
        assert len(to) == 1
        assert frm not in steps
        steps[frm] = to

    print(polymer)
    last = polymer[-1]
    poly = defaultdict(int)
    for i in range(len(polymer)-1):
        poly[polymer[i:i+2]] += 1
    print(poly)
    print(len(poly)+1)
    print(steps)

    for i in range(40):
        new_poly = copy(poly)
        for p in poly:
            count = poly[p]
            if count <= 0:
                continue
            if p in steps:
                frm, to = p, steps[p]
                new_poly[p] += -count
                new_poly[frm[0]+to] += count
                new_poly[to+frm[1]] += count

        poly = new_poly
        print(f'step {i+1}: {sum(poly.values())+1}')

    counts = defaultdict(int)
    for p in poly:
        counts[p[0]] += poly[p]
    counts[last] += 1
    print(counts)
    print(max(counts.values()) - min(counts.values()))


if __name__ == '__main__':
    main()
