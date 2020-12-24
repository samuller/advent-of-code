#!/usr/bin/env python3
import fileinput
# import sys; sys.path.append("..")
# from lib import *
from collections import defaultdict


def parse_dir(line):
	directions = ['e', 'se', 'sw', 'w', 'nw', 'ne']
	dir = ''
	moves = []
	for i in range(len(line)):
		dir += line[i]
		if dir in directions:
			moves.append(dir)
			dir = ''
	return moves
	# print(line, moves)


def get_rc(moves):
	curr_rc = [0, 0]
	for move in moves:
		row_even = curr_rc[0]%2
		move_action = {
			'w': (0, -1),
			'e': (0, +1),
			'nw': (-1, -row_even),
			'ne': (-1, 1-row_even),
			'sw': (+1, -row_even),
			'se': (+1, 1-row_even)
		}
		assert move in move_action
		action = move_action[move]
		curr_rc[0] += action[0]
		curr_rc[1] += action[1]
		# print(curr_rc)
	return curr_rc


def get_neighbours(tile):
	row_even = tile[0]%2
	neighbours = [
		(0, -1), # w
		(0, +1), # e
		(-1, -row_even),  # nw
		(-1, 1-row_even), # ne
		(+1, -row_even),  # sw
		(+1, 1-row_even)  # se
	]
	return [(tile[0] + n[0], tile[1] + n[1]) for n in neighbours]
assert get_neighbours([0, 0]) == [(0, -1), (0, 1), (-1, 0), (-1, 1), (1, 0), (1, 1)]
assert get_neighbours([1, 0]) == [(1, -1), (1, 1), (0, -1), (0, 0), (2, -1), (2, 0)]


def are_equal(movesA, movesB):
	loc_A = get_rc(movesA)
	loc_B = get_rc(movesB)
	return loc_A == loc_B


def count_black(black_tiles, ref_tile):
	neighbours = get_neighbours(ref_tile)
	count = 0
	for n in neighbours:
		if tuple(n) in black_tiles:
			count += 1
	# print(ref_tile, '->', neighbours, '=', count)
	return count


def flip_by_pattern(black_tiles):
    # Any black tile with zero or more than 2 black tiles
	# 	immediately adjacent to it is flipped to white.
    # Any white tile with exactly 2 black tiles immediately
	# 	adjacent to it is flipped to black.
	assert type(black_tiles) == set

	to_white = set()
	for tile in black_tiles:
		count = count_black(black_tiles, tile)
		if count == 0 or count > 2:
			to_white.add(tuple(tile))

	to_black = set()
	for tile in black_tiles:
		neighbours = get_neighbours(tile)
		# We cover some tiles multiple times from different neighbours
		for outer_tile in neighbours:
			# Only look at white tiles
			if tuple(outer_tile) in black_tiles:
				continue
			count = count_black(black_tiles, outer_tile)
			if count == 2:
				to_black.add(tuple(outer_tile))

	# print('Remove: {}'.format(len(to_white)))
	# print('Add: {}'.format(len(to_black)))
	for w in to_white:
		assert w in black_tiles
		black_tiles.remove(w)
	for b in to_black:
		assert b not in black_tiles
		black_tiles.add(b)

	return black_tiles

# Part 1: hexagon coords
# Part 2: copy-paste add wrong tile to set()
def main():
	lines = [line.strip() for line in fileinput.input()]
	print('Lines: {}'.format(len(lines)))

	assert get_rc(parse_dir('nwwswee')) == [0, 0], get_rc(parse_dir('nwwswee'))
	assert get_rc(parse_dir('esewnw')) == [0, 0], get_rc(parse_dir('esewnw'))
	assert are_equal(parse_dir('esewnw'), parse_dir('nwwswee')), '{} != {}'.format(
		get_rc(parse_dir('esewnw')), get_rc(parse_dir('nwwswee')))

	tile_flips = defaultdict(int)
	for line in lines:
		moves = parse_dir(line)
		tile = get_rc(moves)
		tile_flips[tuple(tile)] += 1
		# print(tuple(tile), line)

	# assert len(tile_flips) == 15, len(tile_flips)
	# print(tile_flips)

	black_tiles = {k for k, v in tile_flips.items() if v % 2 == 1}
	print(len(black_tiles))

	for i in range(100):
		black_tiles = flip_by_pattern(black_tiles)
		print('Day {}: {}'.format(i+1, len(black_tiles)))
	print(len(black_tiles))


if __name__ == '__main__':
	main()
