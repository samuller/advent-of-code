#!/usr/bin/env python3
import fileinput
# import sys; sys.path.append("..")
# from lib import *


if __name__ == '__main__':
	lines = [line.strip() for line in fileinput.input()]
	lines = ['0,3,6']
	lines = ['1,0,18,10,19,6']
	print('Lines: {}'.format(len(lines)))

	numbers = [int(n) for n in lines[0].split(',')]

	times_spoken = {}
	for idx, number in enumerate(numbers):
		pos = idx + 1
		print(pos, number)
		if number in times_spoken:
			times_spoken[number].append(pos)
		else:
			times_spoken[number] = [pos]
	print(times_spoken)

	count = len(numbers) + 1
	last_number = numbers[-1]
	while count < 30000000+1:
	# while count < 2020+1:
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
	print(count-1, speak_number) #, times_spoken)
