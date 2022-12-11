#!/usr/bin/env python3
import fileinput
from collections import Counter

import sys; sys.path.append("../..")
from lib import *


def draw_char(X, cycle):
    style = [' ', '█']  # Full block (U+2588)
    # style = ['⬛', '🟦']  # Large squares
    # print("D", cycle, X)
    pos = (cycle%40) - 1
    if pos in [X-1, X, X+1]:  #X in [cycle-1, cycle, cycle+1]:
        return style[1]
    else:
        return style[0]


def check_signal(cycle, X):
    signal_strength = 0
    if cycle == 20 or (cycle-20) % 40 == 0:
        # print(X, cycle)
        signal_strength = X * cycle
    return signal_strength


#part 2 - BJFRHRFU
def main():
    lines = [line.replace("\n", "") for line in fileinput.input()]

    # Closure to reduce repeated code for each cycle
    def do_cycle(after_op=None):
        nonlocal cycle, cmd, X, total_signal, CRT
        if after_op is None:
            after_op = lambda x: None

        CRT.append(draw_char(X, cycle))
        cycle +=1
        # Currently, the only operation occurs after a cycle
        after_op(cmd)
        total_signal += check_signal(cycle, X)

    X = 1
    cycle = 1
    total_signal = 0
    CRT = []
    for line in lines:
        # if len(CRT) > 60:
        #     exit()
        cmd = line.split()
        if cmd[0] == "noop":
            do_cycle()
            continue
        elif cmd[0] == "addx":
            # Operation to perform for this command
            def add(_cmd):
                nonlocal X
                X += int(_cmd[1])

            # Operation takes 2 cycles
            do_cycle()
            do_cycle(after_op=add)
            continue
        else:
            assert False

    # Part 1
    print(total_signal)
    # Part 2
    assert len(CRT) == 40*6
    for r in range(6):
        for c in range(40):
            print(CRT[r*40 + c], end="")
        print()


if __name__ == '__main__':
    main()
