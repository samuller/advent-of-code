#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("..")
from lib import *
import re


def matches_rec(specs, input, root_spec): #spec_key='0'):
#	print("'{}'".format(input), root_spec)
	# root_spec = specs[spec_key]
	# Base case
	if root_spec.startswith('"'):
		spec = root_spec[1:-1]
		if input.startswith(spec):
			return 1, root_spec
		else:
			return 0, root_spec

	longest_match = (0, None)
	paths = root_spec.split(' | ')
	assert len(paths) <= 2, paths
	for path in paths:
		symbols = path.split(' ')
		# if len(symbols) == 1:
		# 	chars_matching = matches_rec(specs, input, specs[symbols[0]])
		# 	longest_match = max(longest_match, chars_matching)
		# 	continue

		chars_matching = 0
		full_path = path
#		print('___', path,'___')
		for sym in symbols:
			# if sym in ['8', '42'] and len(input) % 5 != 0:
			# 	# Force fail
			# 	print('SKIPSSS!')
			# 	chars_matching = 0
			# 	break
#			if sym == '8':
#				print('==========')
#			if sym == '11':
#				print('<><><><><><><><><>')
#			print(sym, '=> ', end="")
			# If matching completes but there are still symbols left
			if input[chars_matching:] == '' or \
				len(symbols) > len(input): # Assume no empty symbols
				print('WOAH!')
				# Then force it to fail
				chars_matching = 0
				break
			n, sub_path = matches_rec(specs, input[chars_matching:], specs[sym])
			full_path += '({})'.format(sub_path)
			chars_matching += n
#			print('    ', input, sym, '({})'.format(path), '=', chars_matching)
			# Ensure rule matches something (not sure if needed and wouldn't generalise
			# to specs with dead-ends/empty symbols)
			if n == 0:
				break
		# Small optimization
		# if chars_matching == len(input):
		# 	return chars_matching

		longest_match = max(longest_match, (chars_matching, full_path), key=lambda t: t[0])

	return longest_match


def find_literal(specs):
	for key, spec in specs.items():
		if spec.startswith('"'):
			return key, spec
	return None


def replace_literals(specs):
	while find_literal(specs) is not None:
		# Current literal
		lit_key, lit_val = find_literal(specs)
		lit_val = lit_val.replace('"', '')
		for key in specs.keys():
			symbols = specs[key].split(' ')
			while str(lit_key) in symbols:
				idx = symbols.index(str(lit_key))
				symbols[idx] = lit_val
				specs[key] = ' '.join(symbols)
		# Remove/ignore literal
		specs[lit_key] = ''
	return specs


def replace_rules(specs):
	for key in sorted(specs.keys(), key=int, reverse=True):
		for num in re.findall('\d+', specs[key]):
			ref_spec = specs[num]
			if '|' in ref_spec:
				parts = []
				for val in ref_spec.split(' | '):
					parts.append(specs[key].replace(num, val))
				specs[key] = ' | '.join(parts)
			else:
				specs[key] = specs[key].replace(num, ref_spec)
	return specs


def print_specs(specs):
	for key in sorted(specs.keys(), key=int):
		print(key,':', specs[key])


def print_path(path):
	if not path:
		print(path)
		return
	indent = 0
	for part in path.split('('):
		print('{}{}('.format(' '*indent, part))
		if ')' in part:
			indent -= 4 * (part.count(')')-1)
		else:
			indent += 4
	

# Part 1 - assumed ordered spec
#  uh... hit my 32Gbs or RAM trying to pre-compute all possibilities...
#  handled 1-symbol case incorrectly after quickly adding it
# Part 2 - 376 @ 10:00 - too high? (20min break at ~8:00)
if __name__ == '__main__':
	lines = [line.strip() for line in fileinput.input()]
	print('Lines: {}'.format(len(lines)))

	sections = grouped(lines)
	raw_spec = next(sections)
	input = next(sections)

	specs = {}
	for idx, spc in enumerate(raw_spec):
		id, val = spc.split(': ')
		specs[id] = val
	# Part 2
	# # 31 and 42 match only lengths of 5
	# # rules no longer greedy?
	# # matches only length multiples of 5
	# specs['8'] = '42 | 42 8'
	# # matches only length multiples of 10, always the same number of 42s and then 31s
	# specs['11'] = '42 31 | 42 11 31'
	print_specs(specs)

	# input = ['aaaabbaaaabbaaa']
	# input = ['bbabbbbaabaabba']

	matches = 0
	for idx, line in enumerate(input):
		# if matches_spec(final_spec, line):
		# if matches_spec(specs, line):
		match_len, max_path = matches_rec(specs, line, specs['0'])
#		print_path(max_path)
		if match_len == len(line):
			print('---', match_len,'/',len(line), line)
			matches += 1
		# if idx == 2:
		# 	exit()
	print(matches)

	# print_specs(specs)
