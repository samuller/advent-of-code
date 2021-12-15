#!/usr/bin/env python3
import math
import fileinput
from collections import deque, namedtuple
from heapq import heappush, heappop
import sys; sys.path.append("../..")
from lib import *


EndLoc = namedtuple('EndLoc', ['len', 'cost', 'pos'])


def full_path(map):
    MIN_LEN = map.rows + map.cols + 1
    END = (map.rows-1, map.cols-1)
    curr = (int(map[0,0]), (0,0))
    paths = [[curr]]
    while True:
        print(len(paths[0]), '->', len(paths))
        new_paths = []
        completed_paths = []
        for path in paths:
            # next = paths.pop()
            # seen.add(next)
            _, curr = path[-1]
            if curr == END or len(path) > MIN_LEN:
                completed_paths.append(path)
                continue
            r,c = curr
            consider = []
            for dr, dc in [(0,1),(1,0)]: #(-1,0), ,(0,-1)
                # for dc in DC:
                rr, cc = r + dr, c + dc
                if not map.in_bounds(rr, cc):
                    continue
                val = int(map[rr,cc])
                if (val, (rr,cc)) in path:
                    continue
                # print(rr,cc)
                consider.append((val, (rr,cc)))
                assert val < 10
            consider.sort(key=lambda vrc: vrc[0], reverse=True)
            for c in consider:
                new_path = list(path)
                new_path.append(c)
                new_paths.append(new_path)           
            # if len(path) > 11:
            #     print(path)
            #     print(sum([p[0] for p in path]))
            #     exit()
        if len(new_paths) == 0:
            print('NO NEW')
            break
        paths = new_paths
        print('done',len(completed_paths))
        for path in completed_paths:
            # print(path)
            print(sum([p[0] for p in path]))
        # for path in paths:
        #     print(path)
        #     print(sum([p[0] for p in path]))
        # exit()
    print(len(paths))
    print('done',len(completed_paths))

    least_risk = sum([p[0] for p in completed_paths[0]])
    least_risk_path = completed_paths[0]
    for path in completed_paths:
        val, final_loc = path[-1]
        if final_loc != END:
            continue
        # print(path)
        risk = sum([p[0] for idx, p in enumerate(path) if idx != 0])
        if risk < least_risk:
            least_risk = risk
            least_risk_path = path
    print(least_risk)
    print(least_risk_path)
    # print(paths[0])
    # print(completed_paths[0])



def bfs(map):
    assert map.rows == map.cols
    MIN_LEN = map.rows + map.cols + 1
    END = (map.rows-1, map.cols-1)
    # start = (0,0)
    curr = (int(map[0,0]), (0,0))
    # DR = [-1,0,1,0]
    # DC = [0,1,0,-1]
    path_done = []
    path_ends = deque()
    start = EndLoc(len=1, pos=(0,0), cost=0)
    path_ends.append(start)
    seen = {(0,0): start}
    while path_ends:
        curr = path_ends.pop()
        # print(curr, int(map[curr.pos]))
        if curr.pos == END or curr.len > MIN_LEN:
            path_done.append(curr)
            print(len(path_done), len(path_ends))
            continue
        r,c = curr.pos
        for dr, dc in [(0,1),(1,0)]:
            rr, cc = r + dr, c + dc
            if not map.in_bounds(rr, cc):
                continue
            val = int(map[rr,cc])
            next = EndLoc(len=curr.len+1, pos=(rr,cc), cost=curr.cost+val)
            if next.pos in seen:
                visited = seen[next.pos]
                if visited.cost < next.cost:
                    seen[next.pos] = next
            else:
                path_ends.append(next)
    print(len(path_done))
    # print(seen)
    lowest = path_done[0]
    for end in path_done:
        if end.cost < lowest.cost:
            lowest = end
    print(lowest)


def heuristic(map, pos, goal_pos):
    dr = goal_pos[0] - pos[0]
    dc = goal_pos[1] - pos[1]
    return math.sqrt(dr**2 + dc**2)

def a_star(map, start_pos=(0,0), goal_pos=None):
    if goal_pos is None:
        goal_pos = (map.rows-1, map.cols-1)
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
            return curr

        r, c = curr.pos
        for dr, dc in [(0,1),(1,0)]:
            rr, cc = r + dr, c + dc
            if not map.in_bounds(rr, cc):
                continue
            val = int(map[rr,cc])
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


def main():
    lines = [line.strip() for line in fileinput.input()]
    print(f'Lines: {len(lines)}')

    map = Map2D()
    map.load_from_data(lines)

    # First attempt
    # full_path(map)

    # Second attempt
    # bfs(map)

    # Third attempt
    print(a_star(map))


if __name__ == '__main__':
    main()
