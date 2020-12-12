#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("..")
from lib import *
import math


def rotate90s(point, degree):
	# 90 degree rotations basically swap the x-y axes
	# and then negates one axis
	# +R -> +D -> -L -> -U, +D -> -L -> -U -> +R
	# -L -> +U -> +R -> +D, -U -> +R -> +D -> -L
	p1, p2 = point
	times = round(abs(degree) / 90)
	# print(p1, p2)
	for t in range(times):
		p1, p2 = p2, p1
		if degree > 0:
			p2 = -p2
		else:
			p1 = -p1
	return p1, p2
# (-4, 10) -> (10,_4) -> (4, _-10) -> (-10 ,_-4) -> (-4, 10)
assert rotate90s((-4, 10), 90) == (10, 4)
assert rotate90s((-4, 10), 180) == (4, -10)
assert rotate90s((-4, 10), 270) == (-10, -4)
assert rotate90s((-4, 10), 360) == (-4, 10)
assert rotate90s((-4, 10), -270) == (10, 4)
assert rotate90s((-4, 10), -180) == (4, -10)
assert rotate90s((-4, 10), -90) == (-10, -4)
assert rotate90s((-4, 10), -360) == (-4, 10)


def rotate(center, point, degree):
	degree = -degree
	angle = math.radians(degree)
	# https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python
	ox, oy = center
	px, py = point

	qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
	qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
	return int(round(qx)), int(round(qy))
assert rotate90s((-4, 10), 90) == rotate([0,0],(-4,10),90), \
	'{} != {}'.format(rotate90s((-4, 10), 90), rotate([0,0],(-4,10),90))
assert rotate90s((-4, 10), 180) == rotate([0,0],(-4,10),180), \
	'{} != {}'.format(rotate90s((-4, 10), 180), rotate([0,0],(-4,10),180))
assert rotate90s((-4, 10), 270) == rotate([0,0],(-4,10),270), \
	'{} != {}'.format(rotate90s((-4, 10), 270), rotate([0,0],(-4,10),270))
assert rotate90s((-4, 10), 90) == rotate([0,0],(-4,10),90), \
	'{} != {}'.format(rotate90s((-4, 10), 90), rotate([0,0],(-4,10),90))


def part1(lines):
	rc = (0,0) # (NS v, WE ->)
	facing = 90  # N = 0, start at E, clockwise
	for line in lines:
		action = line[0]
		amt = int(line[1:])
		if action == 'F':
			if facing == 0:
				action = 'N'
			elif facing == 90:
				action = 'E'
			elif facing == 180:
				action = 'S'
			elif facing == 270:
				action = 'W'
			else:
				print('ERROR:', line)
				break

		rc_amt = (0,0)
		if action == 'N':
			rc_amt = (-amt, 0)
		elif action == 'S':
			rc_amt = (+amt, 0)
		elif action == 'E':
			rc_amt = (0, +amt)
		elif action == 'W':
			rc_amt = (0, -amt)
		elif action == 'L':
			facing -= amt
		elif action == 'R':
			facing += amt
		else:
			print('ERROR2:', line)
			break
		facing = facing % 360
		if facing < 0:
			facing = 360 - facing
		rc = (rc[0] + rc_amt[0], rc[1] + rc_amt[1])
		# print(line, ':', facing, action, ship_rc, wp_rc)
	return facing, rc


def part2(lines):
	ship_rc = (0,0) # (NS v, WE ->)
	wp_rc = (-1,10) # (NS v, WE ->)
	for line in lines:
		action = line[0]
		amt = int(line[1:])
		# dir_amt = (amt, amt)
		if action == 'F':
			# print(wp_rc[0] - ship_rc[0])
			# print(wp_rc[1] - ship_rc[1])
			new_r = ship_rc[0] + amt*(wp_rc[0])
			new_c = ship_rc[1] + amt*(wp_rc[1])
			ship_rc = (new_r, new_c)

		rc_amt = (0,0)
		if action == 'N':
			rc_amt = (-amt, 0)
		elif action == 'S':
			rc_amt = (+amt, 0)
		elif action == 'E':
			rc_amt = (0, +amt)
		elif action == 'W':
			rc_amt = (0, -amt)
		elif action == 'L':
			wp_rc = rotate90s(wp_rc, -amt)
		elif action == 'R':
			wp_rc = rotate90s(wp_rc, +amt)
		elif action != 'F':
			print('ERROR2:', line)
			break
		wp_rc = (wp_rc[0] + rc_amt[0], wp_rc[1] + rc_amt[1])
		# print(line, ':', action, ship_rc, wp_rc)
	return ship_rc, wp_rc


# 422 @ 7:09, -27 7:12 -> 445, 66969 @ 7:46
# Part 1: facing looping, absolute value of coords (or distance to origin)
# Part 2: facing meaning, rotation function, rotate L-R copy-paste 
if __name__ == '__main__':
	lines = [line.strip() for line in fileinput.input('input.txt')]
	test = """F10
N3
F7
R90
F11"""
	# lines = test.split('\n')
	print('Lines: {}'.format(len(lines)))

	# Part 1
	facing, rc = part1(lines)
	print('END:', facing, rc)
	x = abs(rc[0])
	y = abs(rc[1])
	print(x + y)

	# Part 2
	ship_rc, wp_rc = part2(lines)
	print('END:', ship_rc, wp_rc)
	x = abs(ship_rc[0])
	y = abs(ship_rc[1])
	print(x + y)
	# print(sum(ship_rc))
