#!/usr/bin/env python
import itertools

input_file = open('input.txt','r')
# lines = input_file.readlines()
nums = [int(line.strip()) for line in input_file]
#print(nums)

# Part 1

nums = set(nums)
perms = itertools.permutations(nums, 2)
#print(list(perms))
for perm in perms:
	if sum(perm) == 2020:
 		print(perm)
 		print(perm[0] * perm[1])

# Part 2

perms = itertools.permutations(nums, 3)
for perm in perms:
	if sum(perm) == 2020:
		print(perm)
		print(perm[0] * perm[1] * perm[2])

