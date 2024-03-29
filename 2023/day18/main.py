#!/usr/bin/env python3
import fileinput
# import sys; sys.path.append("../..")
# from lib import *


class Classy:
    def __init__(self):
        pass


NORTH = (-1, 0)
SOUTH = ( 1, 0)
EAST = (0,  1)
WEST = (0, -1)

INS_TO_DIR = {
    'L': WEST,
    'R': EAST,
    'D': SOUTH,
    'U': NORTH,
}


def move(loc, move_dir):
    loc = list(loc)
    for idx in range(len(loc)):
        loc[idx] += move_dir[idx]
    loc = tuple(loc)
    return loc


def count_edges_before_after(row_edges, all_edges, Cmin, Cmax, rr, c_pos):
    assert Cmin <= c_pos <= Cmax
    if (rr, c_pos) in row_edges:
        return 0, 0

    # edges_before = 0
    # edges_after = 0
    # edge_counted = False
    # for cc in range(Cmin, Cmax+1):       
    #     if (rr, cc) in row_edges:            
    #         if not prev_edge:
    #             if cc < c_pos:
    #                 edges_before += 1
    #                 edge_counted = True
    #             elif cc > c_pos:
    #                 edges_after += 1
    #                 edge_counted = True
    #         prev_edge = True
    #     else:
    #         prev_edge = False
    #         edge_counted = False

    # edges_before = 0
    # edges_after = 0
    # prev_edge = False

    # for cc in range(Cmin, Cmax+1):       
    #     if (rr, cc) in row_edges:            
    #         prev_edge = True
    #     else:
    #         if prev_edge:
    #             if cc < c_pos:
    #                 edges_before += 1
    #             elif cc > c_pos:
    #                 edges_after += 1
    #         prev_edge = False

    above, below = 0, 0
    edges_before = 0
    prev_edge = False
    for cc in range(Cmin, c_pos):
        if (rr, cc) in row_edges:               
            if not prev_edge:
                edges_before += 1
            if (rr-1, cc) in all_edges:
                above += 1
            if (rr+1, cc) in all_edges:
                below += 1
            prev_edge = True
        else:
            # "Fake" edges that don't go both up and down only once
            if (above + below) > 0 and (above, below) != (1, 1):
                edges_before -= 1
            assert (above + below) in [0, 2], f"{(rr, c_pos)}/{cc}: {above} / {below} [{edges_before}]"
            above, below = 0, 0
            prev_edge = False
    if (above + below) > 0 and (above, below) != (1, 1):
        edges_before -= 1
    # if edges_before > 0:
    #     assert (above + below) == (2 * edges_before), f"{(rr, c_pos)}: {above} / {below} [{edges_before}]"

    above, below = 0, 0
    edges_after = 0
    prev_edge = False
    for cc in range(Cmax, c_pos, -1):
        if (rr, cc) in row_edges:               
            if not prev_edge:
                edges_after += 1
            if (rr-1, cc) in all_edges:
                above += 1
            if (rr+1, cc) in all_edges:
                below += 1
            prev_edge = True
        else:
            # print("ab", above, below)
            if (above + below) > 0 and (above, below) != (1, 1):
                edges_after -= 1
            above, below = 0, 0
            prev_edge = False
    if (above + below) > 0 and (above, below) != (1, 1):
        edges_after -= 1

    # assert (edges_before + edges_after) % 2 == 0
    return edges_before, edges_after


def fill_trench(edges):
    all_rr = sorted([loc[0] for loc in edges])
    all_cc = sorted([loc[1] for loc in edges])
    fill = set()
    for rr in all_rr:
        same_row = [loc for loc in edges if loc[0] == rr]
        # Speed up processing processing only needed columns
        col_start = min([loc[1] for loc in same_row])
        col_end = max([loc[1] for loc in same_row])
        # if rr == (-237 + 78):
        #     print_grid(same_row)
        # if rr > (-237 + 78):
        #     exit()
        # Determine if we're "in" an edge (for contiguous edges)
        for cc in range(col_start, col_end+1):
            if (rr, cc) in same_row:
                continue
            before, after = count_edges_before_after(same_row, edges, Cmin, Cmax, rr, cc)
            assert (before + after) % 2 == 0
            # if rr == (-237 + 78):
            #     print(before, after)
            if before > 0 and before % 2 == after % 2 == 1:
                # inside
                fill.add((rr,cc))
        # print('='*10)

        # edge_count = 0
        # inside = False
        # prev_edge = False
        # for cc in range(Cmin, Cmax+1):
        #     if inside:
        #         fill.add((rr,cc))
        #     # Alternate in/out
            # if (rr, cc) in same_row:
            #     if not prev_edge:
            #         edge_count += 1              
            #     prev_edge = True
            # else:
            #     prev_edge = False
        #         # maybe_swap = True
        #         # inside = False
            # if (edge_count % 2) == 0:
            #     inside = False
            # if (edge_count % 2) == 1 and not (rr, cc) in same_row:
            #     inside = True
        #     # But only actually swap on empty spots
        #     # if maybe_swap and not (rr, cc) in same_row:
        #     #     inside = not inside
        #     #     maybe_swap = False
    return fill


def print_grid(locs):
    Rmin = min([loc[0] for loc in locs])
    Rmax = max([loc[0] for loc in locs])
    Cmin = min([loc[1] for loc in locs])
    Cmax = max([loc[1] for loc in locs])
    for rr in range(Rmin, Rmax+1):
        for cc in range(Cmin, Cmax+1):
            if (rr, cc) in locs:
                print('#', end=" ")
            else:
                print('.', end=" ")
        print()
    print()


# [7:27] 47721 wrong (only counted before edges)
# [8:05] 11124 wrong (reqruied equal before & after edges)
# [8:18] break - should've gone BFS flood fill...
# [19:30-20:30] start again, fix issues, then got distracted and submit correct at 23:08
# [23:47] sleep
# TODO: optimize part1 by skipping processing to only places that contain points
def main():
    lines = [line.strip() for line in fileinput.input()]
    # Test data
    # lines = [
    #     "R 4 (#70c710)",
    #     "D 2 (#0dc571)",
    #     "R 3 (#5713f0)",
    #     "D 3 (#0dc571)",
    #     "L 7 (#5713f0)",
    #     "U 5 (#d2c081)"
    # ]
    # lines = [
    #     "R 4 (#70c710)",
    #     "D 2 (#0dc571)",
    #     "R 3 (#5713f0)",
    #     "U 1 (#d2c081)",
    #     "R 2 (#5713f0)",
    #     "D 2 (#0dc571)",
    #     "R 1 (#5713f0)",
    #     "D 1 (#0dc571)",
    #     "L 2 (#5713f0)",
    #     "D 1 (#0dc571)",
    #     "L 6 (#5713f0)",
    #     "U 1 (#d2c081)",
    #     "D 1 (#d2c081)",
    #     "L 5 (#5713f0)",
    #     "U 4 (#d2c081)",
    #     "R 3 (#5713f0)",
    #     "U 1 (#d2c081)",
    # ]

    curr_loc = (0, 0)
    trench = set([curr_loc])
    for line in lines:
        dir_ins, amt, color = line.split(' ')
        amt = int(amt)
        for _ in range(amt):
            curr_loc = move(curr_loc, INS_TO_DIR[dir_ins])
            trench.add(curr_loc)
        # print(dir_ins, amt)
    fill = fill_trench(trench)
    print_grid(trench)
    print_grid(fill)
    print(len(fill) + len(trench))

    # Part 2
    # NUM_TO_DIR = {
    #     0: EAST, # 'R',
    #     1: SOUTH, # 'D',
    #     2: WEST,  # 'L',
    #     3: NORTH, # 'U',
    # }
    # trench_edges = set()
    # prev_point = (0, 0)
    # for line in lines:
    #     _, _, dir_ins_amt = line.split(' ')
    #     dir_ins = NUM_TO_DIR[int(dir_ins_amt[-2])]
    #     amt = int(dir_ins_amt[2:-2], base=16)
    #     move_vec = tuple([val*amt for val in dir_ins])
    #     # print(dir_ins, amt, move_vec)
    #     next_point = move(prev_point, move_vec)
    #     trench_edges.add((prev_point, next_point))
    #     prev_point = next_point
    # # print(trench_edges)

    # vert_edges = []
    # horz_edges = []
    # for edge in trench_edges:
    #     p1, p2 = edge
    #     if p1[1] == p2[1]:
    #         assert p1[0] != p2[0]
    #         vert_edges.append(edge)
    #     else:
    #         assert p1[0] == p2[0]
    #         horz_edges.append(edge)
    # assert len(horz_edges) + len(vert_edges) == len(trench_edges)
    # vert_edges.sort(key=lambda val: val[1])
    # horz_edges.sort(key=lambda val: val[0])
    # print(vert_edges)
    # print(horz_edges)

    # while len(trench_edges) > 0:
    #     # Count rectangles starting at most western outer edge and moving east (so can guarantee in/out)
    #     outer_edge = vert_edges.pop(0)
    #     outer_rr_min = min(outer_edge[0][0], outer_edge[1][0])
    #     outer_rr_max = max(outer_edge[0][0], outer_edge[1][0])
    #     # Find closest overlapping vertical edge
    #     for edge in vert_edges:
    #         p1, p2 = edge
    #         cc = p1[1]
    #         min_rr = min(p1[0], p2[0])
    #         max_rr = max(p1[0], p2[0])
    #         if min_rr <= outer_rr <= max_rr
    #         rr_range = ()
    #     break


if __name__ == '__main__':
    main()
