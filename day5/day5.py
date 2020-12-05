#!/usr/bin/env python
import sys; sys.path.append("..")
from lib import prod, Map2D


def gaps_in_list(listy):
	gaps = []
	listy = sorted(listy)
	prev_val = listy[0] - 1
	for val in listy:
		if (val - prev_val) != 1:
			gaps.append((prev_val, val))
		prev_val = val
	return gaps


# Binary space partition
def bsp_path_parser(bsp_path, second_half_indicator_char):
	size = pow(2, len(bsp_path))
	assert len(set(bsp_path)) <= 2 , set(bsp_path)
	pos = 0
	divisor = size
	for c in bsp_path:
		if c == second_half_indicator_char:
			pos += divisor / 2
		divisor /= 2
	return pos


def parse_seat(full_path):
	row_data = full_path[0:7]
	col_data = full_path[-3:]
	curr_row = bsp_path_parser(row_data, 'B')
	curr_col = bsp_path_parser(col_data, 'R')
	return curr_row, curr_col


# 748, 749, 747
if __name__ == '__main__':
	# Example
	assert bsp_path_parser('FBFBBFF', 'B') == 44
	assert bsp_path_parser('RLR', 'R') == 5
	assert parse_seat('FFFFFFFLLL') == (0, 0)
	assert parse_seat('BBBBBBBRRR') == (127, 7)

	input_file = open('input.txt','r')
	lines = [line.strip() for line in input_file.readlines()]

	rows = 128
	cols = 8
	max_seat = 0
	all_rows = set()
	all_seats = set()
	for line in lines:
		curr_row, curr_col = parse_seat(line)
		seat = curr_row * 8 + curr_col
		assert seat == int(seat)
		seat = int(seat)
		
		all_rows.add(curr_row)
		all_seats.add(seat)
		if seat > max_seat:
			max_seat = seat
	
	print('Highest seat:', max_seat)
	print('Row range:', min(all_rows), '-', max(all_rows))
	print('Row gaps:', gaps_in_list(list(all_rows)))
	seat_gaps = gaps_in_list(list(all_seats))
	print('Seat gaps:', seat_gaps, 'i.e.', seat_gaps[0][0] + 1)
