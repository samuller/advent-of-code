#!/usr/bin/env python3
from collections import namedtuple
import fileinput
import sys; sys.path.append("../..")
from lib import *


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


# 7:16 wrong 100066560 -> wrong width-height
def main():
    lines = [line.strip() for line in fileinput.input()]
    Robot = namedtuple('Robot', ['pos', 'vel'])
    robots = []
    for line in lines:
        pos_str, vel_str = line.split(' ')
        pos = [int(n) for n in pos_str.split('p=')[1].split(',')]
        vel = [int(n) for n in vel_str.split('v=')[1].split(',')]
        robots.append(Robot(pos=pos, vel=vel))
    # width, height = 11, 7
    width, height = 101, 103
    dims = (width, height)
    p2 = 0
    longest_diag = 0
    for iter in range(10000):
        # Part 2 - investigate
        # if iter % 100 == 0:
        # print(iter)
        # draw(robots, (width, height))
        diag = find_longest_diagonal(robots)
        if diag > longest_diag:
            longest_diag = diag
            p2 = iter
        # if diag > 10:
        #     print(iter, ":", diag)
        # if iter == 6493:
        #     draw(robots, (width, height))
        for idx, robot in enumerate(robots):
            pos, vel = robot
            new_pos = ((pos[0]+vel[0]) % width, (pos[1]+vel[1]) % height)
            robots[idx] = Robot(pos=new_pos, vel=vel)
    # draw(robots, (width, height))
    quadrants = [0,0,0,0]
    for robot in robots:
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
    print(p2)

if __name__ == '__main__':
    main()
