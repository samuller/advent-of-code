#!/usr/bin/env python3
import fileinput
# import sys; sys.path.append("..")
# from lib import *


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


if __name__ == '__main__':
	lines = [line.strip() for line in fileinput.input()]
	print('Lines: {}'.format(len(lines)))

	line_idx = 0
	constraints = []
	for line_idx, line in enumerate(lines):
		if line.strip() == '':
			break
		field_name, valid_values = line.split(': ')
		valid_ranges = [[int(r) for r in rng.split('-')] for rng in valid_values.split(' or ')]
		constraints.append((field_name, valid_ranges))
		# print(field_name, valid_ranges)
	
	line_idx += 1
	assert lines[line_idx].strip() == 'your ticket:'

	line_idx += 1
	your_ticket = [int(n) for n in lines[line_idx].split(',')]
	# print(your_ticket)
	
	line_idx += 2
	assert lines[line_idx].strip() == 'nearby tickets:', lines[line_idx]

	line_idx += 1
	other_valid_tickets = []
	ticker_scanning_error_rate = 0
	for idx in range(line_idx, len(lines)):
		if lines[idx].strip() == '':
			break

		curr_ticket = [int(n) for n in lines[idx].split(',')]
		valid, invalid_num = ticket_is_valid(constraints, curr_ticket)
		# print(curr_ticket, valid, invalid_num)
		# Part 1
		if not valid:
			ticker_scanning_error_rate += invalid_num
		else:
			other_valid_tickets.append(curr_ticket)
	print(ticker_scanning_error_rate)

	# Part 2
	num_of_fields = len(other_valid_tickets[0])
	all_field_values = [[] for _ in other_valid_tickets[0]]
	# print(other_valid_tickets[0])
	# print(all_field_values)
	for ticket in other_valid_tickets:
		assert len(ticket) == num_of_fields
		for idx, n in enumerate(ticket):
			all_field_values[idx].append(n)
		# print(ticket)
		# print(all_field_values)

	valid_cons = [[] for _ in range(len(all_field_values))]
	for idx, field_values in enumerate(all_field_values):
		# print(field_values)
		for con in constraints:
			if all_numbers_valid(con, field_values):
				con_name, _ = con
				valid_cons[idx].append(con_name)
	
	# pruning?
	only_valid_cons = [[] for _ in range(len(valid_cons))]
	while max_length(valid_cons) > 1:
		consider_field_idx = None
		consider_field = None
		for idx, field in enumerate(valid_cons):
			if len(field) == 1:
				consider_field_idx = idx
				consider_field = field[0]
				break
		if consider_field_idx is None:
			print('Done?')
			break
		# print(consider_field, consider_field_idx)
		only_valid_cons[consider_field_idx].append(consider_field)
		for idx in range(len(valid_cons)):
			# if idx == consider_field_idx:
			# 	continue
			# print(consider_field)
			# print(valid_cons[idx])
			if consider_field in valid_cons[idx]:
				valid_cons[idx].remove(consider_field)
	# print(valid_cons)
	# Add last field
	for idx in range(len(valid_cons)):
		if len(valid_cons[idx]) == 1:
			only_valid_cons[idx].append(valid_cons[idx][0])
	# print(only_valid_cons)

	final_field_names = [cons[0] for cons in only_valid_cons]
	print(final_field_names)
	prod = 1
	print(your_ticket)
	for idx, field in enumerate(final_field_names):
		if field.startswith('departure'):
			prod *= your_ticket[idx]
			print(your_ticket[idx])
	print(prod)
