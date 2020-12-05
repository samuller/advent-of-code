#!/usr/bin/env python
import sys; sys.path.append("..")
from lib import prod, Map2D


def function(input):
	return False

# 748, 749
if __name__ == '__main__':
	input_file = open('input.txt','r')
	lines = [line.strip() for line in input_file.readlines()]
	print('Lines: {}'.format(len(lines)))

	rows = 128
	cols = 8
	max_val = 0
	all_rows = set()
	all_seats = set()
	for line in lines: # ['FBFBBFFRLR']:# lines:
		row = line[0:7]
		col = line[-3:]

		# print(row, col)

		# print(row)
		row_divisor = 128
		curr_row = 0
		for r in row:
			if r == 'F':
				curr_row += 0
			else:
				curr_row += row_divisor / 2
			row_divisor /= 2
			# print(curr_row, row_divisor)
		# print(curr_row, row_divisor)

		# print(col)
		col_divisor = 8
		curr_col = 0
		for c in col:
			if c == 'L':
				curr_col += 0
			else:
				curr_col += col_divisor / 2
			col_divisor /= 2
			# print(curr_col, col_divisor)
		# print(curr_col, col_divisor)

		seat = curr_row * cols + curr_col
		all_rows.add(curr_row)
		all_seats.add(seat)
		# print(seat)
		if seat > max_val:
			max_val = seat
	
	# print(max_val)
	# print(sorted(list(all_rows)))
	# prev_val = 0
	# for val in sorted(list(all_rows)):
	# 	if (val - prev_val) != 1:
	# 		print(val)
	# 	prev_val = val

	prev_val = 0
	for val in sorted(list(all_seats)):
		print(val)
		# if (val - prev_val) != 1:
			# print(val)
		prev_val = val



