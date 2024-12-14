#!/usr/bin/env python3
from collections import namedtuple
import fileinput
import sys; sys.path.append("../..")
from lib import *


Robot = namedtuple('Robot', ['pos', 'vel'])


def draw(robots, dimensions):
    width, height = dimensions
    robots_pos = [r[0] for r in robots]
    for yy in range(height):
        for xx in range(width):
            count = robots_pos.count((xx, yy))
            if count == 0:
                print('.', end="")
            else:
                print(count, end="")
        print()
    # print(robots)


def find_longest_diagonal(robots):
    robots_pos = set([tuple(r[0]) for r in robots])
    longest_diag = 0
    for pos in robots_pos:
        diag = 1
        while (pos[0]+1, pos[1]+1) in robots_pos:
            diag += 1
            pos = (pos[0]+1, pos[1]+1)
        if diag > longest_diag:
            longest_diag = diag
    return longest_diag


def run_sim(robots, dimensions, iterations=100, custom_checks=None):
    # Make copy before editing
    robots = list(robots)
    if custom_checks is None:
        custom_checks = lambda iter, robots: None
    width, height = dimensions

    for iter in range(iterations):
        custom_checks(iter, robots)
        for idx, robot in enumerate(robots):
            pos, vel = robot
            new_pos = ((pos[0]+vel[0]) % width, (pos[1]+vel[1]) % height)
            robots[idx] = Robot(pos=new_pos, vel=vel)
    return robots


# 7:16 wrong 100066560 -> wrong width-height
def main():
    lines = [line.strip() for line in fileinput.input()]
    robots = []
    for line in lines:
        pos_str, vel_str = line.split(' ')
        pos = [int(n) for n in pos_str.split('p=')[1].split(',')]
        vel = [int(n) for n in vel_str.split('v=')[1].split(',')]
        robots.append(Robot(pos=pos, vel=vel))
    # width, height = 11, 7  # Test data
    width, height = 101, 103
    dims = (width, height)
    robots_p1 = run_sim(robots, dims, iterations=100, custom_checks=None)
    quadrants = [0,0,0,0]
    for robot in robots_p1:
        quad = None
        pos = robot[0]
        if 0 <= pos[0] < width//2:
            if 0 <= pos[1] < height//2:
                quad = 3
            if height//2 < pos[1] < height:
                quad = 2
        if width//2 < pos[0] < width:
            if 0 <= pos[1] < height//2:
                quad = 0
            if height//2 < pos[1] < height:
                quad = 1
        if quad is not None:
            quadrants[quad] += 1
    print(prod(quadrants))
    # Part 2
    p2 = 0
    longest_diag = 0
    def has_tree(iter, robots):
        nonlocal p2, longest_diag
        diag = find_longest_diagonal(robots)
        if diag > longest_diag:
            longest_diag = diag
            # print(iter, longest_diag)
            # print(iter)
            # draw(robots, dims)
            p2 = iter
    run_sim(robots, dims, iterations=10_000, custom_checks=has_tree)
    print(p2)

if __name__ == '__main__':
    main()
