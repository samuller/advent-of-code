#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("..")
from lib import *
import re



def matches_rec(specs, input, root_spec): #spec_key='0'):
	# print(input, root_spec)
	# root_spec = specs[spec_key]
	# Base case
	if root_spec.startswith('"'):
		spec = root_spec[1:-1]
		if input.startswith(spec):
			return 1
		else:
			return 0

	longest_match = 0
	paths = root_spec.split(' | ')
	assert len(paths) <= 2, paths
	for path in paths:
		symbols = path.split(' ')
		if len(symbols) == 1:
			chars_matching = matches_rec(specs, input, specs[symbols[0]])
			longest_match = max(longest_match, chars_matching)
			continue
		assert len(symbols) == 2, symbols
		sym1, sym2 = symbols

		n = matches_rec(specs, input, specs[sym1])
		chars_matching = n
		if n == 0:
			continue
		# Else continue to symbol 2
		n2 = matches_rec(specs, input[n:], specs[sym2])
		chars_matching += n2
		# if chars_matching == len(input):
		# 	return chars_matching

		longest_match = max(longest_match, chars_matching)

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
			specs[key] = specs[key].replace(str(lit_key), lit_val)
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


# Part 1 - assumed ordered spec
#  uh... hit my 32Gbs or RAM trying to pre-compute all possibilities...
#  handled 1-symbol case incorrectly after quickly adding it
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
	# print(specs)


	matches = 0
	for idx, line in enumerate(input):
		# if matches_spec(final_spec, line):
		# if matches_spec(specs, line):
		match_len = matches_rec(specs, line, specs['0'])
		# print('---', match_len,'/',len(line), line)
		if match_len == len(line):
			matches += 1
		# if idx == 2:
		# 	exit()
	print(matches)
