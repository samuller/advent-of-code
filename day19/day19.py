#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("..")
from lib import *
import re


def matches_spec(spec, input):
	possible_values = spec.split('|')
	if input in possible_values:
		return True
	return False


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
	print(sorted(specs.keys(), key=int, reverse=True))
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


# Part 1 - uh... hit my 32Gbs or RAM trying to pre-compute all possibilities...
if __name__ == '__main__':
	lines = [line.strip() for line in fileinput.input()]
	print('Lines: {}'.format(len(lines)))

	sections = grouped(lines)
	raw_spec = next(sections)
	input = next(sections)

	print(raw_spec)
	specs = {}
	for idx, spc in enumerate(raw_spec):
		id, val = spc.split(': ')
		specs[id] = val
		# assert int(id) == idx, id
		# specs.append(val)
	print(specs)
	specs = replace_literals(specs)
	print(specs)
	specs = replace_rules(specs)
	print(specs)
	final_spec = specs['0'].replace(' ','')
	print(final_spec)

	matches = 0
	for line in input:
		if matches_spec(final_spec, line):
			matches += 1
	print(matches)
