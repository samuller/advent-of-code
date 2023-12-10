#!/usr/bin/env python3
import fileinput
from enum import Enum
from collections import Counter


# 7 Five of a kind, where all five cards have the same label: AAAAA
# 6 Four of a kind, where four cards have the same label and one card has a different label: AA8AA
# 5 Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
# 4 Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
# 3 Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
# 2 One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
# 1 High card, where all cards' labels are distinct: 234
# 0
class HandTypes(Enum):
    # Pentuplet, quintuplet
    FIVE_OF_A_KIND = 7
    # Quads, quadruplet, tetraplet
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    # Triplet
    TRIPS = 4
    TWO_PAIR = 3
    # Couplet
    ONE_PAIR = 2
    # Singlet
    HIGH_CARD = 1


def replace_jokers(hand, card_ranks):
    assert 'J' in hand
    unique = Counter(hand)
    new_hand = hand
    other_cards = [c for c in hand if c != 'J']
    # sort by value
    other_cards.sort(key=lambda val: card_ranks.index(val))
    count_others = Counter(other_cards)

    match unique['J'], len(count_others):
        case 5 , _:
            # 5x Js are just lowest pentuplets
            pass
        case 4 , _:
            assert len(count_others) == 1
            # highest other card - pents
            new_hand = other_cards[0]*5
        case 3, _:
            assert len(count_others) in [1, 2]
            # highest other card - quads
            new_hand = hand.replace('J', other_cards[-1])
        case 2, 3:
            # highest other card - trips
            new_hand = hand.replace('J', other_cards[-1])
        case 2, 2:
            # most other cards - quads
            joker_card = Counter(other_cards).most_common()[0][0]
            new_hand = hand.replace('J', joker_card)
        case 2, 1:
            # any - pents
            new_hand = hand.replace('J', other_cards[0])
        case 2, _:
            assert len(count_others) in [1, 2, 3]
            assert False
        case 1, 4:
            # highest other card - pair
            new_hand = hand.replace('J', other_cards[-1])
        case 1, 3:
            # most other cards - trips
            # (or highest other card?)
            joker_card = Counter(other_cards).most_common()[0][0]
            new_hand = hand.replace('J', joker_card)
        case 1, 2:
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
        case 1, 1:
            # any - pents
            new_hand = hand.replace('J', other_cards[0])
        case 1, _:
            assert len(count_others) in [1, 2, 3, 4]
            assert False

    # print(hand, "->", new_hand)
    return new_hand


def type_of_hand(hand):
    unique = Counter(hand)
    most_common_value, most_common_count = unique.most_common()[0]
    common = unique.most_common()
    match most_common_count, len(unique):
        # pentuplets
        case 5, _:
            assert len(unique) == 1
            assert most_common_value == hand[0]
            # return (7, card_ranks.index(most_common_value))
            return HandTypes.FIVE_OF_A_KIND.value
        # quads
        case 4, _:
            assert len(unique) == 2
            # return (6, card_ranks.index(most_common_value))
            return HandTypes.FOUR_OF_A_KIND.value
        # Full house
        case 3, 2:
            assert common[1][1] == 2
            # return (5, card_ranks.index(most_common_value), card_ranks.index(common[1][0]))
            return HandTypes.FULL_HOUSE.value
        # trips
        case 3, _:
            assert len(unique) in [2, 3]
            # return (4, card_ranks.index(most_common_value))
            return HandTypes.TRIPS.value
        # two pair
        case 2, 3:
            assert common[1][1] == 2
            # value of 2nd pair?
            # return (3, card_ranks.index(most_common_value), card_ranks.index(common[1][0]))
            return HandTypes.TWO_PAIR.value
        # pair
        case _, 4:
            assert most_common_count == 2
            # return (2, card_ranks.index(most_common_value))
            return HandTypes.ONE_PAIR.value
    # high card
    assert len(common) == 5, hand
    # card_values = [card_ranks.index(val) for val in hand]
    # highest_card = max(card_values)
    # type, within_type
    # return (0, highest_card)
    return HandTypes.HIGH_CARD.value


def value_of_hand(hand, card_ranks, jokers=False):
    assert len(hand) == 5
    for c in hand:
        assert c in card_ranks
    per_card_value = tuple([card_ranks.index(c) for c in hand])
    # Part 2
    # TODO: full house
    if jokers and 'J' in hand:
        hand = replace_jokers(hand, card_ranks)
    hand_type = type_of_hand(hand)
    return (hand_type, *per_card_value)


def total_winnings(lines, card_ranks, jokers=False):
    hand_to_value = dict()
    hand_to_bid = dict()
    for line in lines:
        hand, bid = line.split(' ')
        assert len(hand) == 5
        bid = int(bid)
        hand_to_bid[hand] = bid
        hand_to_value[hand] = value_of_hand(hand, card_ranks, jokers)
        # print(hand, value_of_hand(hand))
    # print()
    hand_values = list(hand_to_value.items())
    hand_values.sort(key=lambda val: val[1])
    # print(hand_to_bid)
    # print(hand_values)
    ans1 = 0
    for rank, hand_value in enumerate(hand_values):
        hand, value = hand_value
        bid = hand_to_bid[hand]
        ans1 += (bid * (rank + 1))
    # print(hands_value)
    return ans1


# [7:23] 254142052 [highest card value]
# [7:28] 253677864 [wrong draw ranking]
# [7:35] part1!
def main():
    lines = [line.strip() for line in fileinput.input()]

    card_ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    card_ranks.reverse()
    ans1 = total_winnings(lines, card_ranks, False)
    print(ans1)
    # assert value_of_hand("2345A") == (1, 12)  #  "Bug"
    # Part 1
    assert value_of_hand("A2345", card_ranks) == (1, 12, 0, 1, 2, 3), value_of_hand("A2345", card_ranks)

    # Part 2
    card_ranks = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
    card_ranks.reverse()
    ans2 = total_winnings(lines, card_ranks, True)
    print(ans2)
    # Part 2
    assert value_of_hand("A2345", card_ranks) == (1, 12, 1, 2, 3, 4), value_of_hand("A2345", card_ranks)


if __name__ == '__main__':
    main()
