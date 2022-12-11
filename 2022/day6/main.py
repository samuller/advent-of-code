#!/usr/bin/env python3
import fileinput
from collections import Counter

import sys; sys.path.append("../..")
from lib import *


def read_packet(data, size):
    """Find first X (size) distinct characters in a row to indicate the start of a packet or message."""
    for idx in range(0, len(data)):
        packet = data[idx:idx + size]
        if len(set(packet)) == size:
            return idx, packet
    return None


def main():
    lines = [line.replace("\n", "") for line in fileinput.input()]
    # print(lines)

    for data in lines:
        pos, _ = read_packet(data, 4)
        print(pos + 4)
        pos, _ = read_packet(data, 14)
        print(pos + 14)


if __name__ == '__main__':
    main()
