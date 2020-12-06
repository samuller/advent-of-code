#!/usr/bin/env python
import sys; sys.path.append("..")
from lib import prod, Map2D


if __name__ == '__main__':
	input_file = open('input.txt','r')
	test = """
abc

a
b
c

ab
ac

a
a
a
a

b
	"""
	# internet connection...
	# 6567, 6585? (server @ 7:11, @ 7:14) / 3264 (0729)
	lines = [line.strip() for line in input_file.readlines()] #test]
	# lines = test.split('\n')
	lines.append('\n')
	print('Lines: {}'.format(len(lines)))
	

	count_valid = 0
	curr_group = set()
	curr_group_2 = set()
	line_in_group = 0
	total_quest = 0
	total_quest_2 = 0
	for line in lines:
		print(''.join(sorted(line)))
		if line.strip() == '':
			curr_ques_count = len(curr_group)
			total_quest += curr_ques_count
			total_quest_2 += len(curr_group_2)
			# print('[1]:', curr_group, len(curr_group), total_quest)
			# new group
			print('end', ''.join(sorted(curr_group_2)))
			print('[2]:', curr_group_2, len(curr_group_2), total_quest_2)
			line_in_group = 0
			curr_group = set()
			curr_group_2 = set()
		else:
			tmp_curr_group_2 = set()
			for c in line.strip():
				curr_group.add(c)
				tmp_curr_group_2.add(c)
			if len(curr_group_2) == 0 and line_in_group == 0:
				curr_group_2 = tmp_curr_group_2
			else:
				# curr_group_2 -= tmp_curr_group_2
				eval_curr_group_2 = curr_group_2.copy()
				for c in curr_group_2:
					if c not in tmp_curr_group_2:
						eval_curr_group_2.remove(c)
				curr_group_2 = eval_curr_group_2
			line_in_group += 1
	curr_ques_count = len(curr_group)
	total_quest += curr_ques_count
	# print(curr_group, len(curr_group), total_quest)
	# print(total_quest)

	total_quest_2 += len(curr_group_2)
	print('end-fin', ''.join(sorted(curr_group_2)))
	print('[2]:', curr_group_2, len(curr_group_2), total_quest_2)
	print(total_quest_2)


