#!/usr/bin/env python3
import fileinput
from collections import Counter

import sys; sys.path.append("..")
from lib import *


# SCORE_RESULT = {0: 0, 1: 3, 2: 6}


def me_win_rps(me, opp):
    opp, me = ord(opp)-ord('A'), ord(me)-ord('X')
    if opp == me:
        return False
    # 0 > 2, 1 > 0, 2 > 1
    if (me, opp) in [(0, 2), (1, 0), (2, 1)]:
        return True
    return False


def get_rps_to_match(opp, action):
    opp, action = ord(opp)-ord('A'), ord(action)-ord('X')
    # Draw
    if action == 1:
        return opp
    # Win
    if action == 2:
        return {2: 0, 0: 1, 1: 2}[opp]
    # Lose
    return {0: 2, 1: 0, 2: 1}[opp]


def main():
    lines = [line.strip() for line in fileinput.input()]
    # rock, paper, sciss
    # 0, 3, 6
    score = {'A': 1, 'B': 2, 'C': 3, 'X': 1, 'Y': 2, 'Z': 3}

    my_score = 0
    for game in lines:
        opp, me = game.split()
        print(game, opp, me)
        action = me
        me = chr(get_rps_to_match(opp, action) + ord('X'))

        my_score += score[me]
        if me_win_rps(me, opp):
            my_score += 6
        opp, me = ord(opp)-ord('A'), ord(me)-ord('X')
        if opp == me:
            my_score += 3
        print(my_score)
    print(my_score)

if __name__ == '__main__':
    print(me_win_rps('A', 'X'))
    main()
