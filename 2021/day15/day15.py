#!/usr/bin/env python3
import math
import fileinput
from collections import deque, namedtuple
from heapq import heappush, heappop
import sys; sys.path.append("../..")
from lib import *


EndLoc = namedtuple('EndLoc', ['len', 'cost', 'pos'])


def heuristic(map, pos, goal_pos):
    r,c = pos
    val = map[r][c]
    dr = goal_pos[0] - pos[0]
    dc = goal_pos[1] - pos[1]
    dist = math.sqrt(dr**2 + dc**2)
    return val + dist


def reconstruct_path(came_from, pos):
    path = [pos]
    while pos in came_from:
        pos = came_from[pos]
        path.append(pos)
    return list(reversed(path))


def a_star(map, start_pos=(0,0), goal_pos=None):
    R = len(map)
    C = len(map[0])
    if goal_pos is None:
        goal_pos = (R-1, C-1)
    start_node = EndLoc(len=1, pos=start_pos, cost=0)
    
    inf = float("inf")

    came_from = {}
    g_score = {start_pos: 0.0}
    f_score = {start_pos: 0.0 + heuristic(map, start_pos, goal_pos)}

    open_pos_set = set([start_pos])
    open_heap = []
    heappush(open_heap, (f_score[start_pos], start_node))
    while open_heap:
        # print(open_heap)
        curr_f_score, curr = heappop(open_heap)
        open_pos_set.remove(curr.pos)
        # print(curr_f_score, curr)
        if curr.pos == goal_pos:
            # print(came_from[end])
            path = reconstruct_path(came_from, goal_pos)
            # print(path)
            print(sum([map[p[0]][p[1]] for p in path]) - map[path[0][0]][path[0][1]])
            return curr

        r, c = curr.pos
        for dr, dc in [(0,1),(1,0),(0,-1),(-1,0)]:
            rr, cc = r + dr, c + dc
            if not (0<=rr<R and 0<=cc<C):
                continue
            val = map[rr][cc]
            near = EndLoc(len=curr.len+1, pos=(rr,cc), cost=curr.cost+val)

            guess = g_score.get(curr.pos, inf) + val
            # print("guess", guess)
            if guess < g_score.get(near.pos, inf):
                came_from[near.pos] = curr.pos
                g_score[near.pos] = guess
                f_score[near.pos] = guess + heuristic(map, near.pos, goal_pos)
                if near.pos not in open_pos_set:
                    open_pos_set.add(near.pos)
                    heappush(open_heap, (f_score[near.pos], near))
    assert False


def expand_map(map, times=5):
    R = len(map)
    C = len(map[0])
    # big_map = [[0]*C*5]*R*5
    big_map = [[0 for _ in range(C*5)] for _ in range(R*5)]
    for r, row in enumerate(big_map):
        for c, val in enumerate(row):
            # print(r,c)
            val = map[r % R][c % C]
            add = (r // R) + (c // C)
            val = 1 + ((val - 1 + add) % 9)
            big_map[r][c] = val

            if 0<=r<R and 0<=c<C:
                assert big_map[r][c] == map[r][c]
    return big_map


def print_map(map):
    for r, row in enumerate(map):
        for c, val in enumerate(row):
            print(val, end="")
        print()
    print()

# 14:28 - 2973 (too high) - no up or left movements
# 14:37 - 2970 (too high) - heuristic not good enough when including left & up?
# 14:50 - 2969 (too high) - guess
# 15:02 - cost somehow took starting value into account again
def main():
    lines = [line.strip() for line in fileinput.input()]
    print(f'Lines: {len(lines)}')

    # map = Map2D()
    # map.load_from_data(lines)
    map = [[int(c) for c in line] for line in lines]
    R = len(map)
    C = len(map[0])

    # # Test equation for height changes
    # for r in range(5):
    #     for c in range(5):
    #         val = 8
    #         add = r + c
    #         val = 1 + ((val - 1 + add) % 9)
    #         # val += 1
    #         print(val, end=" ")
    #         # print((r,c), end=" ")
    #     print()
    # print()

    print(a_star(map))

    big_map = expand_map(map)
    # print_map(big_map)
    print(a_star(big_map))


if __name__ == '__main__':
    main()
