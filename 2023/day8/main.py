#!/usr/bin/env python3
import math
import fileinput
import sys; sys.path.append("../..")
from lib import *


def follow_multiple(starts, instructions, nodes):
    """Follow multiple paths via brute-force.
    
    Doesn't work fast enough with given data, but more generally applicable to any data.
    """
    currs = list(starts)
    steps_needed = [0] * len(currs)

    steps = 0
    ins_idx = 0
    while not all([curr[-1] == "Z" for curr in currs]):
        ins = instructions[ins_idx % len(instructions)]
        ins_idx += 1
        for idx, curr in enumerate(currs):
            if ins == "L":
                currs[idx] = nodes[curr][0]
            elif ins == "R":
                currs[idx] = nodes[curr][1]
            else:
                assert False, ins
            # Used in test data to indicate unreachable nodes
            assert currs[idx] != "XXX", currs
            if currs[idx][-1] == "Z" and steps_needed[idx] == 0:
                steps_needed[idx] = steps + 1
                # print(steps_needed, prod(steps_needed), prod(steps_needed) < best_ans)
        # if prod(steps_needed) != 0 and prod(steps_needed) < best_ans:
        #     best_ans = prod(steps_needed)
        #     print(best_ans)
        steps += 1

    print(currs)
    print(steps_needed, prod(steps_needed))
    return math.lcm(*steps_needed)


# https://stackoverflow.com/questions/15347174/python-finding-prime-factors
def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i == 0:
            n = n//i
            factors.append(i)
        else:
            i += 1
    factors.append(n)
    return factors

assert prime_factors(600851475143) == [71, 839, 1471, 6857]


def follow_cycles(starts, instructions, nodes):
    """Process data with expectation of proper cycles in graph."""
    steps_needed = []

    for start in starts:
        steps = follow(start, instructions, nodes, lambda val: val[-1] == "Z")
        steps_needed.append(steps)
    lcm = math.lcm(*steps_needed)
    # Can also take all prime factors, remove duplicates and multiple them all together.
    primes = set([p for n in steps_needed for p in prime_factors(n)])
    assert prod(primes) == lcm
    return lcm


def follow(start, instructions, nodes, is_end = lambda val: val == "ZZZ"):
    curr = start
    steps = 0
    ins_idx = 0
    while not is_end(curr):
        ins = instructions[ins_idx % len(instructions)]
        ins_idx += 1
        if ins == "L":
            curr = nodes[curr][0]
        elif ins == "R":
            curr = nodes[curr][1]
        else:
            assert False, ins
        steps += 1
    assert is_end(curr)
    # assert ins_idx == steps + 1
    return steps


# [7:27] 18792518403772666320570269
# [7:38] 18792518403772666320570269 // 263 (GCD) = 71454442599896069659963
# [7:44] 56787204941 (multiplied without 263s, e.g. // 263^5)
# [7:45] correct (multiplied with one 263)
def main():
    lines = [line.strip() for line in fileinput.input()]

    instructions = lines[0]
    part2_starts = []
    assert lines[1] == ""
    nodes = dict()
    for line in lines[2:]:
        node, neigh = line.split(' = ')
        # Remove brackets
        neigh = neigh[1:-1]
        left, right = neigh.split(", ")
        # print(node, left, right)
        assert node not in nodes
        nodes[node] = (left, right)
        if node[-1] == "A":
            part2_starts.append(node)

    if "AAA" in nodes:
        ans1 = follow("AAA", instructions, nodes)
        print(ans1)
    ans2 = follow_cycles(part2_starts, instructions, nodes)
    print(ans2)


if __name__ == '__main__':
    main()
