#!/usr/bin/env python
import itertools

input_file = open('input.txt','r')
# lines = input_file.readlines()
nums = [int(line.strip()) for line in input_file]
#print(nums)

# Part 1

nums = set(nums)
combs = itertools.combinations(nums, 2)
#print(list(perms))
for comb in combs:
	if sum(comb) == 2020:
 		print(comb)
 		print(comb[0] * comb[1])

# Part 2

combs = itertools.combinations(nums, 3)
for comb in combs:
	if sum(comb) == 2020:
		print(comb)
		print(comb[0] * comb[1] * comb[2])

