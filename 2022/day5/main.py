#!/usr/bin/env python3
import fileinput
from collections import Counter

import sys; sys.path.append("../..")
from lib import *


def main():
    lines = [line.replace("\n", "") for line in fileinput.input()]
    groups = grouped(lines)
    # for group in groups:
    #     print(group)
    # exit()
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
            print(f"_{crate}_[{i}:{i+4}]")
            crate = crate.strip()
            if len(crate) == 0:
                continue
            assert crate[0] == '[' and crate[2] == ']' # and crate[3] == ' '
            stack.append(crate[1])
        # Put top at the right
        stack.reverse()
        stacks.append(stack)
    print(stacks)

    line_cmds = next(groups)
    print(line_cmds)
    for cmd in line_cmds:
        acts = cmd.strip().split()
        count = int(acts[1])
        from_id = int(acts[3]) - 1
        to_id = int(acts[5]) - 1
        print(cmd)
        print(count, from_id, to_id)
        print(stacks)
        # Part 1 - started at 7:23 (after formatting code)
        # for _ in range(count):
        #     crate = stacks[from_id].pop()
        #     stacks[to_id].append(crate)
        # Part 2
        move_stack = stacks[from_id][-count:]
        stacks[from_id] = stacks[from_id][:-count]
        stacks[to_id].extend(move_stack)
    # 7:26 & 7:29
    print("".join([stack[-1] for stack in stacks]))



if __name__ == '__main__':
    main()
