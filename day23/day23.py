#!/usr/bin/env python3
import fileinput
import cProfile


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


def play_cups(cups, rounds=100, add_mil=False, part2=False):
	if add_mil:
		cups = cups + list(range(max(cups)+1,1_000_000+1))
		assert len(cups) == 1_000_000

	min_cup = min(cups)
	max_cup = max(cups)
	cups = list_to_circular_linked_list(cups)
	# print(cups)
	all_nodes = dict_to_nodes(cups)
	curr_cup = cups.head
	for i in range(rounds):
		if part2 and i % (rounds/10) == 0:
			print('Part 2 in progress: {} %'.format(round(i/rounds*100)))
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

		dest_node = all_nodes[dest_val]
		cups.insert_section(dest_node, picked_up)
		curr_cup = curr_cup.next
		# print(cups, curr_cup.val)
	print()
	if not part2:
		node_1 = cups.find_before(1).next
		ans = ''
		for node in cups.iterate(start=node_1.next):
			if node != node_1:
				ans += str(node.val)
		print(ans)
	else:
		node_1 = all_nodes[1]
		print(node_1.next.val, node_1.next.next.val)
		print(node_1.next.val * node_1.next.next.val)


# Part 2: 1480 @ 8:40 (too low)
# - looked for some patterns that can be optimized, e.g.:
#    part1(list(range(1, 40)), 20, 9)
#    part2(list(range(1, 40)), 20, 9, False)
# 	If numbers are monotonically increasing (first few passes):
#    then idx jumps by 4 and all numbers visited will always be right before idx
#    until the near the end
# - but once numbers become mixed up, i.e. after a few passes, no more patterns remain?
# - didn't use linked list in Part 1
# - needed to optimize more by removing assert that was confirming sizes (by counting whole list)
# - and using dict to find values in linked list
def main():
	lines = [line.strip() for line in fileinput.input()]
	print('Lines: {}'.format(len(lines)))

	cups = [int(l) for l in lines[0]]
	print(cups)

	play_cups(cups, rounds=100)
	play_cups(cups, rounds=10_000_000, add_mil=True, part2=True)

	# Performance profiling
	# cProfile.runctx('play_cups(cups)', globals(), locals(), 'restats')
	# import pstats
	# p = pstats.Stats('restats')
	# p.strip_dirs().sort_stats('cumulative').print_stats()


if __name__ == '__main__':
	main()
