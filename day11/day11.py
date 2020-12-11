#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("..")
from lib import *
from copy import deepcopy


def surroundings(mappy, row, col):
	n = []
	for c in range(col-1,1+col+1):
		for r in range(row-1,1+row+1):
			# print(c,r)
			if 0 <= c < mappy.cols and 0 <= r < mappy.rows and (r,c) != (row, col):
				n.append(mappy.get(r,c))
	assert len(n) in [3, 5, 7, 8], len(n)
	return n

def count_far_surroundings(mappy, row, col):
	count = 0
	# Right row
	for c in range(col+1, mappy.cols):
		val = mappy.get(row,c)
		if val == '#':
			count += 1
		if val in ['#', 'L']:
			break
	# Left row
	for c in range(col-1, -1, -1):
		val = mappy.get(row,c)
		if val == '#':
			count += 1
		if val in ['#', 'L']:
			break
	# Top
	for r in range(row-1, -1, -1):
		val = mappy.get(r,col)
		if val == '#':
			count += 1
		if val in ['#', 'L']:
			break
	# Bottom
	for r in range(row+1, mappy.rows):
		val = mappy.get(r,col)
		if val == '#':
			count += 1
		if val in ['#', 'L']:
			break
	# Left-top
	rc = 1
	while mappy.in_bounds(row-rc, col-rc):
		val = mappy.get(row - rc,col - rc)
		if val == '#':
			count += 1
		if val in ['#', 'L']:
			break
		rc += 1
	# Left-bottom
	rc = 1
	while mappy.in_bounds(row+rc, col-rc):
		val = mappy.get(row + rc,col - rc)
		if val == '#':
			count += 1
		if val in ['#', 'L']:
			break
		rc += 1
	# Right-top
	rc = 1
	while mappy.in_bounds(row-rc, col+rc):
		val = mappy.get(row - rc,col + rc)
		if val == '#':
			count += 1
		if val in ['#', 'L']:
			break
		rc += 1
	# Right-bottom
	rc = 1
	while mappy.in_bounds(row+rc, col+rc):
		val = mappy.get(row + rc,col + rc)
		if val == '#':
			count += 1
		if val in ['#', 'L']:
			break
		rc += 1
	return count

def count_taken_seats(mappy):
	total_count = 0
	for c in range(next_mappy.cols):
		for r in range(next_mappy.rows):
			if next_mappy.get(r,c) == '#':
				total_count += 1
	return total_count


if __name__ == '__main__':
	test1 = """.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#....."""
	test2 = """.............
.L.L.#.#.#.#.
............."""
	test3 = """.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##."""
	# mappy = Map2D()
	# mappy.load_from_data(test1.split('\n'))
	# assert count_far_surroundings(mappy, 4, 3) == 8
	# mappy = Map2D()
	# mappy.load_from_data(test2.split('\n'))
	# assert count_far_surroundings(mappy, 1, 1) == 0
	# mappy = Map2D()
	# mappy.load_from_data(test3.split('\n'))
	# assert count_far_surroundings(mappy, 3, 3) == 0
	# exit()

	test = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""
	lines = [line.strip() for line in fileinput.input('input.txt')]
	# lines = test.split('\n')
	print('Lines: {}'.format(len(lines)))

	mappy = Map2D()
	# mappy.load_from_file('input.txt')
	mappy.load_from_data(lines)
	print(mappy)

	prev_mappy = mappy
	next_mappy = deepcopy(prev_mappy)
	prev_count = 123
	curr_count = count_taken_seats(next_mappy)
	loops = 0
	while prev_count != curr_count:
		prev_count = curr_count
		prev_mappy = next_mappy
		next_mappy = deepcopy(prev_mappy)
		for c in range(prev_mappy.cols):
			for r in range(prev_mappy.rows):
				if prev_mappy.get(r,c) == '.':
					continue
				# print(c,r, mappy.get(r,c))
				# Part 1
				# nhs = surroundings(prev_mappy, r, c)
				# count = 0
				# for n in nhs:
				# 	if n == '#':
				# 		count += 1
				# Part 2
				count = count_far_surroundings(prev_mappy, r, c)
				# print(count, nhs)
				if count == 0:
					next_mappy.set(r,c, '#')
				elif count >= 5:
					next_mappy.set(r,c, 'L')
		curr_count = count_taken_seats(next_mappy)
		loops += 1
		print(loops)
	print(next_mappy)
	print(count_taken_seats(next_mappy))
