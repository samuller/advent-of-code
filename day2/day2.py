#!/usr/bin/env python
from collections import Counter

def password_valid(password, range_str, character):
	assert(len(character) == 1)
	range = range_str.split('-')
	assert(len(range) == 2)
	range = [int(r) for r in range]
	assert(range[0] < range[1])
	
	counts = Counter(password)
	# Handle zero edge case
	if character not in counts:
		if 0 not in range:
			return False
		else:
			counts[character] = 0

	count = counts[character]
	if range[0] <= count <= range[1]:
		return True
	return False

if __name__ == '__main__':
	input_file = open('input.txt','r')
	lines = [line.strip() for line in input_file.readlines()]
	print('Total: {}'.format(len(lines)))

	count_valid = 0
	for line in lines:
		fields = line.split(' ')
		assert(len(fields) == 3)
		valid = password_valid(fields[2], fields[0], fields[1][0])
		if valid:
			count_valid += 1

	print('Valid: {}'.format(count_valid))
