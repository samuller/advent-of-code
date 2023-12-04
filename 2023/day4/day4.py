#!/usr/bin/env python3
import math
import fileinput
from collections import defaultdict, Counter


def main():
    lines = [line.strip() for line in fileinput.input()]

    ans1 = 0
    cards = Counter() #defaultdict(int)
    for line in lines:
        card, data = line.split(': ')
        id = int(card.split()[1])
        cards[id] += 1
        winners, have = data.split(' | ')
        winners = [int(num) for num in winners.split()]
        have = [int(num) for num in have.split()]
        print(id, winners, have)
        won = []
        for num in winners:
            if num in have:
                won.append(num)
        prize = 0
        if len(won) > 0:
            prize = math.pow(2, len(won)-1)
        # print(won, prize)
        ans1 += prize

        matches = len(won)
        for curr_copy in range(cards[id]):
            for next_copy_idx in range(matches):
                cards[id + 1 + next_copy_idx] += 1
        print(matches, cards)
    print(int(ans1))
    print(cards.total())



if __name__ == '__main__':
    main()
