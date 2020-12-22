#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("..")
from lib import *


def calc_score(deck):
	return sum([(1+i)*c for i,c in enumerate(deck)])


def prepend(deck, cards):
	tmp = deck
	deck = cards
	deck.extend(tmp)
	return deck


def play_game(p1, p2):
	rounds = 0
	# Do you need history from previous recursions?
	history_p1 = []
	history_p2 = []
	while len(p1) != 0 and len(p2) != 0:
		if p1 in history_p1 and p2 in history_p2 \
			and history_p1.index(p1) == history_p2.index(p2):
			print('P1 wins by base case!')
			return p1, []
		history_p1.append(list(p1))
		history_p2.append(list(p2))
		c1 = p1.pop()
		c2 = p2.pop()
		if c1 <= len(p1) and c2 <= len(p2):
			rec_p1, rec_p2 = play_game(list(p1[-c1:]), list(p2[-c2:]))
			if calc_score(rec_p1) > calc_score(rec_p2):
				p1 = prepend(p1, [c2,c1])
			else:
				p2 = prepend(p2, [c1,c2])
		elif c1 > c2:
			p1 = prepend(p1, [c2,c1])
			# tmp = p1
			# p1 = [c2,c1]
			# p1.extend(tmp)
		else:
			p2 = prepend(p2, [c1,c2])
			# tmp = p2
			# p2 = [c1,c2]
			# p2.extend(tmp)
		rounds += 1
		# print(p1, p2)
	print('Ended after {} rounds'.format(rounds))
	return p1, p2


# 33590 @ 7:27
# Part 2: forgot to change return value for base case, run very slow
def main():
	lines = [line.strip() for line in fileinput.input()]
	print('Lines: {}'.format(len(lines)))

	decks = grouped(lines)
	p1 = list(reversed([int(c) for c in next(decks)[1:]]))
	p2 = list(reversed([int(c) for c in next(decks)[1:]]))
	print(p1)
	print(p2)

	p1, p2 = play_game(p1, p2)

	print("Player 1's deck: " + str(p1))
	print("Player 2's deck: " + str(p2))
	
	print("Player 1's Score:", sum([(1+i)*c for i,c in enumerate(p1)]))
	print("Player 2's Score:", sum([(1+i)*c for i,c in enumerate(p2)]))


if __name__ == '__main__':
	main()
