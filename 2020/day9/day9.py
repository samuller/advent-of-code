#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("..")
from lib import *
import itertools


def find_sum_of_portion(listy, sum_value):
	"""Find a contiguous set of at least two numbers in the list
	that sum to the given value.
	"""
	found_portion = False
	min_len = 2
	for start in range(0, len(lines) - min_len):
		# Range needs to go to len + 1 since we'll be using it as end of slice
		for end in range(start + min_len, len(lines)+1):
			portion = lines[start:end]
			# print(len(portion), start, end)
			# print(portion)
			if sum(portion) == num:
				return portion, start, end


# Part 1: didn't realise preamble moves
# Part 2: thought sum was in preamble
if __name__ == '__main__':
	# Test data
	pre = 5
	lines = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""
	lines = lines.split('\n')

	pre = 25
	lines = [line.strip() for line in fileinput.input('input.txt')]
	lines = [int(l) for l in lines]
	print('Lines: {}'.format(len(lines)))

	# print(lines)
	for idx in range(pre, len(lines)):
		preamble = [l for l in lines[idx - pre:idx]]
		# print(preamble)
		num = lines[idx]
		matches = False
		for (m, n) in itertools.combinations(preamble, 2):
			# print(m, n)
			assert m != n
			if m + n == num:
				matches = True
				# print(m, '+', n, '=', num)
				break
		if not matches:
			print(num)
			portion, start_idx, end_idx = find_sum_of_portion(lines, num)
			print(portion)
			print(min(portion), '+', max(portion), '=',  min(portion) + max(portion))
			break
