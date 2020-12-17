#!/usr/bin/env python3
import fileinput
from copy import deepcopy
# import sys; sys.path.append("..")
# from lib import *


def count_neighbours(sparse, w,z,r,c):
	count = 0
	for dw in [-1,0,1]:
		for dz in [-1,0,1]:
			for dr in [-1,0,1]:
				for dc in [-1,0,1]:
					if (dw, dz, dr, dc) == (0,0,0,0):
						continue
					if (w+dw,z+dz,r+dr,c+dc) in sparse:
						count += 1
	return count


def count_all(sparse):
	return len(sparse)


def print_grid(sparse, debug=False):
	ws, zs, rs, cs = list(zip(*sparse))
	for w in range(min(ws), 1+max(ws)):
		for z in range(min(zs), 1+max(zs)):
			print('z =',z,'w=',w)
			for r in range(min(rs), 1+max(rs)):
				for c in range(min(cs), 1+max(cs)):
					if debug:
						print(count_neighbours(sparse,w,z,r,c),end='')
						continue
					if (w,z,r,c) in sparse:
						print('#',end='')
					else:
						print('.',end='')					
				print()


def change_states(sparse):
	new_sparse = set()
	ws, zs, rs, cs = list(zip(*sparse))
	for w in range(min(ws)-1, 2+max(ws)):
		for z in range(min(zs)-1, 2+max(zs)):
			for r in range(min(rs)-1, 2+max(rs)):
				for c in range(min(cs)-1, 2+max(cs)):
					count = count_neighbours(sparse, w,z,r,c)
					if (w,z,r,c) in sparse and count in [2,3]:
						new_sparse.add((w,z,r,c))
					elif (w,z,r,c) not in sparse and count in [3]:
						new_sparse.add((w,z,r,c))
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
				sparse.add((0,0,r,c))

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