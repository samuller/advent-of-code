#!/usr/bin/env python
import functools
import numbers
# from copy import deepcopy


def prod(iterable):
	# operator.mul
    return functools.reduce(lambda a,b,: a*b, iterable, 1)


def set_char(stringy, pos, charry):
	list1 = list(stringy)
	list1[pos] = charry
	return ''.join(list1)


def wrap(value, limit):
	return value % limit


class Pos2D:
	def __init__(self, row, col):
		self.row = row
		self.col = col

	# def wrap(self, row, col, shape, wrap=False):
	# 	"""
	# 	p.wrap(5, 6, wrap=True)
	# 	p.wrap(5, 6, wrap=(True, False))
	# 	"""
	# 	assert(isinstance(shape, tuple))
	# 	if isinstance(wrap, bool):
	# 		wrap = (wrap, wrap)
	# 	if wrap[0]:
	# 		row = row % self.rows()
	# 	if wrap[1]:
	# 		col = col % self.cols()
	# 	return row, col

	@property
	def r(self):
		return self.row

	@property
	def c(self):
		return self.col

	@property
	def x(self):
		return self.col

	@property
	def y(self):
		return self.row

	@property
	def h(self):
		return self.row

	@property
	def w(self):
		return self.col


class Map2D:
	"""
	A 2D map based on a list of strings. Has wrapping capabilities.
	"""

	def __init__(self):
		pass

	def load_from_file(self, filename):
		input_file = open(filename,'r')
		mappy = [line.rstrip('\n') for line in input_file.readlines()]
		self.load_from_data(mappy)

	def load_from_data(self, list_of_strings):
		self.map_data = list_of_strings
		self.validate()

	def validate(self):
		assert(self.rows() > 0)
		first_row_len = self.cols()
		for row in self.map_data:
			assert(len(row) == first_row_len)

	# height, y-axis
	def rows(self):
		return len(self.map_data)

	# width, x-axis
	def cols(self):
		return len(self.row(0))

	@property
	def shape(self):
		return (self.rows(), self.cols())

	def row(self, idx):
		return self[idx]
	
	def col(self, idx):
		"""Get a whole column as a string"""
		colly = ''
		for row in self.map_data:
			colly += row[idx]
		return colly

	def in_bounds(self, row, col):
		if (0 <= row < self.rows()) and (0 <= col < self.cols()):
			return True
		return False

	def get(self, row, col):
		return self.map_data[row][col]

	def set(self, row, col, value):
		whole_row = self.map_data[row]
		self.map_data[row] = set_char(whole_row, col, value)

	def __getitem__(self, key):
		"""
		No wrapping capabilities. Use get() for that.
		"""
		if isinstance(key, numbers.Integral):
			key = (key, slice(None, None, None))

		assert(isinstance(key, tuple))
		assert(len(key) == 2)
		# assert(all(isinstance(i, numbers.Integral) for i in key))
		row, col = key
		return self.map_data[row][col]

	def to_str(self):
		stry = ''
		for row in self.map_data:
			stry += row + '\n'
		return stry

	def to_str_partial(self, first=3, last=3):
		"""Show string with only first and last few rows"""
		stry = ''
		for idx in range(first):
			stry += self[idx] + '\n'
		stry += '\n    ...\n\n'
		for idx in range(last, 0, -1):
			stry += self[-idx] + '\n'
		return stry

	def __str__(self):
		stry = 'Size: {}x{}\n'.format(self.rows(), self.cols())	
		if self.rows() <= 10:
			stry += self.to_str()
		else:
			stry += self.to_str_partial()
		return stry

if __name__ == '__main__':
	# mapp = Map2D()
	# mapp.load_from_file('input.txt')
	# print(mapp)
	# print(mapp.get(0, 0))
	# print(mapp.get(322, 30))
	# print(mapp.get(323, 31, wrap=True))
	# print(mapp.get(322, 31, wrap=(False, True)))
	# print(mapp.to_str())
	# print(mapp.col(1))
	pos = Pos2D(1, 2)
	print(pos.r, pos.c)
	print(pos.x, pos.y)
	print(pos.w, pos.h)
	exit()