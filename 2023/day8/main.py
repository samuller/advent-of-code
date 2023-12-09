#!/usr/bin/env python3
import math
import fileinput
import sys; sys.path.append("../..")
from lib import *

# steps = [13939, 17621, 19199, 15517, 12361, 20777]
# print(steps)
# new_steps = []
# for step in steps:
#     new_steps.append(step // 263)
# print(new_steps)
# print(prod(new_steps) * 263)
# exit()

# 2 3 5
# 2*3*5 = 30
# 6*3*5 = 90 -> 30
# 2*3 * 3 * 5
# 13939, 17621, 19199, 15517, 12361, 20777
# 53 × 263, 67 × 263, 73 × 263, 59 × 263, 79 × 263
# 53, 67, 73, 59, 79
def follow_cycles(starts, instructions, nodes):
    currs = list(starts)
    steps_needed = [0] * len(currs)

    steps = 0
    ins_idx = 0
    # while not all([curr[-1] == "Z" for curr in currs]):
    while any([step == 0 for step in steps_needed]):
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

    # print(currs)
    # print(steps_needed, prod(steps_needed))
    return math.lcm(*steps_needed)


def follow(start, instructions, nodes):
    curr = start
    steps = 0
    ins_idx = 0
    while curr != "ZZZ":
        ins = instructions[ins_idx % len(instructions)]
        ins_idx += 1
        if ins == "L":
            curr = nodes[curr][0]
        elif ins == "R":
            curr = nodes[curr][1]
        else:
            assert False, ins
        steps += 1
    assert curr == "ZZZ"
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
