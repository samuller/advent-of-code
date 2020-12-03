#!/usr/bin/env python
from functools import reduce

class Classy:
	def __init__(self):
		pass

def print_map(input):
	for line in input:
		print(line)
	print()

def set_char(stringy, pos, charry):
	list1 = list(stringy)
	list1[pos] = charry
	return ''.join(list1)

def run_slope(mappy, next_pos, debug=False):
	# We use copy in case we want to change map for debugging
	mappy = mappy.copy()
	trees_found = 0
	curr_pos = {'row': 0, 'col': 0}
	while curr_pos['row'] < len(mappy):
		# Move
		curr_pos['row'] += next_pos['row']
		if curr_pos['row'] >= len(mappy):
			break
		assert(len(mappy[curr_pos['row']]) == 31)

		curr_pos['col'] += next_pos['col']
		if curr_pos['col'] >= len(mappy[curr_pos['row']]):
			curr_pos['col'] -= len(mappy[curr_pos['row']])

		# Count
		if mappy[curr_pos['row']][curr_pos['col']] == '#':
			trees_found += 1

		if debug:
			mappy[curr_pos['row']] = set_char(mappy[curr_pos['row']], curr_pos['col'], 'O')
			# Show
			print(curr_pos)
			print(mappy[curr_pos['row']][curr_pos['col']])
			print_map(mappy)
	return curr_pos, trees_found

def prod(iterable):
	# operator.mul
    return reduce(lambda a,b,: a*b, iterable, 1)

if __name__ == '__main__':
	input_file = open('input.txt','r')
	mappy = [line.strip() for line in input_file.readlines()]
	print('Lines: {}'.format(len(mappy)))
	print('Width: {}'.format(len(mappy[0])))

	# Opposite order of question (e.g. 2nd is right 3, down 1)
	slopes = [
		{'row': 1, 'col': 1},
		{'row': 1, 'col': 3},
		{'row': 1, 'col': 5},
		{'row': 1, 'col': 7},
		{'row': 2, 'col': 1},
	]

	all_found = []
	for next_pos in slopes:
		print(next_pos)
		curr_pos, trees_found = run_slope(mappy, next_pos)
		print(curr_pos)
		print(trees_found)
		all_found.append(trees_found)
	print(all_found)
	print(prod(all_found))
