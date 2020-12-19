#!/usr/bin/env python3
import fileinput
import re


def calc_op(op_str):
	assert re.match(r'^\d+ [+*\-] \d+$', op_str) is not None, op_str
	return str(eval(op_str))


def calc_boam(op_str):
	# Part 2 - brackets-of-addition-multiplication (not BODMAS)
	op_str = subrec(r'\d+ \+ \d+', lambda m: calc_op(m.group(0)), op_str)
	op_str = subrec(r'\d+ \* \d+', lambda m: calc_op(m.group(0)), op_str)
	return str(eval(op_str))


def calc_bo(op_str):
	# Part 1 - brackets-only (not BODMAS)
	# We count=1 so that we successively replace the first value from the left
	# (otherwise all non-overlapping matches are handled simultaneously)
	op_str = subrec(r'\d+ [*+] \d+', lambda m: calc_op(m.group(0)), op_str, count=1)
	return op_str


def subrec(pattern, repl, string, count=0):
	"""Substitute recursively"""
	string, subs = re.subn(pattern, repl, string, count)
	while subs != 0:
		string, subs = re.subn(pattern, repl, string, count)
	return string


def parse_and_calc(input, parse_func=calc_bo):
	# Recursively process parentheses
	input = subrec(r'\(([^()]+)\)', lambda m: parse_func(m.group(1)), input)
	input = parse_func(input)
	return int(input)


def sum_of_calcs(lines, parse_func=calc_bo):
	sum_ = 0
	for line in lines:
		sum_ += parse_and_calc(line, parse_func)
	return sum_


if __name__ == '__main__':
	lines = [line.strip() for line in fileinput.input()]
	print('Lines: {}'.format(len(lines)))

	# assert parse_and_calc('1 + 2 * 3 + 4 * 5 + 6') == 71
	# assert parse_and_calc('1 + (2 * 3) + (4 * (5 + 6))') == 51
	# assert parse_and_calc('2 * 3 + (4 * 5)') == 26
	# assert parse_and_calc('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 437
	# assert parse_and_calc('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 12240
	# assert parse_and_calc('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 13632

	# def parse_and_calc2(inp):
	# 	return parse_and_calc(inp, parse_func=calc_boam)
	# assert parse_and_calc2('1 + 2 * 3 + 4 * 5 + 6') == 231
	# assert parse_and_calc2('1 + (2 * 3) + (4 * (5 + 6))') == 51
	# assert parse_and_calc2('2 * 3 + (4 * 5)') == 46
	# assert parse_and_calc2('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 1445
	# assert parse_and_calc2('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 669060
	# assert parse_and_calc2('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 23340
	# exit()
	
	print(sum_of_calcs(lines, parse_func=calc_bo))
	print(sum_of_calcs(lines, parse_func=calc_boam))
