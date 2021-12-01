#!/usr/bin/env python3
import fileinput
import itertools
import sys; sys.path.append("../..")
from lib import *


# bugs:
# 1509 - off by one error on indices
# 1998 - same, on 2nd prev + if offset
def main():
    lines = [int(line.strip()) for line in fileinput.input()]
    print('Lines: {}'.format(len(lines)))

    # Part 1
    count = 0
    prev = lines[0]
    for num in lines:
        if num > prev:
            count += 1
        prev = num
    print(count)

    # Part 2
    count = 0
    prev = lines[0:3]
    for idx, num in enumerate(lines):
        if idx > len(lines) - 3:
            continue
        curr = lines[idx:idx+3]
        if sum(curr) > sum(prev):
            count += 1
        prev = lines[idx:idx+3]
    print(count)


if __name__ == '__main__':
    main()
