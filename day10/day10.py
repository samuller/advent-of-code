#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("..")
from lib import *
import numpy as np


def find_max_utilization_arrangement(adapters, debug=False):
	assert adapters == sorted(adapters)
	adapters = np.array(adapters)
	diffs = adapters[1:] - adapters[:-1]
	# If we can assume that no differences exceed the max, then the whole list
	# can be used/utilized in the maximum arrangement
	assert max(diffs) == 3
	return adapters, diffs


#
# Analyze possible configurations/arrangements
#
# # print(dynamic_programming(list(range(1,7))))
# # exit()
# # PART 2Y - brute force smalls
# for i in range(2, 10):
# 	whole = list(range(1,i))
# 	# Adding this value doesn't change the result, but makes
# 	# clear that the result is applicable to subsets of the problem
# 	# i.e. sequences with differences of 1 followed by a difference of 3
# 	whole.append(whole[-1]+3)
# 	# print(whole)
# 	memoization = {}
# 	print(len(whole), '=', dynamic_programming(whole))
# exit()
#
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
# Consider dynamic programming whenever there are combinations with different lengths?
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
	print(lines)

	# Part 1
	chosen_order, diffs = find_max_utilization_arrangement(lines)
	print(chosen_order)
	print(diffs)
	ones = np.count_nonzero(diffs == 1)
	threes = np.count_nonzero(diffs == 3)
	print(ones, threes, '=', ones * threes)
	
	# Part 2
	possible_routes = dynamic_programming(lines)
	print(possible_routes)
