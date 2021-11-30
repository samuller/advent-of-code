#!/usr/bin/env python3
import fileinput
from collections import defaultdict


def transform(subject_num, loop_size, start_loop=0, start_value=1):
	# return pow(subject_num, loop_size, 20201227)
	# return pow(subject_num, loop_size) % 20201227
	value = start_value
	for _ in range(start_loop, loop_size):
		value = value * subject_num
		value = value % 20201227
	return value


def find_transform(subject_num, result_num):
	trans = 1
	loop = 1
	while True:
		# if loop % 10_000_000 == 0:
		# 	print('Progress... {}'.format(loop))
		trans = transform(subject_num, loop, start_loop=loop-1, start_value=trans)
		if trans == result_num:
			return loop
		loop += 1
	return None


def main():
	lines = [line.strip() for line in fileinput.input()]

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

	card_pub = int(lines[0]) # 15628416
	door_pub = int(lines[1]) # 11161639

	door_loops = find_transform(7, door_pub)
	card_enc_key = transform(card_pub, door_loops)
	# Print answer early
	print(card_enc_key)
	# Do confirmation steps later
	card_loops = find_transform(7, card_pub)
	door_enc_key = transform(door_pub, card_loops)
	assert card_enc_key == door_enc_key, '{} != {}'.format(card_enc_key, door_enc_key)
	print('Confirmed:',card_loops, door_loops)


if __name__ == '__main__':
	main()
