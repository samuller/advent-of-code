#!/usr/bin/env python3
import fileinput
from collections import Counter
# import sys; sys.path.append("../..")
# from lib import *


class Classy:
    def __init__(self):
        pass


# 7 Five of a kind, where all five cards have the same label: AAAAA
# 6 Four of a kind, where four cards have the same label and one card has a different label: AA8AA
# 5 Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
# 4 Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
# 3 Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
# 2 One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
# 1 High card, where all cards' labels are distinct: 234
# 0

card_ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
card_ranks.reverse()
hand_ranks = []

def value_of_hand(hand):
    assert len(hand) == 5
    for c in hand:
        assert c in card_ranks
    unique = Counter(hand)
    most = unique.most_common()[0]
    common = unique.most_common()
    per_card_value = tuple([card_ranks.index(c) for c in hand])
    # pentuplets
    if most[1] == 5:
        assert len(common) == 1
        assert most[0] == hand[0]
        # return (7, card_ranks.index(most[0]))
        return (7, *per_card_value)
    # quads
    if most[1] == 4:
        assert len(common) == 2
        # return (6, card_ranks.index(most[0]))
        return (6, *per_card_value)
    # Full house
    if len(common) == 2 and most[1] == 3 and common[1][1] == 2:
        # return (5, card_ranks.index(most[0]), card_ranks.index(common[1][0]))
        return (5, *per_card_value)
    # trips
    if most[1] == 3:
        assert len(common) in [2, 3]
        # return (4, card_ranks.index(most[0]))
        return (4, *per_card_value)
    # two pair
    if len(common) == 3 and most[1] == 2 and common[1][1] == 2:
        # value of 2nd pair?
        # return (3, card_ranks.index(most[0]), card_ranks.index(common[1][0]))
        return (3, *per_card_value)
    # pair
    if len(common) == 4:
        assert most[1] == 2
        # return (2, card_ranks.index(most[0]))
        return (2, *per_card_value)
    # high card
    assert len(common) == 5
    card_values = [card_ranks.index(val) for val in hand]
    highest_card = max(card_values)
    # type, within_type
    # return (0, highest_card)
    return (1, *per_card_value)


# assert value_of_hand("2345A") == (1, 12)
assert value_of_hand("A2345") == (1, 12, 0, 1, 2, 3), value_of_hand("A2345")


# [7:23] 254142052 [highest card value]
# [7:28] 253677864 [wrong draw ranking]
# [7:35] part1!
def main():
    lines = [line.strip() for line in fileinput.input()]

    print(card_ranks)

    hand_to_value = dict()
    hand_to_bid = dict()
    for line in lines:
        hand, bid = line.split(' ')
        assert len(hand) == 5
        bid = int(bid)
        hand_to_bid[hand] = bid
        hand_to_value[hand] = value_of_hand(hand)
        print(hand, value_of_hand(hand))
    print()
    hand_values = list(hand_to_value.items())
    hand_values.sort(key=lambda val: val[1])
    # print(hand_to_bid)
    print(hand_values)
    ans1 = 0
    for rank, hand_value in enumerate(hand_values):
        hand, value = hand_value
        bid = hand_to_bid[hand]
        ans1 += (bid * (rank + 1)) 
    print(ans1)
    # print(hands_value)


if __name__ == '__main__':
    main()
