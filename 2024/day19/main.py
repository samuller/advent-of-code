#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("../..")
from lib import *


CACHE = {}
def solve(want, available):
    if want in CACHE:
        return CACHE[want]
    if len(want) == 0:
        return 1
    possibilities = []
    for towel in available:
        if want.startswith(towel):
            possibilities.append(towel)
    counts = 0
    for poss in possibilities:
        attempt = want[len(poss):]
        counts += solve(attempt, available)
    assert want not in CACHE
    CACHE[want] = counts
    return counts


# 7:11 - 228 wrong attempt #1
# 7:25 right attempt #2
# 7:38 part2 - wrong 3510259888632
def main():
    lines = [line.strip() for line in fileinput.input()]
    available = list(grouped(lines))[0][0].split(", ")
    wanted = list(grouped(lines))[1]
    p1 = 0
    p2 = 0
    for want in wanted:
        found = solve(want, available)
        if found > 0:
            p1 += 1
        # else:
        #     print(want)
        p2 += found

    # for want in wanted:
    #     print(f"=== {want} ===")
    #     # attempts = [want]
    #     attempts = set([want])
    #     found = 0
    #     # counts_as = defaultdict(lambda: 1)  # randomness???
    #     counts_as = {}
    #     while len(attempts) > 0:
    #         print(attempts, counts_as)
    #         attempt = attempts.pop()
    #         if attempt in counts_as:
    #             parent_count = counts_as[attempt] + 1
    #         else:
    #             parent_count = 1
    #         possibilities = []
    #         for towel in available:
    #             if attempt.startswith(towel):
    #                 possibilities.append(towel)
    #         for poss in possibilities:
    #             change = attempt[len(poss):]
    #             if change in counts_as:
    #                 count = counts_as[change] + parent_count
    #             else:
    #                 count = parent_count
    #             if len(change) == 0:
    #                 found += count
    #             else:
    #                 attempts.add(change)
    #                 counts_as[change] = count
    #     if found > 0:
    #         p1 += 1
    #     # else:
    #     #     print(want)
    #     p2 += found
    #     print(want, found)
    print(p1)
    print(p2)

if __name__ == '__main__':
    main()
