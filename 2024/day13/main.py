#!/usr/bin/env python3
from collections import namedtuple
import fileinput
import sys; sys.path.append("../..")
from lib import *


class Classy:
    def __init__(self):
        pass


def function(input):
    return False


def main():
    lines = [line.strip() for line in fileinput.input()]
    Machine = namedtuple('Machine', ['a_jumps', 'b_jumps', 'prize_loc'])
    machines = []
    for group in grouped(lines):
        assert group[0].split(': ')[0] == 'Button A'
        assert group[1].split(': ')[0] == 'Button B'
        assert group[2].split(': ')[0] == 'Prize'
        a_jumps = [int(s[1:]) for s in group[0].split(': ')[1].split(', ')]
        b_jumps = [int(s[1:]) for s in group[1].split(': ')[1].split(', ')]
        prize_loc =  [int(s[2:]) for s in group[2].split(': ')[1].split(', ')]
        print(a_jumps, b_jumps, prize_loc)
        machines.append(Machine(a_jumps=a_jumps, b_jumps=b_jumps, prize_loc=prize_loc))

    cost_a = 3
    cost_b = 1
    p1 = 0
    for machine in machines:
        lowest_cost = None
        lowest_cost_jumps = None
        a_jumps, b_jumps, prize_loc = machine
        for press_a in range(100):
            for press_b in range(100):
                if prize_loc[0] == a_jumps[0]*press_a + b_jumps[0]*press_b and \
                    prize_loc[1] == a_jumps[1]*press_a + b_jumps[1]*press_b:
                    cost = press_a*cost_a + press_b*cost_b
                    if lowest_cost is None or cost < lowest_cost:
                        lowest_cost = cost
                        lowest_cost_jumps = (press_a, press_b)
        print(lowest_cost, lowest_cost_jumps)
        if lowest_cost is not None:
            p1 += lowest_cost
    print(p1)


if __name__ == '__main__':
    main()
