#!/usr/bin/env python
import sys; sys.path.append("..")
from lib import prod, Map2D


class Classy:
	def __init__(self):
		pass


def function(input):
	return False


if __name__ == '__main__':
	lines = []
	with open('input.txt', 'r') as input_file:
		lines = [line.strip() for line in input_file.readlines()]
	print('Lines: {}'.format(len(lines)))

	count_valid = 0
	for line in lines:
		fields = line.split(' ')
