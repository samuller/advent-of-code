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
	assert old_r == 1, 'greatest common divisor = ' + old_r
	if old_s < 0:
		old_s += b
	return old_s

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
	bus_offsets = {}
	for offset, bus in enumerate(busses):
		if bus != 'x':
			# bus_offsets.append((offset, int(bus)))
			bus_offsets[offset] = int(bus)
	# print(bus_offsets)
	# print(bus_offsets.items())
	
	M = prod(list(bus_offsets.values()))
	x = 0
	for a_i, m_i in bus_offsets.items():
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
	print(M - (x % M))
	return M - (x % M)
	# exit()

	# (17x - 0) == (13y - 2) == (19z - 3)

	# x,y,z = 201,263,180
	#           == 2 + 4y
	#
	# 17, 34, 51, 68, 85, 102
	# 13, 26, 39, 52, 65, 78
	# 19, 38, 57
	#
	# 2 * 13 - 17 = 9
	# (17-13) + 13x = 4 + 13x
	# 2 * 17 - 2 * 13 = 2 * (17-13) = 8
	#
	# 3 * 17 - 2 * 13 =  25
	# 17x - 13y = 25
	# 17x - 25 = 13y
	# (17x - 25)/13 = y
	# 17/13 x - 25/13 = y
	# 1.5x = y
	#
	# 17x == 13y - 2
	# 2 == (17-13) + 13u = 4 + 13u = 
	#
	# 17,x,13,19 -> 3417 (201,x,263,180)
	# diff: 0,x,-4,2
	# idx:  0,x,2,3
	# 0,x,-8,6
	#
	# 
	# 19 * 180 = 3420
	# 17 * 180 = 3060
	#             360  (360 / 2 = 180)
	# 201 = 1, 3, 67, 201
	# 263 = 1, 263
	# 180 = 1, 2, 3, 4, 5, 6, 9, 10, 12, 15, 18, 20, 30, 36, 45, 60, 90, 180
	# 3417 = 1, 3, 17, 51, 67, 201, 1139, 3417
	for offset, bus in bus_offsets.items():
		offset
	# for i in range(10000000):
	# 	invalid = False
	# 	for offset, bus in bus_offsets: 
	# 		if (i + offset) % bus != 0:
	# 			invalid = True
	# 	if not invalid:
	# 		return i
	return None

# 5057105 @ 07:16, 640856202464571 @ 10:23
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

	lines = [line.strip() for line in fileinput.input('input.txt')]
# 	test1 = """939
# 7,13,x,x,59,x,31,19"""
	tests = ["7,13,x,x,59,x,31,19", "17,x,13,19", "67,7,59,61", "67,x,7,59,61",
			 "67,7,x,59,61", "1789,37,47,1889"]
	test_ans = [1068781, 3417, 754018, 779210, 1261476, 1202161486]
	for idx, test in enumerate(tests):
		busses = test.split(',')
		calc = calc_time(busses)
		print(calc)
		assert calc == test_ans[idx], idx
# 	exit()

	# test_idx = None
	# if test_idx is not None:
	# 	lines = test[test_idx].split('\n')
	print('Lines: {}'.format(len(lines)))

	busses = lines[1].split(',')
	print(calc_time(busses))
	exit()

	busses = [int(b) for b in busses if b != 'x']
	print(busses)
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
		print(b, ':', bus_earliest)
		if first_time is None or bus_earliest < first_time:
			first_bus = b
			first_time = bus_earliest

	print(first_time, '= +', first_time - time)
	print(first_bus * (first_time - time))

	# sched = lines[1].split(',')
	# print(sched)
	# schedules = []
	# curr_sched = []
	# for s in sched:
	# 	if s[0] in '0123456789':
	# 		schedules.append(curr_sched)
	# 		curr_sched = [int(s)]
	# 	else:
	# 		curr_sched.append(s)
	# schedules.remove([])
	# print(schedules)
