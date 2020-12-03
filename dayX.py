#!/usr/bin/env python
import sys; sys.path.append("..")
from lib import prod, Map2D


class Classy:
	def __init__(self):
		pass


def function(input):
	return False


if __name__ == '__main__':
	input_file = open('input.txt','r')
	lines = [line.strip() for line in input_file.readlines()]
	print('Lines: {}'.format(len(lines)))

	count_valid = 0
	for line in lines:
		fields = line.split(' ')
