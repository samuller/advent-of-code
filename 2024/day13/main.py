#!/usr/bin/env python3
from collections import namedtuple
import fileinput
import sys; sys.path.append("../..")
from lib import *


def calc_jumps(machines):
    cost_a = 3
    cost_b = 1
    cost = 0
    # Brute force
    # for machine in machines:
    #     lowest_cost = None
    #     lowest_cost_jumps = None
    #     a_jumps, b_jumps, prize_loc = machine
    #     for press_a in range(100):
    #         for press_b in range(100):
    #             x_loc = a_jumps[0]*press_a + b_jumps[0]*press_b
    #             y_loc = a_jumps[1]*press_a + b_jumps[1]*press_b
    #             # print(x_loc, y_loc)
    #             if prize_loc == (x_loc, y_loc):
    #                 cost = press_a*cost_a + press_b*cost_b
    #                 # This should only happen once... (or never)
    #                 if lowest_cost is None or cost < lowest_cost:
    #                     lowest_cost = cost
    #                     lowest_cost_jumps = (press_a, press_b)
    #     # print(lowest_cost, lowest_cost_jumps)
    #     if lowest_cost is not None:
    #         cost += lowest_cost
    for machine in machines:
        a_jumps, b_jumps, prize_loc = machine
        # Math
        # # print(start_a, start_b)
        # # presses = a,b / jumps = (x_a, y_a), (x_b, y_b) / prize_loc = (x,y)
        # # f_1: x = a*x_a + b*x_b
        # # f_2: y = a*y_a + b*y_b
        # # ???: a = ?, b = ?
        # # x = a*x_a + b*x_b
        # # f_3: a = (x - b*x_b)/x_a
        # # place into f_2
        # # y = (x - b*x_b)/x_a * y_a + b*y_b
        # # y = x*y_a/x_a - b*x_b*y_a/x_a + b*y_b
        # # y = x*y_a/x_a - b*(x_b*y_a/x_a + y_b)
        # ### b = (y - x*y_a/x_a)/(x_b*y_a/x_a + y_b)
        # ## b = -(y - x*y_a/x_a)/(x_b*y_a/x_a + y_b)
        # # b = (x*y_a/x_a - y)/(x_b*y_a/x_a + y_b)
        # # place into f_3
        # # a = x/x_a - (y - x*y_a/x_a)/(x_by_a/x_a + y_b)*x_b/x_a
        # ### press_b = (prize_loc[1] - prize_loc[0]*a_jumps[1]/a_jumps[0])/(b_jumps[0]*a_jumps[1]/a_jumps[0] + b_jumps[1])
        # press_b = (prize_loc[0]*a_jumps[1]/a_jumps[0] - prize_loc[1])/(b_jumps[0]*a_jumps[1]/a_jumps[0] + b_jumps[1])
        # press_a = (prize_loc[0] - press_b*b_jumps[0])/a_jumps[0]
        # # y = a*y_a + b*y_b
        # #   = (x - b*x_b)/x_a * y_a + (x*y_a/x_a - y)/(x_b*y_a/x_a + y_b) * y_b
        # #   = x*y_a/x_a - b*x_b*y_a/x_a + x*y_b*y_b/(x_a*(x_b*y_a/x_a + y_b)) - y*y_b/(x_b*y_a/x_a + y_b)
        # #   = x*y_a/x_a - b*x_b*y_a/x_a + x*y_b*y_b/(x_a*x_b*y_a/x_a + x_a*y_b) - y*y_b/(x_b*y_a/x_a + y_b)
        # # y*(1 + y_b/(x_b*y_a/x_a + y_b)) = x*y_a/x_a - b*x_b*y_a/x_a + x*y_b*y_b/(x_a*x_b*y_a/x_a + x_a*y_b)
        # # y = (x*y_a/x_a - b*x_b*y_a/x_a + x*y_b*y_b/(x_a*x_b*y_a/x_a + x_a*y_b))/(1 + y_b/(x_b*y_a/x_a + y_b))
        # print(press_a, press_b)
        # print(prize_loc, a_jumps[0]*press_a + b_jumps[0]*press_b, a_jumps[1]*press_a + b_jumps[1]*press_b)
        # # x, y = prize_loc
        # # x_a, y_a = a_jumps
        # # x_b, y_b = b_jumps
        # # b = -(y - x*y_a/x_a)/(x_b*y_a/x_a + y_b)
        # # a = (x - b*x_b)/x_a
        # # print(a, b)

        # newton optimization?
        # start_a, start_b = prize_loc[0]//b_jumps[0], prize_loc[1]//b_jumps[1]

        # okay, now integer-only math..
        # a > 0 and b > 0

        # 8400 = 94a + 22b
        # 5400 = 34a + 67b
        # a = (8400-22b) / 94
        # 5400 = 34*(8400-22b)/94 + 67b
        # 5400 = 34*8400/94 - 34*22b/94 + 67b
        # 5400 - 34*8400/94 = b(-(34*22/94) + 67)
        # b = (5400 - 34*8400/94) / (-(34*22/94) + 67)
        # b = 40
        # a = 80
        press_b = (prize_loc[1] - a_jumps[1]*prize_loc[0]/a_jumps[0]) / (-(a_jumps[1]*b_jumps[0]/a_jumps[0]) + b_jumps[1])
        press_a = (prize_loc[0] - press_b*b_jumps[0])/a_jumps[0]
        press_a = round(press_a)
        press_b = round(press_b)
        # print(press_a, press_b)
        # print(prize_loc, a_jumps[0]*press_a + b_jumps[0]*press_b, a_jumps[1]*press_a + b_jumps[1]*press_b)
        x_loc = a_jumps[0]*press_a + b_jumps[0]*press_b
        y_loc = a_jumps[1]*press_a + b_jumps[1]*press_b
        # if prize_loc == (round(x_loc), round(y_loc)) and (press_a - round(press_a)) < 1e-6 and (press_b - round(press_b)) < 1e-6:
        #     p2 += round(press_a)*cost_a + round(press_b)*cost_b
        if prize_loc == (x_loc, y_loc):
            # print(prize_loc, a_jumps[0]*press_a + b_jumps[0]*press_b, a_jumps[1]*press_a + b_jumps[1]*press_b)
            cost += press_a*cost_a + press_b*cost_b
    return cost


def main():
    lines = [line.strip() for line in fileinput.input()]
    Machine = namedtuple('Machine', ['a_jumps', 'b_jumps', 'prize_loc'])
    machines = []
    machines_p2 = []
    for group in grouped(lines):
        assert group[0].split(': ')[0] == 'Button A'
        assert group[1].split(': ')[0] == 'Button B'
        assert group[2].split(': ')[0] == 'Prize'
        a_jumps = tuple([int(s[1:]) for s in group[0].split(': ')[1].split(', ')])
        b_jumps = tuple([int(s[1:]) for s in group[1].split(': ')[1].split(', ')])
        prize_loc = tuple([int(s[2:]) for s in group[2].split(': ')[1].split(', ')])
        machines.append(Machine(a_jumps=a_jumps, b_jumps=b_jumps, prize_loc=prize_loc))
        # Part 2
        prize_loc = (10000000000000+prize_loc[0], 10000000000000+prize_loc[1])
        machines_p2.append(Machine(a_jumps=a_jumps, b_jumps=b_jumps, prize_loc=prize_loc))

    p1 = calc_jumps(machines)
    p2 = calc_jumps(machines_p2)
    print(p1)
    print(p2)

if __name__ == '__main__':
    main()
