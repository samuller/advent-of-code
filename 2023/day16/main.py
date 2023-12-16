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



def print_history(R, C, beam_history):
    used = set()
    beam_path_dir = dict()
    dir_to_chr = {
        EAST: '<',
        WEST: '>',
        NORTH: '^',
        SOUTH: 'v',
    }
    for loc, dir in beam_history:
        if loc in beam_path_dir:
            beam_path_dir[loc] = 2
        else:
            beam_path_dir[loc] = dir_to_chr[dir]

    for rr in range(R):
        for cc in range(C):
            if (rr, cc) in beam_path_dir:
                used.add((rr, cc))
                print(beam_path_dir[(rr, cc)], end="")
            else:
                print('.', end="")
        print()
    print()

def print_path(R, C, beam_path):
    used = set()
    for rr in range(R):
        for cc in range(C):
            if (rr, cc) in beam_path:
                used.add((rr, cc))
                print('#', end="")
            else:
                print('.', end="")
        print()
    print()
    assert len(used) == len(beam_path)


# [7:34] - 6286
def main():
    lines = [line.strip() for line in fileinput.input()]
    print(f'Lines: {len(lines)}')

    mirrors_splitters = dict()
    R = len(lines)
    C = len(lines[0])
    for rr, row in enumerate(lines):
        assert len(row) == C
        for cc, val in enumerate(row):
            if val in ['/', '\\', '|', '-']:
                mirrors_splitters[(rr, cc)] = val
            else:
                assert val == '.'
    print(mirrors_splitters)

    beam_fronts = [(0, -1)]
    beam_dirs = [EAST]
    # beam_dirs = [SOUTH]  # input data
    beam_path = set()  # set(beam_fronts)
    beam_history = set()  # set(zip(beam_fronts, beam_dirs))
    print(beam_history)
    while len(beam_fronts) > 0:
        # print_path(R, C, beam_path)
        assert len(beam_fronts) == len(beam_dirs)
        beam = beam_fronts.pop()
        move_dir = beam_dirs.pop()
        beam_history.add((beam, move_dir))

        beam = list(beam)
        for idx in range(len(beam)):
            beam[idx] += move_dir[idx]
        beam = tuple(beam)
        # Out of bounds
        if not (0 <= beam[0] < R and 0 <= beam[1] < C):
            continue
        # Followed path before (avoid loops)
        if (beam, move_dir) in beam_history:
            continue

        beam_path.add(beam)
        # print(beam)
        if beam in mirrors_splitters:
            obj = mirrors_splitters[beam]
            if obj == '\\':
                # Move dir to new move dir
                redir = {
                    EAST: SOUTH,
                    WEST: NORTH,
                    NORTH: WEST,
                    SOUTH: EAST
                }
                beam_fronts.append(beam)
                beam_dirs.append(redir[move_dir])
            elif obj == '/':
                redir = {
                    EAST: NORTH,
                    WEST: SOUTH,
                    NORTH: EAST,
                    SOUTH: WEST
                }
                beam_fronts.append(beam)
                beam_dirs.append(redir[move_dir])
            elif obj == '|':
                redir = {
                    EAST: [NORTH, SOUTH],
                    WEST: [NORTH, SOUTH],
                    NORTH: [NORTH],
                    SOUTH: [SOUTH]
                }
                for new_dir in redir[move_dir]:
                    beam_fronts.append(beam)
                    beam_dirs.append(new_dir)
            elif obj == '-':
                redir = {
                    EAST: [EAST],
                    WEST: [WEST],
                    NORTH: [WEST, EAST],
                    SOUTH: [WEST, EAST]
                }
                for new_dir in redir[move_dir]:
                    beam_fronts.append(beam)
                    beam_dirs.append(new_dir)
            else:
                assert False
        else:
            beam_fronts.append(beam)
            beam_dirs.append(move_dir)
        # print(len(beam_path), beam_fronts)
        print(len(beam_path))
    print_path(R, C, beam_path)
    # print_history(R, C, beam_history)
    print(len(beam_path))


if __name__ == '__main__':
    main()
