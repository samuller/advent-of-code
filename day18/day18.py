#!/usr/bin/env python3
import fileinput
import re


def calc_op(op_str):
	assert re.match(r'^\d+ [+*\-] \d+$', op_str) is not None, op_str
	return eval(op_str)


def calc_str(op_str):
	# Enable for part 2
	op_str = parse_and_replace(r'\d+ \+ \d+', op_str, replace_with=calc_op)
	op_str = parse_and_replace(r'\d+ \* \d+', op_str, replace_with=calc_op)
	# Part 1
	symbols = op_str.split(' ')
	assert len(symbols) % 2 == 1
	result = symbols[0]
	for i in range(1,len(symbols), 2):
		to_calc = '{} '.format(result) + ' '.join(symbols[i:1+i+1])
		result = calc_op(to_calc)
		# print(to_calc)
	return result


def parse_and_replace(pattern, input, replace_with=calc_str):
	"""
	Find string matching regex pattern and then replace it
	(or the first capture group) with the value returned by
	replace_with() which is given the matching string as input.
	"""
	look = re.search(pattern, input)
	while look is not None: # :=
		span = look.span()
		substr = look.group(0)
		if len(look.groups()) >= 1:
			substr = look.group(1)
		# print(substr)
		input = input[:span[0]] + '{}'.format(replace_with(substr)) + input[span[1]:]
		# print(input)
		look = re.search(pattern, input)
	return input


def parse_and_calc(input):
	# Recursively process parentheses
	# while re.search(pattern, input)

	input = parse_and_replace(r'\(([^()]+)\)', input)
	# print(input)
	# input = parse_and_replace(r'\d+ [+*\-] \d+', input, False)
	input = calc_str(input)
	return int(input)


if __name__ == '__main__':
	lines = [line.strip() for line in fileinput.input()]
	print('Lines: {}'.format(len(lines)))

	# assert parse_and_calc('1 + 2 * 3 + 4 * 5 + 6') == 71
	# assert parse_and_calc('1 + (2 * 3) + (4 * (5 + 6))') == 51
	# assert parse_and_calc('2 * 3 + (4 * 5)') == 26
	# assert parse_and_calc('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 437
	# assert parse_and_calc('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 12240
	# assert parse_and_calc('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 13632

	# assert parse_and_calc('1 + 2 * 3 + 4 * 5 + 6') == 231
	# assert parse_and_calc('1 + (2 * 3) + (4 * (5 + 6))') == 51
	# assert parse_and_calc('2 * 3 + (4 * 5)') == 46
	# assert parse_and_calc('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 1445
	# assert parse_and_calc('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 669060
	# assert parse_and_calc('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 23340
	# exit()
	
	sum_ = 0
	for line in lines:
		sum_ += parse_and_calc(line)
	print(sum_)
