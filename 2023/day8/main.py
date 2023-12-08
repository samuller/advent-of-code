#!/usr/bin/env python3
import fileinput
# import sys; sys.path.append("../..")
# from lib import *


class Classy:
    def __init__(self):
        pass


def function(input):
    return False


def main():
    lines = [line.strip() for line in fileinput.input()]

    instructions = lines[0]
    assert lines[1] == ""
    nodes = dict()
    for line in lines[2:]:
        node, neigh = line.split(' = ')
        # Remove brackets
        neigh = neigh[1:-1]
        left, right = neigh.split(", ")
        print(node, left, right)
        nodes[node] = (left, right)
    print(nodes)
    curr = "AAA"
    ans1 = 0
    ins_idx = 0
    while curr != "ZZZ":
        ins = instructions[ins_idx % len(instructions)]
        ins_idx += 1
    # for ins in enuminstructions:
        print("INS", ins)
        if ins == "L":
            curr = nodes[curr][0]
        elif ins == "R":
            curr = nodes[curr][1]
        else:
            assert False, ins
        ans1 += 1
    assert curr == "ZZZ"
    print(ans1)

if __name__ == '__main__':
    main()
