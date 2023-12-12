#!/usr/bin/env python3
import math
import itertools
import fileinput
from collections import Counter
# import sys; sys.path.append("../..")
# from lib import *


def calc_data(springs):
    count = 0
    contig = []
    for c in springs:
        if c == '#':
            count += 1
        if c == '.' and count != 0:
            contig.append(count)
            count = 0
    if count != 0:
        contig.append(count)
    # print(contig)
    return contig


assert calc_data([c for c in ".###.##...#.#.#"]) == [3,2,1,1,1]


def possibilities(springs, data):
    print(springs, data)
    counts = Counter(springs)
    # print(list(itertools.combinations(['.', '#'], 3)))
    # print(list(itertools.permutations(('.', '#'), 2)))
    # print(list(itertools.product(('.', '#'), repeat=3)))
    ans = 0
    for poss in itertools.product(('.', '#'), repeat=counts.get('?', 0)):
        imagine = list(springs)
        # print(poss)
        pidx = 0
        for idx, spring in enumerate(springs):
            if spring == '?':
                imagine[idx] = poss[pidx]
                pidx += 1
        if calc_data(imagine) == data:
            # print(imagine)
            ans += 1
    # ans = math.pow(2, counts.get('?', 0))
    # print(counts)
    
    # ans = 0
    # print(ans)
    return ans

assert possibilities([c for c in "?###????????"], [3,2,1]) == 10


def main():
    lines = [line.strip() for line in fileinput.input()]
    print(f'Lines: {len(lines)}')

    ans1 = 0
    for line in lines:
        springs, data = line.split(' ')
        springs = [c for c in springs]
        data = [int(d) for d in data.split(",")]
        assert set(springs) - set(['#', '.', '?']) == set()
        ans1 += possibilities(springs, data)
    print(ans1)


if __name__ == '__main__':
    main()
