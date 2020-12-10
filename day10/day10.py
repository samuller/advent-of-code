#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("..")
from lib import *
import numpy as np


def can_connect(main, others):
	valid = []
	idxs = []
	for idx, other in enumerate(others):
		if 0 < (other - main) <= 3: #in [1, 3]:
			valid.append(other)
			idxs.append(idx)
	return valid, idxs


def find_max_utilization_arrangement(adapters, debug=False):
	adapters = list(adapters)
	curr_adapter = adapters[0]
	adapters.remove(curr_adapter)
	chosen_order = []
	diffs = []
	while len(adapters) > 0:
		found, _ = can_connect(curr_adapter, adapters)
		if debug:
			print(found)
		chosen = min(found)
		diffs.append(chosen - curr_adapter)
		adapters.remove(chosen)
		curr_adapter = chosen
		chosen_order.append(chosen)
	return chosen_order, diffs


# _13 to _111113 (as 'a' to 'abcde'):
# a => a					(has to end in a) 1
# ab => b, ab				(has to end in b) 2
# abc => c, ac, bc, abc		(has to end in c) 4
# abcd => ad,bd,cd, abd,acd,bcd, abcd (not d)
# 							(has to end in d, and contain at least one of abc) 7
# abcde => be,ce,de, abe,ace,ade,bce,bde,cde, bcde,acde,abde,abce, abcde (not ae, de)
# 							(has to end in e, and contain at least one of bcd... or ad) 13
# 							at least one of bc... or ad / at least one of bcd... but not only d!
# TODO: consider these cases if their were diffs of 2
#

memoization = {}
def dynamic_programming(adapters, start_idx=0):
	if start_idx == len(adapters)-1:
		return 1
	if start_idx in memoization:
		return memoization[start_idx]
	count = 0
	for idx in range(start_idx+1, len(adapters)):
		if (adapters[idx] - adapters[start_idx]) <= 3:
			count += dynamic_programming(adapters, idx)
	memoization[start_idx] = count
	return count


# Part1: misunderstood lower as I was thinking in other direction (not adapter-to-source)
# Part2: wasn't looking at diffs. still unsure why no 2's appear.
#        first considered groups with sum greater than 3, before realising it's actually
#        the length of one sequences that needs to be considered (for possibilities).
#        variable length variations.
if __name__ == '__main__':
	lines = [line.strip() for line in fileinput.input('input.txt')]
	test1 = """16
10
15
5
1
11
7
19
6
12
4"""
	test2 = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""
	# lines = test2.split('\n')
	print('Lines: {}'.format(len(lines)))

	lines = sorted([int(l) for l in lines])
	lines = [0] + lines  # include charging outlet
	lines.append(3 + max(lines))  # add built-in adapter
	# print(lines)

	# # print(find_recursive(list(range(1,7))))
	# # exit()
	# # PART 2Y - brute force smalls
	# for i in range(2, 10):
	# 	whole = list(range(1,i))
	# 	# Adding this value doesn't change the result, but makes
	# 	# clear that the result is applicable to subsets of the problem
	# 	# i.e. sequences with differences of 1 followed by a difference of 3
	# 	# whole.append(whole[-1]+3)
	# 	# print(whole)
	# 	print(len(whole), '=', find_recursive(whole))

	# Part 1

	chosen_order, diffs = find_max_utilization_arrangement(lines)
	print(chosen_order)
	print(diffs)
	ones = len([l for l in diffs if l == 1])
	threes = len([l for l in diffs if l == 3])
	print(ones, threes, '=', ones * threes)
	
	# Part 2
	possible_routes = dynamic_programming(lines)
	print(possible_routes)