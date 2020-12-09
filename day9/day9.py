#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("..")
from lib import *
import itertools

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
			# print(preamble)
			found_portion = False
			for start in range(0, len(lines)-2):
				for end in range(start + 2, len(lines)+1):
					portion = lines[start:end]
					# print(len(portion), start, end)
					# print(portion)
					if sum(portion) == num:
						print(portion)
						print(min(portion), '+', max(portion), '=',  min(portion) + max(portion))
						break
				if found_portion:
					break
			break
			
			

