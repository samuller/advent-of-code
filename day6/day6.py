#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("..")
from lib import prod, Map2D


def grouped(lines):
	"""Separate list of lines into groups of consecutive non-empty lines.
	"""
	group = []
	for line in lines:
		if line == '':
			if len(group) > 0:
				yield group
			group = []
		else:
			group.append(line)
	# Handle final group in case there's no ending separator
	# Alternative is to add separator at the end: lines.append('')
	# but this requires modifying or copying the input
	if len(group) > 0:
		yield group


if __name__ == '__main__':
	test = """
abc

a
b
c

ab
ac

a
a
a
a

b
	"""
	# 6567, 6585 (server @ 7:11, @ 7:14) / 3264 (0729), 3276
	# part 1: miscounted last group because of appending '\n' which wasn't stripped
	#         internet connection... and then missed seeing part 2
	# part 2: missed-counted groups with no matches, missed 1 line long groups
	#         testing took longer because of appending '\n' which wasn't stripped
	lines = [line.strip() for line in fileinput.input(files=['input.txt'])]
	# lines = test.split('\n')
	print('Lines: {}'.format(len(lines)))
	
	total_yes_quests = 0
	total_common_yes_quests = 0
	for group in grouped(lines):
		curr_group = set()
		for line in group:
			curr_group = curr_group.union(set(line))
		total_yes_quests += len(curr_group)

		curr_group_2 = set()
		for idx, line in enumerate(group):
			if idx == 0:
				curr_group_2 = set(line)
			else:
				curr_group_2 = curr_group_2.intersection(set(line))
		total_common_yes_quests += len(curr_group_2)

	print('Total yes questions:', total_yes_quests)
	print('Total common yes questions:', total_common_yes_quests)
