#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("..")
from lib import *
import math


class Classy:
	def __init__(self):
		pass


def rotate(center, point, degree):
	angle = math.radians(degree)
	ox, oy = center
	px, py = point

	qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
	qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
	return int(round(qx)), int(round(qy))


# 422 @ 7:09, -27 7:12 -> 445, 66969 @ 7:46
if __name__ == '__main__':
	lines = [line.strip() for line in fileinput.input('input.txt')]
	test = """F10
N3
F7
R90
F11"""
	# lines = test.split('\n')
	print('Lines: {}'.format(len(lines)))

	ship_rc = (0,0) # (NS v, WE ->)
	wp_rc = (-1,10) # (NS v, WE ->)
	facing = 90  # N = 0, start at E, clockwise
	count_valid = 0
	for line in lines:
		action = line[0]
		amt = int(line[1:])
		dir_amt = (amt, amt)
		if action == 'F':
			# print(wp_rc[0] - ship_rc[0])
			# print(wp_rc[1] - ship_rc[1])
			new_r = ship_rc[0] + amt*(wp_rc[0])
			new_c = ship_rc[1] + amt*(wp_rc[1])
			ship_rc = (new_r, new_c)
			# if facing == 0:
			# 	action = 'N'
			# elif facing == 90:
			# 	action = 'E'
			# elif facing == 180:
			# 	action = 'S'
			# elif facing == 270:
			# 	action = 'W'
			# else:
			# 	print('ERROR:', line)
			# 	break

		if action == 'N':
			# rc = (rc[0]-amt, rc[1])
			wp_rc = (wp_rc[0]-amt, wp_rc[1])
		elif action == 'S':
			# rc = (rc[0]+amt, rc[1])
			wp_rc = (wp_rc[0]+amt, wp_rc[1])
		elif action == 'E':
			# rc = (rc[0], rc[1]+amt)
			wp_rc = (wp_rc[0], wp_rc[1]+amt)
		elif action == 'W':
			# rc = (rc[0], rc[1]-amt)
			wp_rc = (wp_rc[0], wp_rc[1]-amt)
		elif action == 'L':
			# facing -= amt
			# wp_rc = (wp_rc[0] - ship_rc[0], wp_rc[1] - ship_rc[1])
			wp_rc = rotate([0,0], wp_rc, +amt)
		elif action == 'R':
			# facing += amt
			wp_rc = rotate([0,0], wp_rc, -amt)
		elif action != 'F':
			print('ERROR2:', line)
			break
		# facing = facing % 360
		# if facing < 0:
		# 	facing = 360 - facing
		# ship_rc = ()

		print(line, ':', facing, action, ship_rc, wp_rc)
	print('END:', facing, ship_rc, wp_rc)
	x = abs(ship_rc[0])
	y = abs(ship_rc[1])
	print(x + y)
	# print(sum(ship_rc))
