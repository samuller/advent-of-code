#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("..")
from lib import *
import numpy as np


def can_connect(main, others):
	valid = []
	idxs = []
	for idx, other in enumerate(others):
		# print(other - main)
		if 0 < (other - main) <= 3: #in [1, 3]:
			valid.append(other)
			idxs.append(idx)
	return valid, idxs


def find_max_utilization_arrangement(adapters, debug=False):
	adapters = list(adapters)
	curr_adapter = 0
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


# [1, 1, 3, 2, 1, 1, 2, 1, 1, 1, 1, 1] = 
# 3*2*2 = 12
# 567, 57, 67, 7
#
# 2: skip zero or 1st (or 2nd if next allows it?)
# 3: skip zero (skip zero or first), 1st or first 2
#
# 3-1 (diff3): 4 options (123, 23, 3, 13, 1, 2)
# 3-2
# 3-3: 4 options (1, 2, 3, 123, 23, 3, 13, 1, 2)
#
# 3: 7 options: 1,2,3,12,23,13,123
#    3 alternatives (valid endings): 1, 2,12, 3,23,13,123
#    all 7, or 6, or 4
# 2: 3 options: 1,2,12
#    2 alternatives: 1, 2,12
def find_recursive(adapters, start_idx=0, chosen_order=None, route_options=None):
	# Assume sorted
	# adapters = sorted(adapters)

	if chosen_order is None:
		chosen_order = []
	if route_options is None:
		route_options = []

	# if start_idx != 0:
	# 	print(start_idx)
	# 	# return 0
	curr_idx = start_idx
	curr_adapter = adapters[start_idx]
	chosen_order.append(curr_adapter)
	total_routes = 0
	while curr_idx <= len(adapters):
		found, idxs = can_connect(curr_adapter, adapters)
		# print(curr_idx, found, idxs)
		if len(idxs) == 0:
			break
		route_options.append(len(idxs))
		# curr_adapter = min(found)
		# curr_idx = adapters.index(curr_adapter)

		# print(curr_adapter, curr_idx)
		if len(idxs) == 1:
			curr_idx = idxs[0]
			curr_adapter = adapters[curr_idx]
			chosen_order.append(curr_adapter)
		else:
			# Take first route
			curr_idx = idxs[0]
			curr_adapter = adapters[curr_idx]
			# Test alternatives
			for idx in idxs[1:]:
				total_routes += find_recursive(adapters, idx, list(chosen_order), list(route_options))
			chosen_order.append(curr_adapter)
	# print(start_idx, chosen_order, '\n ', route_options)
	# print(start_idx, chosen_order)
	return 1 + total_routes


def count_routes(adapters):
	adapters = np.array(adapters)
	diffs = adapters[1:] - adapters[:-1]
	print(diffs)

	seq_of_ones = 0
	ones = []
	for diff in diffs:
		if diff == 1:
			seq_of_ones += 1
		else:
			ones.append(seq_of_ones)
			seq_of_ones = 0
	ones.append(seq_of_ones)
	# Zeroes occur for each 3,3
	ones = [n for n in ones if n != 0]
	print(ones)

	# +1 to be inclusive, +1 to include ending digit
	vals = [find_recursive(list(range(1,l+1+1))) for l in ones]
	possible_routes = prod(vals)
	return possible_routes


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
	extra_adapter = 3 + max(lines)
	lines.append(extra_adapter)
	# print(lines)

	# # PART 2Y - brute force smalls
	# for i in range(2, 10):
	# 	whole = list(range(1,i))
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
	lines = [0] + lines
	possible_routes = count_routes(lines)
	print(possible_routes)
