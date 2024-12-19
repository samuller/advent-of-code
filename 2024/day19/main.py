#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("../..")
from lib import *


class Classy:
    def __init__(self):
        pass


def function(input):
    return False


# 7:11 - 228 wrong attempt #1
# 7:25 right attempt #2
def main():
    lines = [line.strip() for line in fileinput.input()]
    available = list(grouped(lines))[0][0].split(", ")
    wanted = list(grouped(lines))[1]
    p1 = 0
    for want in wanted:
        # Attempt #2
        attempts = [want]
        found = False
        while len(attempts) > 0:
            # print(attempts)
            attempt = attempts.pop()
            possibilities = []
            for towel in available:
                if attempt.startswith(towel):
                    possibilities.append(towel)
            for poss in possibilities:
                attempt = attempt[len(poss):]
                if len(attempt) == 0:
                    found = True
                attempts.append(attempt)
            if found:
                break
        if found:
            p1 += 1
        else:
            print(want)
        # Attempt #1
        # attempt = want
        # while True:
        #     longest_possible = None
        #     possibilities = []
        #     for towel in available:
        #         if attempt.startswith(towel):
        #             possibilities.append(towel)
        #     possibilities.sort()
        #     if len(possibilities) == 0 or len(attempt) == 0:
        #         if longest_possible is None and len(attempt) != 0:
        #             print(want, attempt)
        #         break
        #     # print(want, longest_possible)
        #     attempt = attempt[len(possibilities[0]):]
        # if len(attempt) == 0:
        #     # print(want)
        #     p1 += 1
    print(p1)


if __name__ == '__main__':
    main()
