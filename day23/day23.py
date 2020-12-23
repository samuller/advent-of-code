#!/usr/bin/env python3
import fileinput
# import sys; sys.path.append("..")
# from lib import *


def pickup(cups, curr_idx, start_offset=1, count=3):
	# print('start pickup')
	assert count < len(cups)
	A = cups[curr_idx + start_offset:]
	new_cups = cups[:curr_idx + start_offset]
	if (curr_idx + start_offset) > len(cups):
		A = cups[(curr_idx + start_offset) % len(cups):]
		new_cups = cups[:(curr_idx + start_offset) % len(cups)]
	# print(new_cups,A,count > len(A))
	if count > len(A):
		# assert count / len(A) < 2
		# assert count % len(A) < len()
		count_extra = count - len(A)
		A.extend(cups[:count_extra])
		new_cups = new_cups[count_extra:curr_idx+1]
		new_curr_idx = curr_idx - count_extra
	else:
		for a in A[count:]:
			new_cups.append(a)
		A = A[:count]
		new_curr_idx = curr_idx
	# cups/remaining, picked-up
	return new_cups, A, new_curr_idx
assert pickup([3,8,9,1,2,5,4,6,7],0,1,3) == ([3,2,5,4,6,7], [8,9,1],0)
assert pickup([8,3,6,7,4,1,9,2,5],7,1,3) == ([6,7,4,1,9,2], [5,8,3],5), pickup([8,3,6,7,4,1,9,2,5],7,1,3)
assert pickup([7,4,1,5,8,3,9,2,6],8,1,3) == ([5,8,3,9,2,6], [7,4,1],5), pickup([8,3,6,7,4,1,9,2,5],7,1,3)


def place_right(cups, picked_up, dest_cup_idx):
	cups = cups[:dest_cup_idx+1] + picked_up + cups[dest_cup_idx+1:]
	return cups
assert place_right([3,2,5,4,6,7], [8,9,1], 1) == [3,2,8,9,1,5,4,6,7]
# Move 4?  [7,2,5,8,9,1,3,4,6], print-out rotates such that next cup is one index further
assert place_right([3,2,5,8,9,1], [4,6,7], 0) == [3,4,6,7,2,5,8,9,1], place_right([3,2,5,8,9,1], [4,6,7], 0)


def part1(cups, rounds=100):
	min_cup_lbl = min(cups)
	max_cup_lbl = max(cups)
	curr_cup_idx = 0
	for round in range(rounds):
		curr_cup_lbl = cups[curr_cup_idx]
		cups, picked_up, curr_cup_idx = pickup(cups, curr_cup_idx, start_offset=1, count=3)
		curr_cup_idx = cups.index(curr_cup_lbl)
		assert curr_cup_lbl == cups[curr_cup_idx]
		# print(picked_up)
		dest_cup_lbl = cups[curr_cup_idx]-1
		if dest_cup_lbl < min_cup_lbl:
				dest_cup_lbl = max_cup_lbl
		while dest_cup_lbl in picked_up:
			dest_cup_lbl -= 1
			if dest_cup_lbl < min_cup_lbl:
				dest_cup_lbl = max_cup_lbl
		# print(dest_cup_lbl)
		cups = place_right(cups, picked_up, cups.index(dest_cup_lbl))
		curr_cup_idx = cups.index(curr_cup_lbl)
		### print(cups, cups[curr_cup_idx])
		curr_cup_idx = (curr_cup_idx + 1) % len(cups)
		# print(cups, cups[curr_cup_idx])
	idx = cups.index(1)
	# Part 1
	ans = cups[idx+1:] + cups[:idx]
	print(ans)
	ans = ''.join([str(c) for c in ans])
	print(ans)


def main():
	lines = [line.strip() for line in fileinput.input()]
	print('Lines: {}'.format(len(lines)))

	cups = [int(l) for l in lines[0]]
	print(cups)

	part1(cups)


if __name__ == '__main__':
	main()
