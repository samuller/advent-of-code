#!/usr/bin/env python3
import fileinput

import sys; sys.path.append("../..")
from lib import *


def main():
    lines = [line.strip() for line in fileinput.input()]
    elves = []
    for elf in grouped(lines):
        total = sum([int(cal) for cal in elf])
        elves.append(total)
    elves = sorted(elves)
    print(elves[-1])
    print(sum(elves[-3:]))


if __name__ == '__main__':
    main()
