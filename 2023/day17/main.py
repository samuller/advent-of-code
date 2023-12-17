#!/usr/bin/env python3
import fileinput
# import sys; sys.path.append("../..")
# from lib import *


NORTH = (-1, 0)
SOUTH = ( 1, 0)
EAST = (0,  1)
WEST = (0, -1)

LEFT_RIGHT = {
    NORTH: [WEST, EAST],
    SOUTH: [WEST, EAST],
    EAST: [NORTH, SOUTH],
    WEST: [NORTH, SOUTH],
}



def print_path(R, C, path):
    for rr in range(R):
        for cc in range(C):
            if (rr, cc) in path:
                print('#', end="")
            else:
                print('.', end="")
        print()
    print()


def print_grid(grid):
    R = len(grid)
    C = len(grid[0])
    for rr in range(R):
        for cc in range(C):
            print(grid[rr][cc], end=" ")
        print()
    print()


def move(loc, move_dir):
    loc = list(loc)
    for idx in range(len(loc)):
        loc[idx] += move_dir[idx]
    loc = tuple(loc)
    return loc


# [8:30] Realise sum_grid needs to contain info for forward-count as well
def main():
    lines = [line.strip() for line in fileinput.input()]

    R = len(lines)
    C = len(lines[0])
    grid = []
    for rr in range(len(lines)):
        row = [int(c) for c in lines[rr]]
        assert len(row) == C
        grid.append(row)
    # print(grid)
    print_grid(grid)

    sum_grid_count = []
    for _ in range(3):
        sum_grid = []
        for _ in range(R):
            sum_grid.append([-1]*C)
        sum_grid[0][0] = 0
        sum_grid_count.append(sum_grid)

    fronts = [(0,0), (0,0)]
    front_dirs = [EAST, SOUTH]
    front_fwd_count = [0, 0]
    while len(fronts) > 0:
        assert len(fronts) == len(front_dirs)
        print(len(fronts), fronts)
        choose_idx = 0
        loc = fronts.pop(choose_idx)
        from_dir = front_dirs.pop(choose_idx)
        count = front_fwd_count.pop(choose_idx)

        curr_cost = max(sum_grid[loc[0]][loc[1]], 0)
        for new_dir in [NORTH, SOUTH, EAST, WEST]:
            new_loc = move(loc, new_dir)
            # Out of bounds
            if not (0 <= new_loc[0] < R and 0 <= new_loc[1] < C):
                # print("|| oob ||", from_dir, '->',new_dir)
                continue
            rr, cc = new_loc
            prev_cost = sum_grid[rr][cc]
            new_cost = curr_cost + grid[rr][cc]
            new_count = 0
            # Moving forward
            if new_dir == from_dir:
                # Limited to 3 forward moves
                if count >= 2:
                    # print("|| fwd ||", from_dir, '->',new_dir)
                    continue
                new_count = count + 1
            # If new path is better
            if prev_cost == -1 or new_cost < prev_cost:
                if (rr, cc) in [(R-1, C-1), (11, 12)]:
                    print(f"==== {(rr, cc)} ====")
                    print(loc, '->',new_loc)
                    print(from_dir, '->',new_dir)
                    print(prev_cost, '->', f"{curr_cost} + {grid[rr][cc]} = {new_cost}")
                sum_grid[rr][cc] = new_cost
                fronts.append(new_loc)
                front_dirs.append(new_dir)
                front_fwd_count.append(new_count)
            else:
                # print("|| max ||", from_dir, '->',new_dir)
                pass

    print_grid(sum_grid)
    print(sum_grid[R-1][C-1])

    # [7:29] needs BFS instead of following all paths blindly like yesterday
    # path_loc = [(0, 0)]
    # path_cost = [0]
    # path_dir = [EAST]
    # path_fwd_count = [0]
    # path_history = [set()]
    # min_solution = 10**20
    # min_path = []
    # while len(path_loc) > 0:
    #     try:
    #         print(min_solution, len(path_loc))
    #         assert len(path_loc) == len(path_dir)
    #         assert len(path_dir) == len(path_fwd_count)
    #         assert len(path_fwd_count) == len(path_cost)
    #         assert len(path_history) == len(path_loc)
    #         choose_idx = 0
    #         loc = path_loc.pop(choose_idx)
    #         move_dir = path_dir.pop(choose_idx)
    #         cost = path_cost.pop(choose_idx)
    #         fwd_count = path_fwd_count.pop(choose_idx)
    #         history = path_history.pop(choose_idx)

    #         loc = list(loc)
    #         for idx in range(len(loc)):
    #             loc[idx] += move_dir[idx]
    #         loc = tuple(loc)

    #         # Out of bounds
    #         if not (0 <= loc[0] < R and 0 <= loc[1] < C):
    #             continue
    #         if loc in history:
    #             continue

    #         fwd_count += 1
    #         cost += grid[loc[0]][loc[1]]
    #         history.add(loc)

    #         if loc == (R-1, C-1):
    #             min_solution = min(min_solution, cost)
    #             min_path = history
    #         else:
    #             # Turn left and right
    #             for new_dir in LEFT_RIGHT[move_dir]:
    #                 path_loc.append(loc)
    #                 path_dir.append(new_dir)
    #                 path_cost.append(cost)
    #                 path_fwd_count.append(0)
    #                 # Copy separate history for new directions
    #                 path_history.append(set(history))
    #             # Forward
    #             if fwd_count <= 4:
    #                 path_loc.append(loc)
    #                 path_dir.append(move_dir)
    #                 path_cost.append(cost)
    #                 path_fwd_count.append(fwd_count)
    #                 path_history.append(history)
    #     except KeyboardInterrupt:
    #         break
    # print_path(R, C, min_path)
    # print(min_solution)


if __name__ == '__main__':
    main()
