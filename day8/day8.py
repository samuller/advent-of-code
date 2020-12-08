#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("..")
from lib import *
from copy import deepcopy


def run_cmd(cmds, ptr, acc):
	op, args = cmds[ptr]
	# Always increment to next instruction
	ptr += 1  # UNDO if instruction changes ptr
	if op == 'nop':
		pass
	elif op == 'jmp':
		# Undo pre-increment
		ptr -= 1
		ptr += args
	elif op == 'acc':
		acc += args
	return ptr, acc


def run_code(instructions):
	acc = 0
	ptr = 0
	looped = None
	already_run = set()
	while 0 <= ptr < len(instructions):
		(op, args) = instructions[ptr]
		# print(ptr, op, args)
		assert op in ['nop', 'jmp', 'acc']

		if ptr in already_run:
			looped = ptr
			break
		already_run.add(ptr)

		ptr, acc = run_cmd(instructions, ptr, acc)
	
	return ptr, acc, looped


def parse_instructions(lines):
	instructions = []
	for line in lines:
		if line == '':
			continue
		fields = line.split(' ')
		op = fields[0]
		args = int(fields[1])
		# print(fields, args)
		instructions.append((op, args))
	return instructions


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

	# Part 1
	instructions = parse_instructions(lines)
	# print(instructions)
	ptr, acc, looped = run_code(instructions)
	print('END with', acc, '\n')

	# Part 2
	print('Part2:')
	for idx, (op, args) in enumerate(instructions):
		# print(idx)
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
				print('loop broken at', idx, op, args)
				break

	# ptr, acc, looped = run_code(instructions)
	print('looped at', looped)
	print('END at', ptr, 'with', acc)
