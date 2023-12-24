#!/usr/bin/env python3
import fileinput
# import sys; sys.path.append("../..")
# from lib import *


def main():
    lines = [line.strip() for line in fileinput.input()]

    stones = []
    for line in lines:
        pos, vel = line.split(' @ ')
        pos = [int(num) for num in pos.split(', ')]
        vel = [int(num) for num in vel.split(', ')]
        print(pos, vel)
        stones.append((pos, vel))

    ans1 = 0
    range_min = 200000000000000  # 7
    range_max = 400000000000000  # 27
    for idx1 in range(len(stones)):
        (x1, y1, z1), v1 = stones[idx1]
        (x2, y2, z2) = (x1 + v1[0], y1 + v1[1], z1 + v1[2])
        # vel_angle1 = v1[1]/v1[0]
        for idx2 in range(idx1 + 1, len(stones)):
            (x3, y3, z3), v2 = stones[idx2]
            (x4, y4, z4) = (x3 + v2[0], y3 + v2[1], z3 + v2[2])
            denominator = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)
            crossing = None
            if denominator != 0:
                # Given two points on each line: https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
                cross_x = ( (x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4) ) / denominator
                cross_y = ( (x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4) ) / denominator
                crossing = (cross_x, cross_y)
                
                in_future1 = (cross_x >= x1 if v1[0] > 0 else cross_x <= x1) and \
                    (cross_y >= y1 if v1[1] > 0 else cross_y <= y1)
                in_future2 = (cross_x >= x3 if v2[0] > 0 else cross_x <= x3) and \
                    (cross_y >= y3 if v2[1] > 0 else cross_y <= y3)
                if range_min <= cross_x <= range_max and range_min <= cross_y <= range_max \
                        and in_future1 and in_future2:
                    print("inside")
                    ans1 += 1

            print((idx1, idx2), crossing)

            # vel_angle2 = v2[1]/v2[0]
            # print((idx1, idx2), vel_angle1, vel_angle2)
            # if vel_angle1 == vel_angle2:
            #     print("parallel")
    print(ans1)


if __name__ == '__main__':
    main()
