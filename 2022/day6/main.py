#!/usr/bin/env python3
import fileinput
from collections import Counter

import sys; sys.path.append("../..")
from lib import *


def main():
    lines = [line.replace("\n", "") for line in fileinput.input()]
    print(lines)
    for line in lines:
        for idx in range(0, len(line)):
            packet = line[idx:idx+14]
            if len(set(packet)) == 14:
                print(packet)
                print(idx+14)
                break


if __name__ == '__main__':
    main()
