#!/usr/bin/env python3
import fileinput
from copy import deepcopy
# import sys; sys.path.append("..")
# from lib import *


def count_neighbours(grid, z,r,c, voi='#'):
	# voi = value of interest
	count = 0
	for dz in [-1,0,1]:
		for dr in [-1,0,1]:
			for dc in [-1,0,1]:
				if (dz, dr, dc) == (0,0,0):
					continue
				if 0 <= z+dz < len(grid) and \
					0 <= r+dr < len(grid[z+dz]) and \
						0 <= c+dc < len(grid[z+dz][r+dr]):
					val = grid[z+dz][r+dr][c+dc]
				else:
					val = '.'
				if val == voi:
					count += 1
	return count


def count_all(grid):
	count = 0
	for z in range(len(grid)):
		for r in range(len(grid[z])):
			for c in range(len(grid[z][r])):
				if grid[z][r][c] == '#':
					count += 1
	return count


def gen_2d_grid(size):
	return [['.' for _ in range(size)] for _ in  range(size)]


def increase_size(grid):
	"""Increases all 3 dimensions by 1."""
	zs = len(grid)
	rs = len(grid[0])
	new_z = (zs + 2)//2

	new_grid = []
	# Add z = -1
	new_grid.append(gen_2d_grid(2+rs))
	for z in range(len(grid)):
		# Add z = 0 (to be filled-in)
		new_grid.append([])
		# Add r = -1
		new_grid[z+1].append(['.' for _ in range(2+len(grid[z]))])
		for r in range(len(grid[z])):
			new_row = ['.']  # Add c = -1
			new_row.extend(grid[z][r])  # Add c = 0
			new_row.append('.')  # Add c = +1
			# Add r = 0
			new_grid[z+1].append(new_row)
		# Add r = +1
		new_grid[z+1].append(['.' for _ in range(2+len(grid[z]))])
	# Add z = +1
	new_grid.append(gen_2d_grid(2+rs))
	return new_grid


def print_grid(grid, debug=False):
	for z in range(len(grid)):
		print('z =',z)
		for r in range(len(grid[z])):
			for c in range(len(grid[z][r])):
				if debug:
					# print(grid[z][r][c], count_neighbours(grid, z,r,c),end='')
					print(count_neighbours(grid, z,r,c),end='')
				else:
					print(grid[z][r][c], end='')
			print()
	return False


def change_states(grid):
	new_grid = deepcopy(grid)
	for z in range(len(grid)):
		for r in range(len(grid[z])):
			for c in range(len(grid[z][r])):
				count = count_neighbours(grid, z,r,c)
				if grid[z][r][c] == '#' and count in [2,3]: # 3
					new_grid[z][r][c] = '#'
				elif grid[z][r][c] == '.' and count in [3]: # 1,2,3,5
					new_grid[z][r][c] = '#'
				else:
					new_grid[z][r][c] = '.'
	return new_grid

# Part 1 - Forgot to count outside of grid
# 
if __name__ == '__main__':
	lines = [line.strip() for line in fileinput.input()]
	print('Lines: {}'.format(len(lines)))

	dim = len(lines)
	grid = []  # [[list(l) for l in lines]]
	grid.append(gen_2d_grid(dim))
	grid.append([list(l) for l in lines])
	grid.append(gen_2d_grid(dim))

	print(grid)
	# print_grid(grid)
	# exit()
	# print(count_all(grid))

	# grid = increase_size(grid)
	# print(grid)
	# print_grid(grid)

	# grid = increase_size(grid)
	# print(grid)
	# print_grid(grid)
	# exit()

	for i in range(6):
		print('After {} cycles:'.format(i))
		if i < 3:
			print_grid(grid)
			print_grid(grid, debug=True)
		grid = increase_size(grid)
		grid = change_states(grid)

		# print('\n\nNow')
		# print_grid(grid)
		# exit()
	print(count_all(grid))