#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("..")
from lib import *
import math


def rotate90s(point, times):
	# 90 degree rotations basically swap the x-y axes
	# and then negates one axis (depending on direction)
	# +R -> +D -> -L -> -U, +D -> -L -> -U -> +R
	# -L -> +U -> +R -> +D, -U -> +R -> +D -> -L
	p1, p2 = point
	for t in range(abs(times)):
		p1, p2 = p2, p1
		if times > 0:
			p2 = -p2
		else:
			p1 = -p1
	return p1, p2
# (-4, 10) -> (10,_4) -> (4, _-10) -> (-10 ,_-4) -> (-4, 10)
assert rotate90s((-4, 10), 1) == (10, 4)
assert rotate90s((-4, 10), 2) == (4, -10)
assert rotate90s((-4, 10), 3) == (-10, -4)
assert rotate90s((-4, 10), 4) == (-4, 10)
assert rotate90s((-4, 10), -3) == (10, 4)
assert rotate90s((-4, 10), -2) == (4, -10)
assert rotate90s((-4, 10), -1) == (-10, -4)
assert rotate90s((-4, 10), -4) == (-4, 10)


def rotate(center, point, degree):
	degree = -degree
	angle = math.radians(degree)
	# https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python
	ox, oy = center
	px, py = point

	qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
	qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
	return int(round(qx)), int(round(qy))
assert rotate90s((-4, 10), 1) == rotate([0,0],(-4,10),90), \
	'{} != {}'.format(rotate90s((-4, 10), 1), rotate([0,0],(-4,10),90))
assert rotate90s((-4, 10), 2) == rotate([0,0],(-4,10),180), \
	'{} != {}'.format(rotate90s((-4, 10), 2), rotate([0,0],(-4,10),180))
assert rotate90s((-4, 10), 3) == rotate([0,0],(-4,10),270), \
	'{} != {}'.format(rotate90s((-4, 10), 3), rotate([0,0],(-4,10),270))
assert rotate90s((-4, 10), 1) == rotate([0,0],(-4,10),90), \
	'{} != {}'.format(rotate90s((-4, 10), 1), rotate([0,0],(-4,10),90))


def move_direction(dir, amt):
	xy_amt = (0,0)
	if dir == 'N':
		xy_amt = (0, +amt)
	elif dir == 'S':
		xy_amt = (0, -amt)
	elif dir == 'E':
		xy_amt = (+amt, 0)
	elif dir == 'W':
		xy_amt = (-amt, 0)
	return xy_amt


def part1(lines):
	xy = (0,0)
	# NESW = 0123
	face_dir = 'NESW'
	facing = 1
	for line in lines:
		action = line[0]
		amt = int(line[1:])
		if action == 'F':
			action = face_dir[facing]

		if action in 'NSEW':
			xy_amt = move_direction(action, amt)
			xy = (xy[0] + xy_amt[0], xy[1] + xy_amt[1])
		elif action == 'L':
			facing += (4-amt//90)
		elif action == 'R':
			facing += amt//90
		else:
			print('ERROR2:', line)
			break
		facing = facing % 4
		# print(line, ':', facing, xy, action)
	return facing, xy


def part2(lines):
	ship_xy = (0,0) # (NS v, WE ->)
	wp_xy = (10, 1) # (NS v, WE ->)
	for line in lines:
		action = line[0]
		amt = int(line[1:])
		# dir_amt = (amt, amt)
		if action == 'F':
			new_x = ship_xy[0] + amt*(wp_xy[0])
			new_y = ship_xy[1] + amt*(wp_xy[1])
			ship_xy = (new_x, new_y)

		if action in 'NSEW':
			xy_amt = move_direction(action, amt)
			wp_xy = (wp_xy[0] + xy_amt[0], wp_xy[1] + xy_amt[1])
		elif action == 'L':
			wp_xy = rotate90s(wp_xy, -amt//90)
		elif action == 'R':
			wp_xy = rotate90s(wp_xy, +amt//90)
		elif action != 'F':
			print('ERROR2:', line)
			break		
		# print(line, ':', action, ship_xy, wp_xy)
	return ship_xy


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
	facing, xy = part1(lines)
	x,y = xy
	print(abs(x) + abs(y))

	# Part 2
	x,y = part2(lines)
	print(abs(x) + abs(y))
