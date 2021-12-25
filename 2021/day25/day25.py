#!/usr/bin/env python3
import fileinput
# import sys; sys.path.append("../..")
# from lib import *


def print_map(map):
    R = len(map)
    C = len(map[0])
    for r in range(R):
        for c in range(C):
            print(map[r][c], end="")
        print()
    print()


def do_moves(map, moves):
    for move in moves:
        value, old_r, old_c, new_r, new_c = move
        map[old_r][old_c] = '.'
        map[new_r][new_c] = value
    return map


# 520 @ +20min
def main():
    map = [list(line.strip()) for line in fileinput.input()]
    R = len(map)
    C = len(map[0])

    print_map(map)
    steps = 0
    while True:
        moves = []
        move_count = 0
        for r in range(R):
            for c in range(C):
                if map[r][c] in ['.', 'v']:
                    continue
                elif map[r][c] == '>' and map[r][(c+1) % C] == '.':
                    moves.append(('>', r,c, r,(c+1) % C))
        map = do_moves(map, moves)
        move_count += len(moves)
        moves = []

        for r in range(R):
            for c in range(C):
                if map[r][c] in ['.', '>']:
                    continue
                elif map[r][c] == 'v' and map[(r+1) % R][c] == '.':
                    moves.append(('v', r,c, (r+1) % R, c))
        map = do_moves(map, moves)
        move_count += len(moves)

        steps += 1
        print("Step", steps, f"({move_count})")
        # print_map(map)
        if move_count == 0:
            break


if __name__ == '__main__':
    main()
