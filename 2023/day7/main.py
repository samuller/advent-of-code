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
# Part 2
card_ranks = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
card_ranks.reverse()
hand_ranks = []

def value_of_hand(hand):
    assert len(hand) == 5
    for c in hand:
        assert c in card_ranks
    per_card_value = tuple([card_ranks.index(c) for c in hand])
    unique = Counter(hand)
    # Part 2
    # TODO: full house
    if 'J' in hand:
        new_hand = hand
        other_cards = [c for c in hand if c != 'J']
        # sort by value
        other_cards.sort(key=lambda val: card_ranks.index(val))
        count_others = Counter(other_cards)
        # 5x Js are just lowest pentuplets
        if unique['J'] == 4:
            assert len(count_others) == 1
            other_card = other_cards[0]
            # highest other card - pents
            new_hand = other_card*5
        elif unique['J'] == 3:
            assert len(count_others) in [1, 2]
            # highest other card - quads
            new_hand = hand.replace('J', other_cards[-1])
        elif unique['J'] == 2:
            assert len(count_others) in [1, 2, 3]
            if len(count_others) == 3:
                # highest other card - trips
                new_hand = hand.replace('J', other_cards[-1])
            elif len(count_others) == 2:
                # most other cards - quads
                joker_card = Counter(other_cards).most_common()[0][0]
                new_hand = hand.replace('J', joker_card)
            elif len(count_others) == 1:
                # any - pents
                new_hand = hand.replace('J', other_cards[0])
        elif unique['J'] == 1:
            assert len(count_others) in [1, 2, 3, 4]
            if len(count_others) == 4:
                # highest other card - pair
                new_hand = hand.replace('J', other_cards[-1])
            if len(count_others) == 3:
                # most other cards - trips
                # (or highest other card?)
                joker_card = Counter(other_cards).most_common()[0][0]
                new_hand = hand.replace('J', joker_card)
            elif len(count_others) == 2:
                # most other cards - quads or full house!!!
                commons = count_others.most_common()
                # 3/1 quads
                if commons[0][1] == 3:
                    assert commons[1][1] == 1
                    # most other cards
                    joker_card = Counter(other_cards).most_common()[0][0]
                    new_hand = hand.replace('J', joker_card)
                # 2/2 full house
                elif commons[1][1] == 2:
                    assert commons[0][1] == 2
                    # highest other card
                    new_hand = hand.replace('J', other_cards[-1])
                # quads?
                else:
                    assert False
                    # joker_card = commons[0][0]
                    # new_hand = hand.replace('J', joker_card)
            elif len(count_others) == 1:
                # any - pents
                new_hand = hand.replace('J', other_cards[0])
        print(hand, "->", new_hand)
        hand = new_hand
    unique = Counter(hand)
    most = unique.most_common()[0]
    common = unique.most_common()
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


# assert value_of_hand("2345A") == (1, 12)  #  "Bug"
# Part 1
# assert value_of_hand("A2345") == (1, 12, 0, 1, 2, 3), value_of_hand("A2345")
# Part 2
assert value_of_hand("A2345") == (1, 12, 1, 2, 3, 4), value_of_hand("A2345")


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
        # print(hand, value_of_hand(hand))
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
