#!/usr/bin/env python3
import fileinput
# import sys; sys.path.append("..")
# from lib import *
from collections import defaultdict


class Classy:
	def __init__(self):
		pass


memoize = defaultdict(dict)
def transform_memoize(subject_num, loop_size):
	start_loop = 0
	value = 1

	if subject_num in memoize:
		if loop_size in memoize[subject_num]:
			return memoize[subject_num][loop_size]
		else:
			start_loop = max(memoize[subject_num].keys())
			if start_loop < loop_size:
				value = memoize[subject_num][start_loop]
			else:
				start_loop = 0

	# print(memoize[7])
	for _ in range(start_loop, loop_size):
		value = value * subject_num
		value = value % 20201227

	memoize[subject_num][loop_size] = value
	# print(memoize[7])
	return value

def transform(subject_num, loop_size, start_loop=0, start_value=1):
	value = start_value
	for _ in range(start_loop, loop_size):
		value = value * subject_num
		value = value % 20201227
	return value


def find_transform(subject_num, result_num):
	trans = 1
	loop = 1
	while True:
	# for loop in range(1, 1_000_000):
		if loop % 10_000_000 == 0:
			print(loop)
		# 	print(loop, len(memoize[subject_num]) if subject_num in memoize else 0)
		# trans = transform_memoize(subject_num, loop)
		trans = transform(subject_num, loop, start_loop=loop-1, start_value=trans)
		if trans == result_num:
			return loop
		loop += 1
	return None


def main():
	# lines = [line.strip() for line in fileinput.input()]
	# print('Lines: {}'.format(len(lines)))

	# card_pub = transform(7)
	# door_pub = transform(7)

	# # Test
	# card_pub = 5764801
	# door_pub = 17807724
	# # assert transform(7, 0) == 1
	# assert transform(7, 8) == 5764801
	# assert transform(7, 11) == 17807724
	# # assert transform(7, 0) == 1
	# assert find_transform(7, 5764801) == 8
	# assert find_transform(7, 17807724) == 11
	# assert transform(17807724, 8) == 14897079
	# assert transform(5764801, 11) == 14897079
	# exit()

	card_pub = 15628416
	door_pub = 11161639

	card_loops = find_transform(7, card_pub)
	door_loops = find_transform(7, door_pub)
	print(card_loops, door_loops)

	card_enc_key = transform(card_pub, door_loops)
	door_enc_key = transform(door_pub, card_loops)
	assert card_enc_key == door_enc_key, '{} != {}'.format(card_enc_key, door_enc_key)
	print(card_enc_key)


if __name__ == '__main__':
	main()
