#!/usr/bin/env python

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
