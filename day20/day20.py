#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("..")
from lib import *
from collections import defaultdict
from math import sqrt


def print_tile(tile_data):
	for line in tile_data:
		print(line)

def top_line(tile_data):
	return tile_data[0]

def bottom_line(tile_data):
	return tile_data[-1]

def left_line(tile_data):
	return ''.join([l[0] for l in tile_data])

def right_line(tile_data):
	return ''.join([l[-1] for l in tile_data])


def match_sides(side_idx, tblr_sides, other_tblr_sides):
	side_key = ['top', 'bottom', 'left', 'right']
	side = tblr_sides[side_idx]
	rev_side = ''.join(reversed(side))

	if side in other_tblr_sides:
		idx = other_tblr_sides.index(side)
		return side_key[side_idx] + '-' + side_key[idx]
	
	if rev_side in other_tblr_sides:
		idx = other_tblr_sides.index(rev_side)
		return 'flip-' + side_key[side_idx] + '-' + side_key[idx]
	return None


def check_match(tiles, tile_key1, tile_key2):
	tile1 = tiles[tile_key1]
	tile2 = tiles[tile_key2]
	# print_tile(tile1)
	# print()
	# print_tile(tile2)

	# All sides
	tblr1 = [top_line(tile1), bottom_line(tile1), left_line(tile1), right_line(tile1)]
	tblr2 = [top_line(tile2), bottom_line(tile2), left_line(tile2), right_line(tile2)]
	side_key = ['top', 'bottom', 'left', 'right']

	# print_tile(tile1)
	match = match_sides(0, tblr1, tblr2)
	if match:
		return match
	match = match_sides(1, tblr1, tblr2)
	if match:
		return match
	match = match_sides(2, tblr1, tblr2)
	if match:
		return match
	match = match_sides(3, tblr1, tblr2)
	if match:
		return match
	# print('top', top_line)
	# print('bottom', bottom_line)
	# print('left', left_line)
	# print('right', right_line)
	return None


def get_neighbours(pairings):
	tile_types = defaultdict(list)
	for pair, match in pairings.items():
		tile_key1, tile_key2 = pair

		tile_types[tile_key1].append(match)
		tile_types[tile_key2].append(match)
	return tile_types


def get_corners(pairings):
	corners = []
	tile_types = get_neighbours(pairings)

	for key in tile_types.keys():
		# print(key, tile_types[key])
		if len(tile_types[key]) == 2:
			corners.append(key)

	return corners


def remove_borders(tile_data):
	# Remove top & bottom
	tile_data = tile_data[1:-1]
	# Remove left & right
	tile_data = [l[1:-1] for l in tile_data]
	return tile_data


def find_pairings(tiles):
	pairings = {}
	# for t1, t2 in itertools.product(tiles.keys(), tiles.keys())
	for tile_key1 in tiles.keys():
		for tile_key2 in tiles.keys():
			if tile_key1 == tile_key2 or tile_key1 >= tile_key2:
				continue
			# print(tile_key1, tile_key2)
			match = check_match(tiles, tile_key1, tile_key2)
			if match:
				print(tile_key1, tile_key2, match)
				pairings[(tile_key1, tile_key2)] = match
	return pairings


def rotate(tile_data, times):
	pass


def get_full_tiling(tiles, pairings):
	"""Basically solving a puzzle"""
	side_len = sqrt(len(tiles))
	assert side_len == int(side_len)
	side_len = int(side_len)

	tiling = tiles.keys()
	tiling = [[None for _ in range(side_len)] for _ in range(side_len)]

	# Possible pairings for square (horizontal + vertical)
	pairs = 2*side_len*(side_len-1)
	assert pairs == len(pairings)
	print('Pairs:', pairs, '({})'.format(side_len))

	corners = get_corners(pairings)
	print('Corners:', corners)

	print(pairings)
	tile_types = get_neighbours(pairings)
	for key in tile_types:
		print(key, tile_types[key])
	print()

	print('Tiling:', tiling)
	return tiling


def build_full_image(tiles, pairings):

	return tiles[3079]


def find_pattern(tiles, pairings, pattern):
	assert len(pattern) == 3, len(pattern)
	assert len(pattern[0]) == 20, len(pattern[0])

	image = build_full_image(tiles, pairings)
	print_tile(image)
	return None

	# for name, tile in tiles.items():
	# 	print(len(tile))
	# 	return
	# return 0


if __name__ == '__main__':
	lines = [line.strip() for line in fileinput.input()]
	print('Lines: {}'.format(len(lines)))

	tiles = {}
	for group in grouped(lines):
		name = int(group[0].split()[1][:-1])
		tile = group[1:]
		# if name == 3079:
		# 	print('name:',name)
		# 	print_tile(tile)
		tiles[name] = tile
		assert len(tile) == len(tile[0])
		assert len(tile) == 10
	# print(tiles)
	print(len(tiles))
	assert len(tiles) in [9, 144]

	# print(check_match(tiles, 2473, 3079))
	# exit()

	pairings = find_pairings(tiles)
	# print(pairings)
	# assert len(pairings) == 12
	corners = get_corners(pairings)
	print(corners)
	print(prod(corners))

	# Part 2
	tiling = get_full_tiling(tiles, pairings)
	assert tiling == [
		[1951, 2311, 3079],
		[2729, 1427, 2473],
		[2971, 1489, 1171]]


	# Remove borders
	for name in tiles.keys():
		tile = tiles[name]
		tiles[name] = remove_borders(tile)
		# if name == 3079:
		# 	print('name:',name)
		# 	print_tile(tiles[name])

	sea_monster = \
	['                  # ',
	 '#    ##    ##    ###',
	 ' #  #  #  #  #  #   ']
	print(find_pattern(tiles, pairings, sea_monster))
