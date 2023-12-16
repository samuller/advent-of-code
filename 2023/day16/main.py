#!/usr/bin/env python3
import fileinput
from random import random
# import sys; sys.path.append("../..")
# from lib import *


class Classy:
    def __init__(self):
        pass


NORTH = (-1, 0)
SOUTH = ( 1, 0)
EAST = (0,  1)
WEST = (0, -1)


def print_history(R, C, beam_history, mirrors_splitters):
    used = set()
    dir_to_chr = {
        EAST: '>',
        WEST: '<',
        NORTH: '^',
        SOUTH: 'v',
    }
    beam_path_dir = dict()
    for loc, dir in beam_history:
        if loc in beam_path_dir:
            val = beam_path_dir[loc]
            if val in dir_to_chr.values():
                beam_path_dir[loc] = 2
            else:
                beam_path_dir[loc] = val + 1
        else:
            beam_path_dir[loc] = dir_to_chr[dir]

    for rr in range(R):
        print(f"{str(rr).rjust(3)}: ", end="")
        for cc in range(C):
            if (rr, cc) in mirrors_splitters:
                print(mirrors_splitters[(rr, cc)], end="")
                continue
            if (rr, cc) in beam_path_dir:
                used.add((rr, cc))
                print(beam_path_dir[(rr, cc)], end="")
            else:
                print('.', end="")
        print()
    print()
    # assert len(used) == len(beam_path_dir), len(beam_path_dir)


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
# [8:08] - 6145 (popleft differs from pop?)
# [8:42] - beam_history had incorrect values
def main():
    lines = [line.strip() for line in fileinput.input()]

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

    # Start out of screen
    beam_fronts = [(0, -1)]
    beam_dirs = [EAST]
    beam_path = set()  # set(beam_fronts)
    beam_history = set()  # set(zip(beam_fronts, beam_dirs))
    print(beam_history)
    while len(beam_fronts) > 0:
        # print_path(R, C, beam_path)
        assert len(beam_fronts) == len(beam_dirs)
        # Popping randomly **shouldn't** affect outcome
        choose_idx = int(random() * len(beam_fronts))
        # choose_idx = -1
        beam = beam_fronts.pop(choose_idx)
        move_dir = beam_dirs.pop(choose_idx)

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

        # Contains first out of screen starting point
        beam_history.add((beam, move_dir))
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
        # print(len(beam_path), len(beam_fronts), beam_fronts)
        print(len(beam_path), len(beam_fronts))
    assert len(beam_fronts) == 0
    # Remove first out of screen starting point
    # beam_history.remove(((0, -1), EAST))
    assert len(beam_path) <= len(beam_history)
    print_path(R, C, beam_path)
    print_history(R, C, beam_history, mirrors_splitters)
    print(len(beam_path))


if __name__ == '__main__':
    main()
