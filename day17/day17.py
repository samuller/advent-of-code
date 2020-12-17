#!/usr/bin/env python3
import fileinput
from copy import deepcopy
# import sys; sys.path.append("..")
# from lib import *


def count_neighbours(sparse, z,r,c):
	count = 0
	for dz in [-1,0,1]:
		for dr in [-1,0,1]:
			for dc in [-1,0,1]:
				if (dz, dr, dc) == (0,0,0):
					continue
				if (z+dz,r+dr,c+dc) in sparse:
					count += 1
	return count


def count_all(sparse):
	return len(sparse)


def print_grid(sparse, debug=False):
	zs, rs, cs = list(zip(*sparse))
	for z in range(min(zs), 1+max(zs)):
		print('z =',z)
		for r in range(min(rs), 1+max(rs)):
			for c in range(min(cs), 1+max(cs)):
				if debug:
					print(count_neighbours(sparse,z,r,c),end='')
					continue
				if (z,r,c) in sparse:
					print('#',end='')
				else:
					print('.',end='')					
			print()


def change_states(sparse):
	new_sparse = set()
	zs, rs, cs = list(zip(*sparse))
	for z in range(min(zs)-1, 2+max(zs)):
		for r in range(min(rs)-1, 2+max(rs)):
			for c in range(min(cs)-1, 2+max(cs)):
				count = count_neighbours(sparse, z,r,c)
				if (z,r,c) in sparse and count in [2,3]:
					new_sparse.add((z,r,c))
				elif (z,r,c) not in sparse and count in [3]:
					new_sparse.add((z,r,c))
	return new_sparse

# Part 1 - Forgot to count outside of grid, didn't use sparse data set
# 
if __name__ == '__main__':
	lines = [line.strip() for line in fileinput.input()]
	print('Lines: {}'.format(len(lines)))

	dim = len(lines)
	tmp_grid = [list(l) for l in lines]
	sparse = set()
	for r in range(dim):
		for c in range(dim):
			if tmp_grid[r][c] == '#':
				sparse.add((0,r,c))

	print(sparse)
	print(list(zip(*sparse)))

	# print_grid(sparse)
	# print_grid(change_states(sparse))
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
			print_grid(sparse)
			# print_grid(sparse, debug=True)
		sparse = change_states(sparse)

		# print('\n\nNow')
		# print_grid(grid)
		# exit()
	print(count_all(sparse))