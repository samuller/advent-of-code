#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("..")
from lib import *
from collections import defaultdict
import itertools


def from_set(s):
	for e in s:
		return e


# Part 1: Took "The first step is to" literally...
# Part 2: determined final answer by hand at 8:02:
# dairy,eggs,fish,nuts,peanuts,sesame,soy,wheat
# vfvvnm,bvgm,rdksxt,xknb,hxntcz,bktzrz,srzqtccv,gbtmdb
def main():
	lines = [line.strip() for line in fileinput.input()]
	print('Lines: {}'.format(len(lines)))

	foods = []
	al_maybes = {}
	for line in lines:
		ingredients, allergens = line.split(' (contains ')
		ingredients = ingredients.split(' ')
		# These are only known allergens, there could be missing info
		# __Assumption__: all known allergens are always shown, others aren't known ever
		# Any ingredient only has 0 or 1 allergens
		# __Assumption__: even if allergen not in current line, it WOULD be
		# elsewhere in the list if the item has 1 allergen (also with the same allergen)
		# Test data:
		# - What about 'fvjkl'?
		allergens = allergens[:-1].split(', ')
		# print(ingredients, allergens)
		foods.append((ingredients, allergens))
		for al in allergens:
			if al not in al_maybes:
				al_maybes[al] = set(ingredients)
			else:
				al_maybes[al] = al_maybes[al].intersection(set(ingredients))

	print('Possible allergen ingredients:')
	print_dict(al_maybes)

	# for idx, food in enumerate(foods):
	# 	ing, ale = food
	# 	print(list(itertools.product(ing, ale)))

	# Prune dict
	removed = True
	while removed:
		removed = False
		for al, ings in al_maybes.items():
			# If there's only 1 option, we know it's valid
			if len(ings) <= 1:
				the_ing = from_set(ings)
				# Remove from other
				for al2, ings2 in al_maybes.items():
					if al == al2:
						continue
					if the_ing in ings2:
						removed = True
						ings2.remove(the_ing)
	
	print('Pruned allergen list:')
	print_dict(al_maybes)

	# There could still be unknown/multi-option allergen ingredients,
	# but we assume their definitely allergenic (just unsure about which)
	known_allergen_ings = set()
	for ale, ing in al_maybes.items():
		for i in ing:
			known_allergen_ings.add(i)

	allergen_free = set()
	for idx, food in enumerate(foods):
		ingredients, allergens = food
		no_aller = set(ingredients) - known_allergen_ings
		for i in no_aller:
			allergen_free.add(i)
	print('Allergen free:')
	print(allergen_free)
	print()

	count = 0
	for food in foods:
		ingredients, allergens = food
		for free in allergen_free:
			if free in ingredients:
				count += 1
	print(count)

	danger = []
	for v in sorted(al_maybes.keys()):
		danger.append(from_set(al_maybes[v]))
	print(','.join(danger))

if __name__ == '__main__':
	main()
