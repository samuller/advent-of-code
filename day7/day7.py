#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("..")
from lib import *


def look_for(input, iwant, known_containers=None):
	# print('look_for( input,', iwant + ',', known_containers, ')')
	if known_containers is None:
		known_containers = set()

	containers = set()
	for line in input:
		line = line.replace(' bags.', '')
		line = line.replace(' bags', '')
		line = line.replace(' bag', '')

		fields = line.split(' contain ')
		assert len(fields) == 2, fields
		big, inside = fields

		inside = inside.split(', ')
		inside = [
			(int(ins.split(' ')[0]) if ins.split(' ')[0] != 'no' else 0,
				' '.join(ins.split(' ')[1:])
			) for ins in inside
		]
		counts = [int(ins[0]) if ins[0] != 'no' else 0 for ins in inside]
		# print(inside)

		# assert len(inside) == 2, len(inside)
		#if  big == iwant
		for ins in inside:
			if iwant in ins[1]:
				containers.add(big)
				# print()
				# print(ins)
				# print(big)
				# print(inside)
				# print(counts)
				# print()
	if len(containers) == 0:
		return []
	# print(len(known_containers))
	# print(containers)
	# print(known_containers)
	for new_want in containers:
		super_containers = look_for(input, new_want, containers)
		containers = containers.union(super_containers)
	return containers


def count_inside(input, look_inside):
	# print()
	# print('look_for( input,', look_inside, ')')

	containers = set()
	total_count = 0
	bigs = set()
	for line in input:
		line = line.replace(' bags.', '')
		line = line.replace(' bags', '')
		line = line.replace(' bag.', '')
		line = line.replace(' bag', '')

		fields = line.split(' contain ')
		assert len(fields) == 2, fields
		big, inside = fields

		inside = inside.split(', ')
		inside = [
			(int(ins.split(' ')[0]) if ins.split(' ')[0] != 'no' else 0,
				' '.join(ins.split(' ')[1:])
			) for ins in inside
		]
		counts = [int(ins[0]) if ins[0] != 'no' else 0 for ins in inside]
		if big == look_inside:
			total_count += sum(counts)
			for ins in inside:
				if ins[0] > 0:
					containers.add(ins)
		assert big not in bigs, big
		bigs.add(big)

	for inss in containers:
		count = inss[0]
		new_look = inss[1]
		sub_count = count_inside(input, new_look)
		# print(look_inside, total_count, '+ (', sub_count, '*', count, new_look, ')')
		total_count += (count * sub_count)
	# print(look_inside, 'total:', total_count)
	return total_count


# 93873 @ 7:50, 158493 @ 8:12
# forgot "bag."
if __name__ == '__main__':
	lines = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""
# 	lines = """shiny gold bags contain 2 dark red bags.
# dark red bags contain 2 dark orange bags.
# dark orange bags contain 2 dark yellow bags.
# dark yellow bags contain 2 dark green bags.
# dark green bags contain 2 dark blue bags.
# dark blue bags contain 2 dark violet bags.
# dark violet bags contain no other bags."""
	lines = lines.split('\n')
	lines = [line.strip() for line in fileinput.input('input.txt')]
	print('Lines: {}'.format(len(lines)))

	iwant = 'shiny gold'
	needs = look_for(lines, iwant)
	print('Bags containing:', len(needs))

	min_bags_needed = count_inside(lines, iwant)
	print('Bags inside:', min_bags_needed)
