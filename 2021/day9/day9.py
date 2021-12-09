#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("../..")
from lib import *
import itertools


def function(input):
    return False


def main():
    lines = [line.strip() for line in fileinput.input()]
    print(f'Lines: {len(lines)}')

    count_valid = 0
    for line in lines:
        fields = line.split(' ')
    
    map = Map2D()
    map.load_from_data(lines)
    count = 0
    # print(map)
    # 513 @ 7:46 (start ~7:30)
    # 1568
    # 508 @ 7:52 (<=)
    for r in range(map.rows):
        for c in range(map.cols):
            height = int(map.get(r,c))
            is_lowest = True
            # print(map.get(r, c))
            for dr,dc in [(-1,0),(0,-1),(1,0),(0,1)]: #itertools.product([-1,0,1],[-1,0,1]):
                if (dr, dc) == (0,0):
                    continue
                if map.in_bounds(r+dr, c+dc):
                    if int(map.get(r+dr, c+dc)) <= height:
                        is_lowest = False
                    # print(map.get(r+dr, c+dc))
            if is_lowest:
                risk_level = height+1
                # print(risk_level)
                # print(r,c,":", height)
                count += risk_level
    print(count)



if __name__ == '__main__':
    main()
