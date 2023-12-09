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
    print(f'Lines: {len(lines)}')

    ans1 = 0
    for line in lines:
        nums = [int(n) for n in line.split(' ')]
        print(nums)
        diff = []
        steps = 0
        prev = nums
        lasts = [nums[-1]]
        while len(set(prev)) != 1:
            for idx in range(len(prev) - 1):
                diff.append(prev[idx+1] - prev[idx])
            # print(" " * (steps + 1), diff)
            unique = set(diff)
            steps += 1
            if len(unique) == 1:
                print(steps)
            # if steps == 5:
            #     exit()
            prev = diff
            diff = []
            lasts.append(prev[-1])
        print(lasts, sum(lasts))
        ans1 += sum(lasts)
    print(ans1)

if __name__ == '__main__':
    main()
