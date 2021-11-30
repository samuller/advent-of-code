#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("..")
from lib import *


# https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode
def extended_gcd(a, b):
	# print('extended_gcd',a,b)
	(old_r, r) = (a, b)
	(old_s, s) = (1, 0)
	(old_t, t) = (0, 1)

	while r != 0:
		quotient = old_r // r
		(old_r, r) = (r, old_r - quotient * r)
		(old_s, s) = (s, old_s - quotient * s)
		(old_t, t) = (t, old_t - quotient * t)
    
	# print("Bézout coefficients:", (old_s, old_t))
	# print("quotients by the gcd:", (t, s))
	assert old_r == 1, 'greatest common divisor = {}'.format(old_r)
	if old_s < 0:
		old_s += b
	return old_s


def confirm_value(busses, value):
	invalid = False
	for offset, bus in busses.items(): 
		if (value + offset) % bus != 0:
			invalid = True
	return not invalid


def calc_time_slow(busses):
	for i in range(1000000000000000):
		if confirm_value(busses, i):
			return i
	return None


# Based on:
# https://www.reddit.com/r/adventofcode/comments/kc60ri/2020_day_13_can_anyone_give_me_a_hint_for_part_2/gfnnfm3/?utm_source=reddit&utm_medium=web2x&context=3
# https://paste.debian.net/plainh/f6796bee
def calc_time_fast(busses):
	curr_value = 0
	bus_list = list(busses.items())
	curr_offset, curr_bus = bus_list[0]
	curr_busses = { curr_offset: curr_bus }
	for idx, (next_offset, next_bus) in enumerate(bus_list[1:]):
		M = prod(list(curr_busses.values()))
		while True:
			curr_value += M
			curr_busses[next_offset] = next_bus
			if confirm_value(curr_busses, curr_value):
				break
	return curr_value


# Chinese remainder theorem @ 9:03
# 0 mod 17
# 2 mod 13
# 3 mod 19
# 13*17*19 = 4199
# 0*(13*19)*(...) + 2*(17*19)*(17*19 mod 13) + 3*(17*13)*(17*13 mod 19)
# = 2*323* 6 + 3*221* 8
# = 3876 + 5304 = 9180
# 9180 mod 4199
# = 782
# = 4199-3417 ?
# != 3417
def calc_time(busses):
	M = prod(list(busses.values()))
	x = 0
	for a_i, m_i in busses.items():
		# print(a_i, m_i)
		b_i = M/m_i
		# The multiple of b_i that gives 1 in mod m_i space
		b_i_inv = extended_gcd(b_i, m_i)
		assert b_i_inv > 0
		assert (b_i_inv * b_i) % m_i == 1
		b_i_prime = b_i_inv # % m_i
		# print(a_i, b_i, b_i_prime)
		x += a_i * b_i * b_i_prime
	print(x, M)
	# print(extended_gcd(x, M))
	answer = int(M - (x % M))
	# answer = abs(int((x % M) - M))
	# print(answer)
	assert confirm_value(busses, answer), answer
	return answer


def bus_dict(bus_list):
	bus_offsets = {}
	for offset, bus in enumerate(bus_list):
		if bus != 'x':
			bus_offsets[offset] = int(bus)
	return bus_offsets


def run_tests(lines):
	for idx, line in enumerate(lines):
		ans, input = line.split('\t')
		ans = int(ans)
		busses = bus_dict(input.split(','))
		calc = calc_time_fast(busses)
		print(calc)
		assert calc == ans, 'failed test {} with {} instead of {}'.format(idx, calc, ans)


# 5057105 @ 07:16, 640856202464571 @ 10:23, 11:34
if __name__ == '__main__':
	# extended_gcd(8400,11)
	# assert extended_gcd(8400,11) == 8
	# assert extended_gcd(5775,16) == 15
	# assert extended_gcd(4400,21) == 2
	# assert extended_gcd(3696,25) == 6
	# print(calc_time("x,x,5,7".split(',')))
	# http://homepages.math.uic.edu/~leon/mcs425-s08/handouts/chinese_remainder.pdf
	# print(calc_time("x,x,x,x,x,x,11,x,x,21,x,x,x,16,x,x,x,x,x,25".split(',')))
	# print(calc_time("17,x,13,19".split(',')))
	# exit()

	lines = [line.strip() for line in fileinput.input()]
	print('Lines: {}'.format(len(lines)))
	if len(lines) != 2:
		run_tests(lines)
		print('Tests passed')
		exit()

	# Part 1
	time = int(lines[0])
	busses = [int(b) for b in lines[1].split(',') if b != 'x']
	# print(busses)
	first_time = None
	first_bus = None
	for b in busses:
		# print(time / b)
		first_time_on_or_before = int(time / b) * b
		# print(b, ':', first_time_on_or_before)
		if first_time_on_or_before == time:
			first_time = first_time_on_or_before
			first_bus = b
			break

		bus_earliest = first_time_on_or_before + b
		# print(b, ':', bus_earliest)
		if first_time is None or bus_earliest < first_time:
			first_bus = b
			first_time = bus_earliest

	# print(first_time, '= +', first_time - time)
	print(first_bus * (first_time - time))

	# Part 2
	busses = bus_dict(lines[1].split(','))
	# print(confirm_value(busses, 640856202464571))
	# print(confirm_value(busses, 640856202464541))
	print(calc_time_fast(busses))
