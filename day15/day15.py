#!/usr/bin/env python3
import fileinput


def play_game(first_numbers, end_count):
	times_spoken = {}
	for idx, number in enumerate(first_numbers):
		pos = idx + 1
		# print(pos, number)
		if number in times_spoken:
			times_spoken[number].append(pos)
		else:
			times_spoken[number] = [pos]
	# print(times_spoken)

	count = len(first_numbers) + 1
	last_number = first_numbers[-1]
	while count < end_count+1:
		speak_number = None
		if len(times_spoken[last_number]) <= 1:
			speak_number = 0
		else:
			prev_numbers = times_spoken[last_number]
			# print(prev_numbers)
			speak_number = prev_numbers[-1] - prev_numbers[-2]
		
		# print('last:', last_number, times_spoken[last_number])
		# print(count, speak_number) #, times_spoken)
		# print(speak_number in times_spoken)
		if speak_number in times_spoken:
			times_spoken[speak_number].append(count)
		else:
			times_spoken[speak_number] = [count]
		last_number = speak_number
		count += 1
	# print(count-1, speak_number) #, times_spoken)
	return speak_number


def run_tests(lines):
	end_count = int(lines[0])
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
