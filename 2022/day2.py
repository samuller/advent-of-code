#!/usr/bin/env python3
import fileinput
from collections import Counter

import sys; sys.path.append("..")
from lib import *


# CHOICE:
ROCK = 0
PAPER = 1
SCISSORS = 2

# RESULT:
LOSE = 0
DRAW = 1
WIN = 2

SCORE_RESULT = {
    LOSE: 0,
    DRAW: 3,
    WIN: 6
}


def get_rps_to_match(opp, action):
    if action == DRAW:
        return opp
    if action == WIN:
        return {2: 0, 0: 1, 1: 2}[opp]
    if action == LOSE:
        return {0: 2, 1: 0, 2: 1}[opp]
    assert False


def calc_result(opp, me):
    if opp == me:
        return DRAW
    tier_list = [
        (ROCK, SCISSORS),
        (PAPER, ROCK),
        (SCISSORS, PAPER)
    ]
    if (me, opp) in tier_list:
        return WIN
    return LOSE


def main():
    lines = [line.strip() for line in fileinput.input()]

    part1 = 0
    part2 = 0
    for game in lines:
        opp, unk = game.split()
        # Convert to numeric
        opp, unk = ord(opp) - ord('A'), ord(unk) - ord('X')
        # Part 1 vs part 2
        me1 = unk
        me2 = get_rps_to_match(opp, unk)

        # Choice score
        part1 += (me1 + 1)
        # Result score
        res = calc_result(opp, me1)
        part1 += SCORE_RESULT[res]

        part2 += (me2 + 1)
        res = calc_result(opp, me2)
        part2 += SCORE_RESULT[res]
    print(part1)
    print(part2)


if __name__ == '__main__':
    main()
