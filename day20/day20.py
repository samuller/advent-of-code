#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("..")
from lib import *
from collections import defaultdict
from math import sqrt
import itertools


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
	return None


def get_neighbours(pairings):
	tile_types = defaultdict(list)
	for pair, match in pairings.items():
		tile_key1, tile_key2 = pair

		tile_types[tile_key1].append(tile_key2)
		tile_types[tile_key2].append(tile_key1)
		# tile_types[tile_key1].append(match)
		# tile_types[tile_key2].append(match)
	return tile_types


def get_sides_with_count(pairings, count=2):
	corners = []
	tile_types = get_neighbours(pairings)

	for key in tile_types.keys():
		# print(key, tile_types[key])
		if len(tile_types[key]) == count:
			corners.append(key)

	return corners


def get_corners(pairings):
	return get_sides_with_count(pairings, 2)


def get_sides(pairings):
	return get_sides_with_count(pairings, 3)


def get_insides(pairings):
	return get_sides_with_count(pairings, 4)


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
				# print(tile_key1, tile_key2, match)
				pairings[(tile_key1, tile_key2)] = match
	return pairings


def rotate(tile_data, times):
	pass


def count_values(tile_data, value='#'):
	count = 0
	for line in tile_data:
		count += line.count(value)
	return count


def count_all_values(tiles, value='#'):
	total_count = 0
	for name, tile_data in tiles.items():
		total_count += count_values(tile_data, value)
	return total_count


def count_missing_tiles(tiling):
	count_nones = 0
	for row in tiling:
		count_nones += row.count(None)
	return count_nones


def empty_tiling(side_len):
	return [[None for _ in range(side_len)] for _ in range(side_len)]


def print_dict(dic):
	for key in sorted(dic.keys()):
		print(key, dic[key])
	print()


def get_orientation(pairings, tile, friend, friend_pos):
	rotate = 0
	flip = 0
	for key, match in pairings.items():
		t1, t2 = key
		if (tile, friend) == key:
			print(tile, friend, match)
		elif (friend, tile) == key:
			print(tile, friend, match)
	# print(pairings)
	return (rotate, flip)


def get_full_tiling(tiles, pairings):
	"""Basically solving a puzzle"""
	side_len = sqrt(len(tiles))
	assert side_len == int(side_len)
	side_len = int(side_len)
	# Possible pairings for square (horizontal + vertical)
	pairs = 2*side_len*(side_len-1)
	assert pairs == len(pairings)
	print('Pairs:', pairs, '({})'.format(side_len))

	tiling = empty_tiling(side_len)

	neighbours = get_neighbours(pairings)
	# print_dict(neighbours)
	corners = get_corners(pairings)
	name = corners[0]
	tiling[0][0] = corners[0]
	tile_orientation = {}
	iterations = 0
	while count_missing_tiles(tiling) != 0:
		for r,c in itertools.product(range(side_len), range(side_len)):
			cell = tiling[r][c]
			if cell is None:
				continue
			friends = list(neighbours[cell])
			for dr,dc in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
				if not 0 <= r+dr < side_len or not 0 <= c+dc < side_len:
					continue
				if tiling[r+dr][c+dc] is None:
					friend = friends.pop()
					tile_orientation[friend] = get_orientation(pairings, cell, friend, (dr,dc))
					tiling[r+dr][c+dc] = friend
				if len(friends) == 0:
					break
		iterations += 1
		# print(tiling)
		# if iterations == 2:
		# 	exit()

	print('Tiling:')
	for line in tiling:
		print('   '.join([str(l) for l in line]))
	return tiling, tile_orientation


def build_full_image(tiles, pairings):
	tiling, tile_orientation = get_full_tiling(tiles, pairings)
	# assert tiling == [
	# 	[1951, 2311, 3079],
	# 	[2729, 1427, 2473],
	# 	[2971, 1489, 1171]]
	side_len = int(sqrt(len(tiles)))
	tile_len = None
	for name, tile_data in tiles.items():
		if tile_len is not None:
			assert tile_len == len(tile_data[0]), '{} != {}'.format(
				tile_len, len(tile_data[0]))
		tile_len = len(tile_data[0])
	print('{}x{}'.format(tile_len, tile_len))

	# full_tiles = [[tiles[tiling[r][c]] for r in range(side_len)] for c in range(side_len)]
	image = []
	for r in range(side_len):
		for _ in range(tile_len):
			image.append('')
		for c in range(side_len):
			name = tiling[r][c]
			tile_data = tiles[name]
			# TODO: rotations & flips
			print(name, tile_orientation[name])
			for idx, tr in enumerate(tile_data):
				image[r*tile_len + idx] = image[r*tile_len + idx] + tr
			# print(tile_data)
			# print_tile(tile_data)
			# exit()

	assert len(image) == side_len * tile_len
	for line in image:
		assert len(line) == side_len * tile_len

	return image


def match_template(image, template, im_row, im_col):
	for tmp_row in range(len(template)):
		for tmp_col in range(len(template[tmp_row])):
			tmp_val = template[tmp_row][tmp_col]
			# If no space for matching rest of template
			if im_row+tmp_row >= len(image) or \
				im_col+tmp_col >= len(image[im_row+tmp_row]):
				return False
			im_val = image[im_row+tmp_row][im_col+tmp_col]
			if tmp_val  == '#' and im_val != '#':
				return False
	return True


def find_pattern(tiles, pairings, pattern):
	assert len(pattern) == 3, len(pattern)
	assert len(pattern[0]) == 20, len(pattern[0])
	assert match_template(pattern, pattern, 0, 0)

	image = build_full_image(tiles, pairings)
	print_tile(image)
	print_tile(pattern)
	dim = len(image)
	# Template matching
	matches = []
	for im_row in range(dim):
		for im_col in range(dim):
			if match_template(image, pattern, im_row, im_col):
				matches.append((im_row, im_col))
	return matches


# 2418 (guess of 2) @ 8:37
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
	patterns_found = find_pattern(tiles, pairings, sea_monster)
	print('Patterns:', patterns_found)
	print(len(patterns_found))

	total_count = count_all_values(tiles)
	print('Total count', total_count)
	print(total_count - 30*len(patterns_found))
