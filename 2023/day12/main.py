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
    ans = count_possibilities_bruteforce(springs, data)
    return ans

# assert inter_possibilities([c for c in "?###????????"], [3,2,1]) == 10


def valid_gaps(data, spring_count):
    assert sum(data)+(len(data) - 1) <= spring_count, f"{sum(data)}+{(len(data) - 1)} < {spring_count}"
    # endpoints + in-between
    gaps = 2 + (len(data) - 1)
    # Gaps between data numbers, but excluding mandatory in-between gaps
    gap_count = spring_count - sum(data) - (len(data) - 1)
    # print(gap_count)
    # generate variations of "gaps"x numbers that sum to spring_count
    for variant in itertools.product(range(gap_count+1), repeat=gaps):
        # print(variant)
        if (sum(variant) == gap_count):
            yield variant


def count_possibilities_matching_gaps(springs, data):
    print(springs, data)
    ans = 0

    # known_springs

    for variant in valid_gaps(data, len(springs)):
        # Check if gap variation matches known springs
        for idx, dt in enumerate(data):
            pass

    #     valid = True
    #     for idx, spring in enumerate(springs):
    #         if spring == '?':
    #             continue
    #         elif poss[idx] != spring:
    #             valid = False
    #             break
    #     if valid:
    #         ans += 1

    # ans = math.pow(2, counts.get('?', 0))
    # print(ans)
    return ans


def valid_possibilities(data, spring_count):
    for variant in valid_gaps(data, spring_count):
        # print(variant)
        # Generate springs from data and gaps variation

        # Slow
        # poss = []
        # for idx, num in enumerate(variant):
        #     poss.extend(["."]*num)
        #     if idx != len(variant)-1:
        #         poss.extend(["#"]*data[idx])
        #         if idx != len(variant)-2:
        #             poss.append(".")
        # assert len(poss) == spring_count, len(poss)

        # Faster?
        poss = ['?']*spring_count
        pidx = 0
        for idx, num in enumerate(variant):
            for _ in range(num):
                poss[pidx] = "."
                pidx += 1
            if idx != len(variant)-1:
                for _ in range(data[idx]):
                    poss[pidx] = "#"
                    pidx += 1
                if idx != len(variant)-2:
                    poss[pidx] = "."
                    pidx += 1
        # assert len(poss) == spring_count, len(poss)

        # print(variant, poss)
        yield poss


# assert valid_possibilities([1,2,3], 10)


# 128 -> 1
# 2048 -> 38760
# 131072 -> 45
# 512 -> 8008
# 512 -> 8008
# 524288 -> 3003
# 2.6s -> 14.8s
def count_possibilities_only_valid(springs, data):
    print(springs, data)
    ans = 0
    count = 0
    for poss in valid_possibilities(data, len(springs)):
        # Check variation is valid with known data
        count += 1
        valid = True
        for idx, spring in enumerate(springs):
            if spring == '?':
                continue
            elif poss[idx] != spring:
                valid = False
                break
        if valid:
            ans += 1
    print(count)
    # ans = math.pow(2, counts.get('?', 0))
    # print(ans)
    return ans


def count_possibilities_bruteforce(springs, data):
    print(springs, data)
    ans = 0

    counts = Counter(springs)
    count = 0
    for poss in itertools.product(('.', '#'), repeat=counts.get('?', 0)):
        count += 1
        # Generate valid variation from permutation
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
    print(count)
    # ans = math.pow(2, counts.get('?', 0))
    # print(ans)
    return ans

assert count_possibilities_bruteforce([c for c in "?###????????"], [3,2,1]) == 10


def main():
    lines = [line.strip() for line in fileinput.input()]

    ans1 = 0
    ans2 = 0
    for line in lines:
        springs, data = line.split(' ')
        springs = [c for c in springs]
        data = [int(d) for d in data.split(",")]
        assert set(springs) - set(['#', '.', '?']) == set()

        func = count_possibilities_bruteforce
        # func = count_possibilities_only_valid

        ans1 += count_possibilities_only_valid(springs, data)
        continue
        repeat = 5
        unfolded = [*springs, '?'] * repeat
        unfolded = unfolded[:-1]

        # counts = Counter(unfolded)
        # if counts['?'] > len(unfolded) or counts['?'] > 16:
        #     func = count_possibilities_only_valid
        # print(' '*6, func.__name__, counts['?'], len(unfolded))

        # ans2 += count_possibilities_bruteforce(unfolded, data * 2)
        ans2 += func(unfolded, data * repeat)
        # unfolded = [*springs, '?'] * 5
        # unfolded = unfolded[:-1]
        # ans2 += count_possibilities(unfolded, data * 5)
        # ans2 += count_possibilities(springs, data) * 5
        # ans2 += inter_possibilities(springs, data) * 4
    print(ans1)
    print(ans2)


if __name__ == '__main__':
    main()
