#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("..")
from lib import *
from copy import deepcopy


def run_code(instructions):
	acc = 0
	ptr = 0
	looped = None
	already_run = []
	while ptr < len(instructions):
		(op, args) = instructions[ptr]
		# print(ptr, op, args)

		if ptr in already_run:
			looped = ptr
			break
		already_run.append(ptr)
		
		ptr += 1
		if op == 'nop':
			continue
		if op == 'jmp':
			ptr -= 1
			ptr += args
			continue
		if op == 'acc':
			acc += args
			continue
	
	return ptr, acc, looped


if __name__ == '__main__':
	lines = [line.strip() for line in fileinput.input('input.txt')]
	test = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
"""
	# lines = test.split('\n')
	print('Lines: {}'.format(len(lines)))
	# print(lines)

	instructions = []
	for line in lines:
		if line == '':
			continue
		fields = line.split(' ')
		op = fields[0]
		args = int(fields[1])
		# print(fields, args)
		instructions.append((op, args))
	
	# print(instructions)
	ptr, acc, looped = run_code(instructions)
	for idx, (op, args) in enumerate(instructions):
		# print(idx, op, args)
		print(idx)
		new_op = None
		if op == 'nop':
			new_op = 'jmp'
		if op == 'jmp':
			new_op = 'nop'
		if new_op is not None:
			new_instructions = deepcopy(instructions)
			new_instructions[idx] = (new_op, args)
			ptr, acc, looped = run_code(new_instructions)
			if looped is None:
				print('loop broken at ', idx, op, args)
				break

	# ptr, acc, looped = run_code(instructions)
	print('\nlooped at', looped)
	print('\nEND at', ptr, 'with', acc)

