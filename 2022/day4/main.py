#!/usr/bin/env python3
import fileinput
from collections import Counter

import sys; sys.path.append("../..")
from lib import *


def main():
    lines = [line.strip() for line in fileinput.input()]
    part1 = 0
    part2 = 0
    for line in lines:
        elf1, elf2 = line.split(",")
        elf1 = [int(n) for n in elf1.split("-")]
        elf2 = [int(n) for n in elf2.split("-")]
        # elf1 = list(range())
        print(elf1, elf2)

        within = False
        if elf1[0] >= elf2[0] and elf1[1] <= elf2[1]:
            within = True
        if elf2[0] >= elf1[0] and elf2[1] <= elf1[1]:
            within = True
        if within:
            part1 += 1

        overlap = False
        if elf2[0] <= elf1[0] <= elf2[1] or elf2[0] <= elf1[1] <= elf2[1]:
            overlap = True
        if elf1[0] <= elf2[0] <= elf1[1] or elf1[0] <= elf2[1] <= elf1[1]:
            overlap = True
        if overlap:
            part2 += 1
    print(part1)
    print(part2)

if __name__ == '__main__':
    main()
