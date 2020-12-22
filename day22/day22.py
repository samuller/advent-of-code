#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("..")
from lib import *
from collections import deque
from copy import copy
from itertools import islice


def calc_score(deck):
	return sum([(len(deck)-i)*c for i,c in enumerate(deck)])


def pre_extend(deck, cards):
	"""Was called prepend(), but actually extends since cards is a list."""
	tmp = deck
	deck = cards
	deck.extend(tmp)
	return deck


def play_game(p1, p2):
	rounds = 0
	# Do you need history from previous recursions? No, decks have changed
	history = set()
	while len(p1) != 0 and len(p2) != 0:
		if (tuple(p1), tuple(p2)) in history:
			print('P1 wins by base case!')
			return p1, []
		history.add((tuple(p1), tuple(p2)))
		c1 = p1.popleft()
		c2 = p2.popleft()
		if c1 <= len(p1) and c2 <= len(p2):
			rec_p1, rec_p2 = play_game(deque(islice(p1,0,c1)), deque(islice(p2,0,c2)))	
			if calc_score(rec_p1) > calc_score(rec_p2):
				p1.extend([c1,c2])
			else:
				p2.extend([c2,c1])
		elif c1 > c2:
			p1.extend([c1,c2])
		else:
			p2.extend([c2,c1])
		rounds += 1
		# print(p1, p2)
	print('Ended after {} rounds'.format(rounds))
	return p1, p2


# 33590 @ 7:27
# Part 2: forgot to change return value for base case, runs very slow (2.5 minutes!)
# Might be slow prepend to list by creating new one when adding cards to deck?
# We did this because we reversed ours lists for pop() to work.
# - Using deque() initially turned out slower, likely because of the need to
#   often needed convert it to a list (which copies it) and back, to e.g. slice
#   it or hash it
# Turns out, speed was mainly due to history being a list and searching throught it
# continuously -> set() made it near instant (5s)
def main():
	lines = [line.strip() for line in fileinput.input()]
	print('Lines: {}'.format(len(lines)))

	decks = grouped(lines)
	p1 = deque([int(c) for c in next(decks)[1:]])
	p2 = deque([int(c) for c in next(decks)[1:]])
	print(p1)
	print(p2)

	p1, p2 = play_game(p1, p2)

	print("Player 1's deck: " + str(p1))
	print("Player 2's deck: " + str(p2))
	
	print("Player 1's Score:", calc_score(p1))
	print("Player 2's Score:", calc_score(p2))


if __name__ == '__main__':
	main()
