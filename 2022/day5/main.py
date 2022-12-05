#!/usr/bin/env python3
import fileinput
from collections import Counter

import sys; sys.path.append("../..")
from lib import *


# Delays: strip(), wrong ordering of loops, numbers below stacks, last column not being 4 wide
def main():
    # Can't strip as white space has meaning of empty stack
    lines = [line.replace("\n", "") for line in fileinput.input()]
    groups = grouped(lines)

    lines_stacks = next(groups)
    counts = [int(n) for n in lines_stacks[-1].split()]
    assert counts == list(range(1, 1+counts[-1]))
    # Throw away numbers
    lines_stacks = lines_stacks[0:-1]

    stacks = []*counts[-1]
    for i in range(0, len(lines_stacks[0]), 4):
        stack = []
        for line in lines_stacks:   
            crate = line[i:i+4]
            # print(f"_{crate}_[{i}:{i+4}]")
            crate = crate.strip()
            if len(crate) == 0:
                continue
            assert crate[0] == '[' and crate[2] == ']' # and crate[3] == ' '
            stack.append(crate[1])
        # Put top at the right
        stack.reverse()
        stacks.append(stack)
    # print(stacks)

    line_cmds = next(groups)
    # print(line_cmds)
    part1_stacks = stacks
    # Make copy
    part2_stacks = [list(stack) for stack in part1_stacks]
    for cmd in line_cmds:
        acts = cmd.strip().split()
        count = int(acts[1])
        from_id = int(acts[3]) - 1
        to_id = int(acts[5]) - 1
        # print(cmd)
        # print(count, from_id, to_id)
        # print(part1_stacks)

        # Part 1 - started at 7:23 (time to write parsing code...)
        for _ in range(count):
            crate = part1_stacks[from_id].pop()
            part1_stacks[to_id].append(crate)
        # Part 2
        move_stack = part2_stacks[from_id][-count:]
        part2_stacks[from_id] = part2_stacks[from_id][:-count]
        part2_stacks[to_id].extend(move_stack)
    # 7:26
    print("".join([stack[-1] for stack in part1_stacks]))
    # 7:29
    print("".join([stack[-1] for stack in part2_stacks]))



if __name__ == '__main__':
    main()
