#!/usr/bin/env python3
import fileinput


def parse_mask(mask_line):
	mask_line = mask_line.replace('mask = ', '')
	mask_dec = bin_to_int(mask_line.replace('X', '0'))
	return mask_line, mask_dec


def bin_op(val_str, mask_str):
	val_str = val_str.zfill(36)
	mask_str = mask_str.zfill(36)
	val_str = list(val_str)
	masks = {i: m for i, m in enumerate(mask_str) if m != 'X'}
	for idx, value in masks.items():
		val_str[idx] = value
	val_str = ''.join(val_str)
	# print(val_str)
	return bin_to_int(val_str)


def mem_loc_op(mem_val, mask_str):
	mem_val = mem_val.zfill(36)
	mask_str = mask_str.zfill(36)
	mem_val = list(mem_val)
	masks = {i: m for i, m in enumerate(mask_str) if m != '0'}
	for idx, value in masks.items():
		mem_val[idx] = value
	mem_val = ''.join(mem_val)
	x_masks = [idx for idx, m in enumerate(mask_str) if m == 'X']
	num_of_mems = 2**len(x_masks)
	variations = [int_to_bin(l).zfill(len(x_masks)) for l in range(num_of_mems)]
	new_mem_locs = []
	for var in variations:
		new_mem_loc = list(mem_val)
		assert len(var) == len(x_masks)
		for i, x_pos in enumerate(x_masks):
			new_mem_loc[x_pos] = var[i]
		new_mem_loc = ''.join(new_mem_loc)
		new_mem_locs.append(bin_to_int(new_mem_loc))
	return new_mem_locs


def bin_to_int(bin_str):
	return int(bin_str, 2)


def int_to_bin(int_val):
	return '{0:b}'.format(int_val)


# 7:17, 
if __name__ == '__main__':
	lines = [line.strip() for line in fileinput.input()]
	print('Lines: {}'.format(len(lines)))

	p1_memory = {}
	p2_memory = {}
	mask_line = None
	mask_dec = None
	for line in lines:
		if line.startswith('mask = '):
			mask_line, mask_dec = parse_mask(line)
			continue
		mem_loc, mem_val = line.split('=')
		mem_loc = mem_loc.replace('mem[', '').replace('] ', '')
		mem_val = int(mem_val.strip())
		# print(mem_loc, mem_val)
		# Part 1
		p1_memory[mem_loc] = bin_op(int_to_bin(mem_val), mask_line)
		# p1_memory[mem_loc] = mem_val | mask_dec
		# Part 2
		new_mem_locs = mem_loc_op(int_to_bin(int(mem_loc)), mask_line)
		# # print(new_mem_locs)
		for new_mem_loc in new_mem_locs:
			p2_memory[new_mem_loc] = mem_val
		# print(new_mem_loc)
	# print(memory.values())
	print(sum(p1_memory.values()))
	print(sum(p2_memory.values()))
