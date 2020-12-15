#!/usr/bin/env python3
import fileinput
# from collections import defaultdict


def build_history(history, curr_number, curr_pos):
	history[curr_number] = curr_pos
	return history


def first_in_history(history, curr_number):
	return curr_number not in history


def diffs_in_history_pos(history, curr_pos, curr_number):
	return curr_pos - history[curr_number]


def play_game(first_numbers, end_count):
	last_spoken = {}
	for idx, number in enumerate(first_numbers[:-1]):
		pos = idx + 1
		history = build_history(last_spoken, number, pos)
	# print(last_spoken)

	count = len(first_numbers) + 1
	last_number = first_numbers[-1]
	while count < end_count+1:
		next_number = None
		if first_in_history(last_spoken, last_number):
			next_number = 0
		else:
			next_number = diffs_in_history_pos(history, count-1, last_number)

		# print(count, next_number, last_spoken, last_number)
		history = build_history(last_spoken, last_number, count-1)
		# print('last:', last_number, last_spoken[last_number])
		last_number = next_number
		count += 1
	# print(count-1, next_number) #, last_spoken)
	return next_number


def run_tests(lines):
	end_count = int(lines[0])
	print('Running tests till {}...'.format(end_count))
	lines = lines[1:]
	for idx, line in enumerate(lines):
		ans, input = line.split('\t')
		ans = int(ans)
		numbers = [int(n) for n in input.split(',')]
		print(ans, input)
		res = play_game(numbers, end_count)
		assert res == ans, 'Test {} failed with {} instead of {}'.format(idx, res, ans)


if __name__ == '__main__':
	lines = [line.strip() for line in fileinput.input()]
	# lines = ['0,3,6']
	print('Lines: {}'.format(len(lines)))

	if len(lines) > 1:
		run_tests(lines)
		exit()

	numbers = [int(n) for n in lines[0].split(',')]
	print(play_game(numbers, 2020))
	print(play_game(numbers, 30000000))
