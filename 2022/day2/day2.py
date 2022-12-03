#!/usr/bin/env python3
import fileinput
from collections import Counter

import sys; sys.path.append("..")
from lib import *


# CHOICE:
ROCK = 0
PAPER = 1
SCISSORS = 2
# Wins it <- choice -> Loses against it
TIER_LIST = [ROCK, PAPER, SCISSORS, ROCK]

WIN_TIER_LIST = [
    # (win, lose)
    (ROCK, SCISSORS),
    (PAPER, ROCK),
    (SCISSORS, PAPER)
]

# RESULT:
LOSE = 0
DRAW = 1
WIN = 2

SCORE_RESULT = {
    LOSE: 0,
    DRAW: 3,
    WIN: 6
}


def get_choice_for_result(opp, result):
    if result == DRAW:
        return opp
    if result == WIN:
        # Find match we want, return only value from list ([0]), but only the other side of match-up ([1]).
        return [match for match in WIN_TIER_LIST if match[0] == opp][0][1]
    if result == LOSE:
        return [match for match in WIN_TIER_LIST if match[1] == opp][0][0]
    assert False


def calc_result(opp, me):
    if opp == me:
        return DRAW
    if (me, opp) in WIN_TIER_LIST:
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
        me2 = get_choice_for_result(opp, unk)

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
