#!/usr/bin/env python3
import math
import itertools
import fileinput
from collections import Counter
# import sys; sys.path.append("../..")
# from lib import *

seen_calc = {}
def calc_data(springs):
    springs = tuple(springs)
    if springs in seen_calc:
        return seen_calc[springs]

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
    seen_calc[springs] = contig
    return contig


assert calc_data([c for c in ".###.##...#.#.#"]) == [3,2,1,1,1]


def inter_possibilities(springs, data):
    springs = springs + ['?'] + list(springs)
    data = data + list(data)
    ans = possibilities(springs, data)
    return ans

# assert inter_possibilities([c for c in "?###????????"], [3,2,1]) == 10


def possibilities(springs, data):
    print(springs, data)
    counts = Counter(springs)
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
    return ans

assert possibilities([c for c in "?###????????"], [3,2,1]) == 10


def main():
    lines = [line.strip() for line in fileinput.input()]
    print(f'Lines: {len(lines)}')

    ans1 = 0
    ans2 = 0
    for line in lines:
        springs, data = line.split(' ')
        springs = [c for c in springs]
        data = [int(d) for d in data.split(",")]
        assert set(springs) - set(['#', '.', '?']) == set()
        # ans1 += possibilities(springs, data)
        # ans2 += possibilities(springs * 5, data * 5)
        ans2 += possibilities(springs, data) * 5
        ans2 += inter_possibilities(springs, data) * 4
    print(ans1)
    print(ans2)


if __name__ == '__main__':
    main()
