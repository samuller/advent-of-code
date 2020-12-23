#!/usr/bin/env python3
import fileinput
import cProfile
# import sys; sys.path.append("..")
# from lib import *


class LinkedListNode:
	def __init__(self, val, next=None):
		self.val = val
		self.next = next
	
	def __str__(self):
		return '{} -> {}'.format(self.val, id(self.next))


class LinkedList:
	"""Linked-list that supports circular loops"""
	def __init__(self, start_node=None):
		if start_node is None:
			self.head = None
		else:
			assert type(start_node) == LinkedListNode
			self.head = start_node

	def is_circular(self):
		return self.get_tail_before_head() is not None

	def iterate(self, start=None):
		if start is None:
			start = self.head
		if start is None:
			return
		yield start

		curr = start.next
		while curr not in [None, start]:
			yield curr
			curr = curr.next

	def get_size(self):
		if self.head is None:
			return 0
		count = 0
		for node in self.iterate():
			count += 1
		return count

	def get_tail(self):
		for node in self.iterate():
			if node.next in [None, self.head]:
				return node
		return None

	def get_tail_before_head(self):
		for node in self.iterate():
			if node.next == self.head:
				return node
		return None

	def add_after(self, val, node_before=None):
		new_node = LinkedListNode(val)
		if node_before is None:
			self.head = new_node
		else:
			node_before.next = new_node
		return new_node

	def make_circular(self):
		self.get_tail().next = self.head

	def find_before(self, val):
		"""Finds first node before node with value"""
		for node in self.iterate():
			next = node.next
			if next is not None and next.val == val:
				return node
		return None

	def remove_section(self, before_start_node, count):
		# assert count < self.get_size(), '{} >= {}'.format(count, self.get_size())
		# print('Moving {}'.format(before_start_node.val))
		section_start = before_start_node.next
		before_start_node.next = None

		curr_section = section_start
		if curr_section == self.head:
				self.head = self.head.next
				# print('Move first head to {}'.format(self.head.val))
		section_size = 1
		while curr_section is not None and section_size < count:
			section_size += 1
			curr_section = curr_section.next
			if curr_section == self.head:
				self.head = self.head.next
				# print('Move head to {}'.format(self.head.val))
		section_end = curr_section

		before_start_node.next = section_end.next
		section_end.next = None
		return LinkedList(section_start)

	def insert_section(self, insert_after_node, section):
		assert not section.is_circular()
		after_section = insert_after_node.next
		insert_after_node.next = section.head
		section.get_tail().next = after_section

	def to_list(self):
		listy = []
		for node in self.iterate():
			listy.append(node.val)
		return listy

	def __str__(self):
		status = '@' if self.is_circular() else ''  # ↻
		return str(self.to_list()) + status


def dict_to_nodes(linked_list):
	dicty = {}
	for node in linked_list.iterate():
		dicty[node.val] = node
	return dicty


def list_to_circular_linked_list(listy):
	ll = LinkedList()
	tail = None
	for val in listy:
		tail = ll.add_after(val, node_before=tail)
	ll.make_circular()
	return ll


def pickup(cups, curr_idx, start_offset=1, count=3):
	# print('start pickup')
	assert count < len(cups)
	A = cups[curr_idx + start_offset:]
	new_cups = cups[:curr_idx + start_offset]
	if (curr_idx + start_offset) > len(cups):
		A = cups[(curr_idx + start_offset) % len(cups):]
		new_cups = cups[:(curr_idx + start_offset) % len(cups)]
	# print(new_cups,A,count > len(A))
	if count > len(A):
		# assert count / len(A) < 2
		# assert count % len(A) < len()
		count_extra = count - len(A)
		A.extend(cups[:count_extra])
		new_cups = new_cups[count_extra:curr_idx+1]
		new_curr_idx = curr_idx - count_extra
	else:
		for a in A[count:]:
			new_cups.append(a)
		A = A[:count]
		new_curr_idx = curr_idx
	# cups/remaining, picked-up
	return new_cups, A, new_curr_idx
assert pickup([3,8,9,1,2,5,4,6,7],0,1,3) == ([3,2,5,4,6,7], [8,9,1],0)
assert pickup([8,3,6,7,4,1,9,2,5],7,1,3) == ([6,7,4,1,9,2], [5,8,3],5), pickup([8,3,6,7,4,1,9,2,5],7,1,3)
assert pickup([7,4,1,5,8,3,9,2,6],8,1,3) == ([5,8,3,9,2,6], [7,4,1],5), pickup([8,3,6,7,4,1,9,2,5],7,1,3)


def place_right(cups, picked_up, dest_cup_idx):
	cups = cups[:dest_cup_idx+1] + picked_up + cups[dest_cup_idx+1:]
	return cups
assert place_right([3,2,5,4,6,7], [8,9,1], 1) == [3,2,8,9,1,5,4,6,7]
# Move 4?  [7,2,5,8,9,1,3,4,6], print-out rotates such that next cup is one index further
assert place_right([3,2,5,8,9,1], [4,6,7], 0) == [3,4,6,7,2,5,8,9,1], place_right([3,2,5,8,9,1], [4,6,7], 0)


def part1(cups, rounds=100, start_idx=0):
	min_cup_lbl = min(cups)
	max_cup_lbl = max(cups)
	curr_cup_idx = start_idx
	for round in range(rounds):
		curr_cup_lbl = cups[curr_cup_idx]
		cups, picked_up, curr_cup_idx = pickup(cups, curr_cup_idx, start_offset=1, count=3)
		curr_cup_idx = cups.index(curr_cup_lbl)
		assert curr_cup_lbl == cups[curr_cup_idx]
		# print(picked_up)
		dest_cup_lbl = cups[curr_cup_idx]-1
		if dest_cup_lbl < min_cup_lbl:
				dest_cup_lbl = max_cup_lbl
		while dest_cup_lbl in picked_up:
			dest_cup_lbl -= 1
			if dest_cup_lbl < min_cup_lbl:
				dest_cup_lbl = max_cup_lbl
		# print(dest_cup_lbl)
		cups = place_right(cups, picked_up, cups.index(dest_cup_lbl))
		curr_cup_idx = cups.index(curr_cup_lbl)
		### print(cups, cups[curr_cup_idx])
		curr_cup_idx = (curr_cup_idx + 1) % len(cups)
		print(cups, cups[curr_cup_idx])
	idx = cups.index(1)
	# Part 1
	print()
	ans = cups[idx+1:] + cups[:idx]
	print(ans)
	ans = ''.join([str(c) for c in ans])
	print(ans)


def part2(cups, rounds=10_000_000, start_idx=0, add_mil=True):
	"""
	If numbers are monotonically increasing (first few passes):
	   then idx jumps by 4 and all numbers visited will always be right before idx
	   until the near the end
	If 
	"""
	# Part 2
	prev_max = max(cups)
	if add_mil:
		cups = cups + list(range(max(cups)+1,1_000_000))

	min_cup_lbl = min(cups)
	max_cup_lbl = max(cups)
	curr_cup_idx = start_idx
	skip_a_few = False
	track_cups = []
	track_cups_set = set()
	# Part 2: 100 -> 10000000
	for round in range(rounds):
		if round % 100_000 == 0:
			print('At round ' + str(round))
		curr_cup_lbl = cups[curr_cup_idx]
		if 9 <= curr_cup_idx < (len(cups) - 6):
			skip_a_few = True
			track_cups.append(curr_cup_lbl)
			track_cups_set.add(curr_cup_lbl)
			curr_cup_idx = (curr_cup_idx + 4) % len(cups)
			print(cups[curr_cup_idx])
			continue
		else:
			# print('skip_a_few recovery...')
			if skip_a_few:
				# Remove track_cups values
				cups = [c for c in cups if c not in track_cups_set]
				# print(cups, track_cups)
				# Idx is temporarily incorrect since we've removed cups
				cups = cups[:curr_cup_idx-len(track_cups)] + track_cups + \
					cups[curr_cup_idx-len(track_cups):]
			track_cups = []
			track_cups_set = set()
			skip_a_few = False
		cups, picked_up, curr_cup_idx = pickup(cups, curr_cup_idx, start_offset=1, count=3)
		curr_cup_idx = cups.index(curr_cup_lbl)
		assert curr_cup_lbl == cups[curr_cup_idx]
		# print(picked_up)
		dest_cup_lbl = cups[curr_cup_idx]-1
		if dest_cup_lbl < min_cup_lbl:
				dest_cup_lbl = max_cup_lbl
		while dest_cup_lbl in picked_up:
			dest_cup_lbl -= 1
			if dest_cup_lbl < min_cup_lbl:
				dest_cup_lbl = max_cup_lbl
		# print(dest_cup_lbl)
		cups = place_right(cups, picked_up, cups.index(dest_cup_lbl))
		curr_cup_idx = cups.index(curr_cup_lbl)
		### print(cups, cups[curr_cup_idx])
		curr_cup_idx = (curr_cup_idx + 1) % len(cups)
		# print(round, cups[curr_cup_idx], curr_cup_idx)
		print(cups, cups[curr_cup_idx])
	print(1+round, cups[curr_cup_idx], curr_cup_idx)
	idx = cups.index(1)
	print(cups[(idx+1) % len(cups)], cups[(idx+2) % len(cups)])
	print(cups[(idx+1) % len(cups)] * cups[(idx+2) % len(cups)])


def part2_linked(cups, rounds=10_000_000):
	# Round 2
	cups = cups + list(range(max(cups)+1,1_000_000+1))
	assert len(cups) == 1_000_000

	min_cup = min(cups)
	max_cup = max(cups)
	cups = list_to_circular_linked_list(cups)
	all_nodes = dict_to_nodes(cups)
	# exit()
	# print(cups)
	curr_cup = cups.head
	# Part 2: 100 -> 10_000_000
	print('Starting')
	for i in range(rounds):
		if i % (rounds/10) == 0:
			print('At round {} %'.format(round(i/rounds*100)))
		picked_up = cups.remove_section(before_start_node=curr_cup, count=3)
		picked_up_list = picked_up.to_list()
		assert len(picked_up_list) == 3

		dest_val = curr_cup.val - 1
		if dest_val < min_cup:
			dest_val = max_cup
		while dest_val in picked_up_list:
			dest_val -= 1
			if dest_val < min_cup:
				dest_val = max_cup

		# print(picked_up_list, '->',dest_val)
		# print(cups)
		# dest_node = cups.find_before(dest_val).next
		dest_node = all_nodes[dest_val]
		cups.insert_section(dest_node, picked_up)

		curr_cup = curr_cup.next
		# print(curr_cup.val, cups)  #, picked_up_list, dest_val)
		# print(cups, curr_cup.val)
	print()
	# Part 1
	# node_1 = cups.find_before(1).next
	# ans = ''
	# for node in cups.iterate(start=node_1.next):
	# 	if node != node_1:
	# 		ans += str(node.val)
	# print(ans)
	# Part 2
	node_1 = all_nodes[1]
	print(node_1.next.val, node_1.next.next.val)
	print(node_1.next.val * node_1.next.next.val)


# Part 2: 1480 @ 8:40 (too low), didn't use linked list in Part 1
def main():
	lines = [line.strip() for line in fileinput.input()]
	print('Lines: {}'.format(len(lines)))

	cups = [int(l) for l in lines[0]]
	print(cups)

	part2_linked(cups)
	# cProfile.run('part2_linked(cups)')
	# cProfile.runctx('part2_linked(cups)', globals(), locals(), 'restats')
	# import pstats
	# p = pstats.Stats('restats')
	# p.strip_dirs().sort_stats('cumulative').print_stats()

	# part1(list(range(1, 40)), 20, 9)
	# part2(list(range(1, 40)), 20, 9, False)
	
	# part1(cups)
	# Part 2
	# part2(cups)


if __name__ == '__main__':
	main()
