#!/usr/bin/env python3
import fileinput
from collections import Counter

import sys; sys.path.append("../..")
from lib import *

# def check_cycyle

def draw_char(X, cycle):
    print("D", cycle, X)
    pos = (cycle%40) - 1
    if pos in [X-1, X, X+1]:  #X in [cycle-1, cycle, cycle+1]:
        return '#'
    else:
        return '.' 

#part 2 - BJFRHRFU
def main():
    lines = [line.replace("\n", "") for line in fileinput.input()]

    X = 1
    cycle = 1
    total_signal = 0
    CRT = []
    for line in lines:
        # if len(CRT) > 60:
        #     exit()
        cmd = line.split()
        if cmd[0] == "noop":
            CRT.append(draw_char(X, cycle))
            # print(len(CRT), "".join(CRT))
            cycle += 1
            if cycle == 20 or (cycle-20) % 40 == 0:
                print(X, cycle, cmd)
                total_signal += X * cycle
            continue
        elif cmd[0] == "addx":
            # for cc in range(2):
            CRT.append(draw_char(X, cycle))
            # print(len(CRT), "".join(CRT))
            cycle +=1
            if cycle == 20 or (cycle-20) % 40 == 0:
                print(X, cycle, cmd)
                total_signal += X * cycle

            CRT.append(draw_char(X, cycle))
            # print(len(CRT), "".join(CRT))
            cycle +=1

            amt = int(cmd[1])
            X += amt
            if cycle == 20 or (cycle-20) % 40 == 0:
                print(X, cycle, cmd)
                total_signal += X * cycle
            continue
        else:
            assert False

    print(X)
    print(total_signal)

    assert len(CRT) == 40*6
    for r in range(6):
        for c in range(40):
            print(CRT[r*40 + c], end="")
        print()

# Part 1
# def main():
#     lines = [line.replace("\n", "") for line in fileinput.input()]

#     X = 1
#     cycle = 1
#     total_signal = 0
#     for line in lines:
#         cmd = line.split()
#         if cmd[0] == "noop":
#             cycle += 1
#             if cycle == 20 or (cycle-20) % 40 == 0:
#                 print(X, cycle, cmd)
#                 total_signal += X * cycle
#             continue
#         elif cmd[0] == "addx":
#             # for cc in range(2):
#             cycle +=1
#             if cycle == 20 or (cycle-20) % 40 == 0:
#                 print(X, cycle, cmd)
#                 total_signal += X * cycle
#             cycle +=1

#             amt = int(cmd[1])
#             X += amt
#             if cycle == 20 or (cycle-20) % 40 == 0:
#                 print(X, cycle, cmd)
#                 total_signal += X * cycle
#             continue
#         else:
#             assert False
#     print(X)
#     print(total_signal)


if __name__ == '__main__':
    main()
