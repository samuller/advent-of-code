#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("..")
from lib import *
from collections import defaultdict
from math import sqrt
import itertools
from copy import deepcopy


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
		return side_key[side_idx] + '-' + side_key[idx] + '-flip'
	return None


def check_match(tile1, tile2):
	# print_tile(tile1)
	# print()
	# print_tile(tile2)

	# All sides
	tblr1 = [top_line(tile1), bottom_line(tile1), left_line(tile1), right_line(tile1)]
	tblr2 = [top_line(tile2), bottom_line(tile2), left_line(tile2), right_line(tile2)]

	# print_tile(tile1)
	matches = []
	match = match_sides(0, tblr1, tblr2)
	matches.append(match)
	match = match_sides(1, tblr1, tblr2)
	matches.append(match)
	match = match_sides(2, tblr1, tblr2)
	matches.append(match)
	match = match_sides(3, tblr1, tblr2)
	matches.append(match)

	assert len(matches) == 4
	count = 0
	for m in matches:
		if m is not None:
			count += 1
	# Check there aren't multiple matches
	assert count <= 1, count
	for m in matches:
		if m is not None:
			return m
	
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
			tile1 = tiles[tile_key1]
			tile2 = tiles[tile_key2]
			match = check_match(tile1, tile2)
			if match:
				# print(tile_key1, tile_key2, match)
				pairings[(tile_key1, tile_key2)] = match
				set_match = set(match.split('-')[0:2])
				# assert set_match.issubset({'bottom', 'top'}) or set_match.issubset({'left', 'right'}), match
	return pairings


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


def rotation_required(curr_side, new_side):
	sides = ['top', 'right', 'bottom', 'left']
	curr_idx = sides.index(curr_side)
	new_idx = sides.index(new_side)
	if curr_idx == new_idx:
		return 0
	if curr_idx > new_idx:
		return 360 + (new_idx - curr_idx)*90
	return (new_idx - curr_idx)*90
assert rotation_required('top', 'bottom') == 180, rotation_required('top', 'bottom')
assert rotation_required('bottom', 'top') == 180, rotation_required('bottom', 'top')
assert rotation_required('left', 'right') == 180, rotation_required('left', 'right')
assert rotation_required('right', 'left') == 180, rotation_required('right', 'left')
assert rotation_required('left', 'top') == 90, rotation_required('left', 'top')
assert rotation_required('top', 'left') == 270, rotation_required('top', 'left')
assert rotation_required('right', 'bottom') == 90, rotation_required('right', 'bottom')
assert rotation_required('bottom', 'right') == 270, rotation_required('bottom', 'right')


def get_orientation(pairings, tile, friend, friend_pos):
	our_key = sorted([tile, friend])
	pos_key = {
		(-1, 0): 'top',
		( 1, 0): 'bottom',
		( 0,-1): 'left',
		( 0, 1): 'right'
	}
	friend_side = pos_key[tuple(friend_pos)]

	rotate = 0  # 0, 90, 180, 270
	flip = False  # True for vertical/left-right (horizontal vs vertical affects rotation)
	for key, match in pairings.items():
		match = match.split('-')
		if our_key == list(key):
			main_side = match[key.index(tile)]
			rotate = rotation_required(main_side, friend_side)
			if len(match) == 3 and match[2] == 'flip':
				flip = True
				# Rotate 180 if flip is horizontal instead of vertical
				rotate = (rotate+180) % 360 if main_side in ['left', 'right'] else rotate
				# Assumes correct rotations
				#'horz' if match[0] in ['left', 'right'] else 'vert'
			print(tile, friend, friend_side, key.index(tile), match, (rotate, flip))
			return (rotate, flip)
		elif our_key == list(reversed(key)):
			print(tile, friend, 'opposite ' + match)
			# TODO: opposite order
			return (rotate, flip)
	return (rotate, flip)


def rotate_tile(tile_data, angle):
	times = angle // 90
	dim = len(tile_data)
	# print(angle)
	# print_tile(tile_data)
	# print()
	for _ in range(times):
		# Rotate 90 degrees clock-wise
		new_tile_data = []
		for r in range(dim):
			new_tile_data.append('')
			for c in reversed(range(dim)):
				new_tile_data[-1] += tile_data[c][r]
		tile_data = new_tile_data
		# print_tile(tile_data)
		# print()
	return tile_data


def flip_tile(tile_data):
	"""Flip vertically"""
	dim = len(tile_data)
	new_tile_data = []
	for r in range(dim):
		new_tile_data.append('')
		for c in reversed(range(dim)):
			new_tile_data[-1] += tile_data[r][c]
	return new_tile_data


def check_orientation(tiles, tile, orient, neigh, neigh_side):
# def check_orientation(tile_data, orient, neigh_data, neigh_side):
	"""
	Check if given tile and orientation are valid with regard to given neighbouring tile.
	"""
	# assert tiles[tile] == rotate_tile(tiles[tile], 360)
	# assert tiles[tile] == flip_tile(flip_tile(tiles[tile]))
	rot, flip = orient
	tile_data = deepcopy(tiles[tile])
	tile_data = rotate_tile(tiles[tile], rot)
	if flip:
		tile_data = flip_tile(tile_data)

	match = check_match(tile_data, tiles[neigh])
	match = match.split('-')
	# print(tile, neigh, neigh_side, match)

	# If neighbour matches on expected side without being flipped
	if match[0] == neigh_side: # and len(match) == 2:
		return True
	return False


def get_used(tiling):
	side_len = len(tiling)
	used = set()
	for r,c in itertools.product(range(side_len), range(side_len)):
		cell = tiling[r][c]
		if cell is not None:
			used.add(cell)
	return used


drdc_to_side = {
	(-1, 0): 'top',
	( 1, 0): 'bottom',
	( 0,-1): 'left',
	( 0, 1): 'right'
}


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
	used = set([corners[0]])
	iterations = 0
	tile_orientation = {}
	while count_missing_tiles(tiling) != 0:
		placements = [(corners[0],0,0)]
		# Go through each cell to place neighbours
		for r,c in itertools.product(range(side_len), range(side_len)):
			cell = tiling[r][c]
			backup_tiling = deepcopy(tiling)
			if cell is None:
				continue
			friends = list(neighbours[cell])
			perm_found = False
			for idx, perm in enumerate(itertools.permutations(friends)):
				curr_perm = list(perm)
				# Drop tiles that have already been placed
				print(idx, curr_perm, '({})'.format(cell))
				for s in used:
					if s in curr_perm:
						curr_perm.remove(s)
				print(idx, curr_perm, '({})'.format(cell))
				# Place remaining tiles in current order
				for dr,dc in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
					if len(curr_perm) == 0:
						break
					if not 0 <= r+dr < side_len or not 0 <= c+dc < side_len:
						continue
					if tiling[r+dr][c+dc] is None:
						friend = curr_perm.pop()
						tiling[r+dr][c+dc] = friend
						used.add(friend)
						placements.append((friend,r,c))
				print_tile(tiling)
				assert len(curr_perm) == 0, curr_perm
				# Check validity of placement order for all rotations & flips
				assert len(list(itertools.product([0, 90, 180, 270], [False, True]))) == 8
				for rot, flip in itertools.product([0, 90, 180, 270], [False, True]):
					orient = (rot, flip)
					valid = True
					for dr,dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
						if not 0 <= r+dr < side_len or not 0 <= c+dc < side_len:
							continue
						buddy = tiling[r+dr][c+dc]
						if buddy is None:
							continue
						neigh_side = drdc_to_side[(dr, dc)]
						# print(orient, cell, buddy)
						if not check_orientation(tiles, cell, orient, buddy, neigh_side):
						# if not check_orientation(tiles[cell], orient, tiles[buddy], neigh_side):
							# print('sub-failed')
							valid = False
							break
					if valid:
						tile_orientation[cell] = orient
						# print('   ASUCCESCS')
						break
				# If no valid orientation found, roll-back and try next permutation
				if cell not in tile_orientation:
					tiling = backup_tiling
					used = get_used(tiling)
					# print_tile(tiling)
					# print('used', used)
					# print('removing', perm)
					# for p in perm:
					# 	used.remove(p)
				else:
					# Don't need to consider other permutations
					perm_found = True
					break
			print(tile_orientation)
			assert perm_found
			#exit() # br = tr-f, br = lb-f

		iterations += 1
		# TODO: backtracking
		print(tiling)
		print(placements)
		if iterations == 2:
			print('FAILURE!')
			exit()
		# 	break

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


def main():
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
	print_dict(pairings)
	# assert len(pairings) == 12
	corners = get_corners(pairings)
	print(corners)
	print(prod(corners))

	# Part 2
	tiling, tile_orientation = get_full_tiling(tiles, pairings)
	exit()

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


# 2418 (guess of 2) @ 8:37
if __name__ == '__main__':
	main()
