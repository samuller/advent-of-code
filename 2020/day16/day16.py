#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("..")
from lib import *


def is_number_valid(constraints, number):
	rng_used = []
	for valid_ranges in constraints:
		_, optional_rngs = valid_ranges
		# valid = False
		for rng in optional_rngs:
			# print('considering', number, 'for rule', rng)
			if rng[0] <= number <= rng[1]:
				# print(number, 'is True because of', rng)
				return True, None
	# print(number, 'is False')
	return False, number


def all_numbers_valid(constraint, numbers):
	for n in numbers:
		valid, _ = is_number_valid([constraint], n)
		if not valid:
			return False
	return True


def ticket_is_valid(constraints, ticket_values):
	for n in ticket_values:
		valid, reason_num = is_number_valid(constraints, n)
		if not valid:
			return False, reason_num
	return True, None


def max_length(list_of_lists):
	return max([len(l) for l in list_of_lists])


def parse_constraints(lines):
	line_idx = 0
	constraints = []
	for line_idx, line in enumerate(lines):
		if line.strip() == '':
			break
		field_name, valid_values = line.split(': ')
		valid_ranges = [[int(r) for r in rng.split('-')] for rng in valid_values.split(' or ')]
		constraints.append((field_name, valid_ranges))
		# print(field_name, valid_ranges)
	return constraints


def get_valid_tickets(other_tickets):
	other_valid_tickets = []
	ticker_scanning_error_rate = 0
	for ticket in other_tickets:
		valid, invalid_num = ticket_is_valid(constraints, ticket)
		# print(curr_ticket, valid, invalid_num)
		# Part 1
		if not valid:
			ticker_scanning_error_rate += invalid_num
		else:
			other_valid_tickets.append(ticket)
	return other_valid_tickets, ticker_scanning_error_rate


def get_values_per_field(other_valid_tickets):
	num_of_fields = len(other_valid_tickets[0])
	all_field_values = [[] for _ in other_valid_tickets[0]]
	for ticket in other_valid_tickets:
		assert len(ticket) == num_of_fields
		for idx, n in enumerate(ticket):
			all_field_values[idx].append(n)
	return all_field_values


def get_all_valid_constraints_per_field(all_field_values, constraints):
	valid_cons = [[] for _ in range(len(all_field_values))]
	for idx, field_values in enumerate(all_field_values):
		# print(field_values)
		for con in constraints:
			if all_numbers_valid(con, field_values):
				con_name, _ = con
				valid_cons[idx].append(con_name)
	return valid_cons


def find_unique_valid_constraints(valid_cons):
	"""
	Assumes there is only one possible set of valid constraints, i.e.
	no two or more fields that could be confused with one another.
	This function will loop forever if that is the case (but an 'non-change'
	check would fix that).
	"""
	# pruning?
	only_valid_cons = [[] for _ in range(len(valid_cons))]
	while max_length(valid_cons) > 0:
		consider_field_idx = None
		consider_field = None
		for idx, field in enumerate(valid_cons):
			if len(field) == 1:
				consider_field_idx = idx
				consider_field = field[0]
				break
		assert consider_field_idx is not None, "Loop validation shouldn't allow this"
		# print(consider_field, consider_field_idx)
		only_valid_cons[consider_field_idx].append(consider_field)
		for idx in range(len(valid_cons)):
			if consider_field in valid_cons[idx]:
				valid_cons[idx].remove(consider_field)
	# print(valid_cons)
	return only_valid_cons


if __name__ == '__main__':
	lines = [line.strip() for line in fileinput.input()]
	print('Lines: {}'.format(len(lines)))

	sections = grouped(lines)
	constraints = parse_constraints(next(sections))
	# print(constraints)

	curr_section = next(sections)
	assert curr_section[0].strip() == 'your ticket:'
	your_ticket = [int(n) for n in curr_section[1].split(',')]
	# print(your_ticket)

	curr_section = next(sections)
	assert curr_section[0].strip() == 'nearby tickets:'
	other_tickets = [[int(n) for n in line.split(',')] for line in curr_section[1:]]
	other_valid_tickets, ticker_scanning_error_rate = get_valid_tickets(other_tickets)

	# Part 1
	print(ticker_scanning_error_rate)

	# Part 2
	all_field_values = get_values_per_field(other_valid_tickets)
	valid_cons = get_all_valid_constraints_per_field(all_field_values, constraints)
	only_valid_cons = find_unique_valid_constraints(valid_cons)
	final_field_names = [cons[0] for cons in only_valid_cons]

	prod = 1
	for idx, field in enumerate(final_field_names):
		if field.startswith('departure'):
			prod *= your_ticket[idx]
			# print(your_ticket[idx])
	print(prod)
