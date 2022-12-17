#!/usr/bin/env python3
import time
import fileinput
from collections import namedtuple

import sys; sys.path.append("../..")
from lib import *


# Block = namedtuple('Block', ['r', 'c'])


def draw_piece(piece, sr=0, sc=0):
    for r in range(4):
        for c in range(4):
            if (sr - r, sc + c) in piece:
                print('#', end="")
            else:
                print('.', end="")
        print()
    print()


def move_piece(piece, dr, dc):
    for idx in range(len(piece)):
        # (r,c) = piece[idx]
        # piece[idx] = (r+dr, c+dc)
        piece[idx][0] += dr
        piece[idx][1] += dc


def hit_scene_below(scene, falling_piece):    
    # scene_top = [0] * 7
    # for c in range(0, 7):
    #     top = 0
    #     for block in scene:
    #         block_r, block_c = block
    #         if block_c != c:
    #             continue
    #         top = min(top, block_r)
    #     scene_top[c] = top
    # print("top:", scene_top)

    # scene_top = scene.top

    for idx in range(len(falling_piece)):
        r, c = falling_piece[idx]
        if (r+1, c) in scene.blocks or r+1 >= 0:
        # if r + 1 == scene_top[c]:
            # print("stopped by", block_r, block_c)
            return True
    return False


def hit_sides(scene, falling_piece, dir):
    dc = 1 if dir == '>' else -1
    for idx in range(len(falling_piece)):
        block_r, block_c = falling_piece[idx]
        # if (block_c, dir) == (6, '>') or (block_c, dir) == (0, '<'):
        #     return True
        if (block_c + dc) in [-1, 7]:
            return True
        if (block_r, block_c + dc) in scene.blocks:
            return True
    return False


class Scene:
    def __init__(self, width=7) -> None:
        self.width = width
        self.blocks = set()
        self.top = [0] * width
        self.outline = set([(0, c) for c in range(width)])

    def add_piece(self, piece):
        self.blocks.update(tuple(map(tuple, piece)))
        # self.blocks.update(tuple([tuple(blk) for blk in piece]))
        self._update_top(piece)
        # Part 2
        # self._update_outline(piece)

    def _update_top(self, new_piece):
        for block in new_piece:
            r, c = block
            self.top[c] = min(self.top[c], r)

    def move_up(self, amount):
        # Move all blocks higher by a certain amount
        for idx in range(len(self.top)):
            self.top[idx] += amount

        new_blocks = set()
        for r,c in self.blocks:
            new_blocks.add((r - amount,c))
        self.blocks = new_blocks
        # self.outline

    def clear_blocks(self):
        """Remove inaccessible blocks below outline/top-surface."""
        # Expand outwards from top-left to find outline
        start = (min(self.top) - 1, 0)
        queue = [start]
        visited = set()
        new_outline = set()
        while len(queue) > 0:
            r, c = queue.pop(0)
            if not (0 <= c < self.width and r < 0):
                continue
            if (r,c) in visited:
                continue
            visited.add((r,c))
            if (r,c) in self.blocks:
                new_outline.add((r,c))
                continue
            # Expand down- and side-wards
            for dr, dc in [(1, 0), (0, -1), (0, 1)]:
                queue.append((r+dr, c+dc))
        # self.outline = new_outline

        self.blocks = new_outline

        # # for r,c in new_piece:
        # #     # Remove pieces directly below newly added pieces
        # #     if (r+1,c) in self.outline:
        # #         self.outline.remove((r+1,c))
        # # Remove surrounded blocks
        # for r,c in self.outline.copy():
        #     surrounded = True
        #     for dr, dc in itertools.product([-1, 1], repeat=2):
        #         if (r+dr, c+dc) not in self.outline and r+dr <= 0:
        #             surrounded = False
        #     if surrounded:
        #         self.outline.remove((r,c))

        # Remove blocks below complete rows
        # found_whole_row = 1
        # for r, c in self.blocks:
        #     if all([(r, cc) in self.blocks for cc in range(self.width)]):
        #         found_whole_row = min(found_whole_row, r)
        # if found_whole_row != 1:
        #     print("Before:", len(self.blocks))
        #     for r, c in self.blocks.copy():
        #         if r > found_whole_row:
        #             self.blocks.remove((r,c))
        #     print("After:", len(self.blocks))

        # blocks = self.blocks.copy()
        # self.blocks = blocks

    # def _update_outline(self, new_piece):
    #     # TODO: Remove inaccessible blocks below outline/top-surface
    #     # print("Outline:", list(sorted(list(self.outline), key=lambda blk: (blk[1], blk[0]))))
    #     for r,c in new_piece:
    #         self.outline.add((r,c))

    def draw(self, falling_piece=None, highest=-10):
        falling_piece = tuple(map(tuple, falling_piece))
        lowest = highest
        for r, _ in self.blocks:
            lowest = max(lowest, r)
        for r in range(highest, lowest+1):
            print(f"{r: <3}: ", end="")
            for c in range(0, 7):
                if falling_piece is not None and (r, c) in falling_piece:
                    print('@', end="")
                # elif (r, c) in self.outline:
                #     print('█', end="")
                elif (r, c) in self.blocks:
                    print('#', end="")
                else:
                    print('.', end="")

            print()
        print()


    def is_in(self, block):
        return block in self.blocks


class Piece:
    def __init__(self, blocks, position) -> None:
        self.blocks = blocks


def find_last_two_repetitions(listy):
    for size in range(1, 1 + len(listy)//2):
        # print(idx)
        # print(list(range(-1, -idx - 1, -1)))
        # print(list(range(-idx - 1, -idx - idx - 1, -1)))
        if listy[-1: -size - 1: -1] == listy[-size - 1: -size - size - 1: -1]:
            return size
    return None


# time python3 -m cProfile -s time main.py < test.txt
# 12:56 - part 2: 1535483869462 too low
# 13:54 - part 2: 1535483870924 (forgot to do extra steps after skip)
def main():
    lines = [line.replace("\n", "") for line in fileinput.input()]
    jet_pattern = lines[0]

    # row, col with bottom-left as 0,0
    pieces = [
        ((0, 0), (0, 1), (0, 2), (0, 3)),  # -
        ((-2, 1), (0, 1), (-1, 0), (-1, 2)),  # + (without center)
        ((0, 0), (0, 1), (0, 2), (-1, 2), (-2, 2)),  # inverse L
        ((-3, 0), (-2, 0), (-1, 0), (-0, 0)),  # |
        ((-1, 0), (-1, 1), (0, 0), (0, 1)),  # []
    ]
    curr_piece = 0
    highest = 0
    scene = Scene()
    push_count = 0
    start_time = time.time()

    # # Even just counting to this number would take 1 day at current speed
    # for i in range(1_000_000_000_000):
    #     if i % 100_000_000 == 0:
    #         print(f"{i:,} ({time.time() - start_time:.2f}s)")
    # exit()

    history = []
    max_steps = 1_000_000_000_000  # 2022, 1_000_000_000_000
    step = 0
    while step < max_steps:
        # print(step, highest)
        # if step % 10_000 == 0:
        #     print(f"{step:,} {len(scene.blocks)} ({time.time() - start_time:.2f}s)")

        start_pos = (highest - (3+1), 2)
        falling_piece = [list(blk) for blk in pieces[curr_piece]]
        move_piece(falling_piece, *start_pos)

        # simulate
        # if step >= 2011:  # if i == 178:
        #     print(step)
        #     scene.draw(falling_piece, highest - 7)
        #     # exit()

        # first gas push
        dir = jet_pattern[push_count]
        push_count = (push_count + 1) % len(jet_pattern)
        if not hit_sides(scene, falling_piece, dir):
            # print('push:', dir)
            move_piece(falling_piece, 0, 1 if dir == '>' else -1)

        height = start_pos[0]
        while not hit_scene_below(scene, falling_piece):  # (height < -1) and not 
            # scene.draw(falling_piece, highest - 7)

            # fall
            move_piece(falling_piece, +1, 0)
            height += 1

            # gas push
            dir = jet_pattern[push_count]
            push_count = (push_count + 1) % len(jet_pattern)
            if not hit_sides(scene, falling_piece, dir):
                move_piece(falling_piece, 0, 1 if dir == '>' else -1)
            #     scene.draw(falling_piece)
            # else:
            #     print('push fails:', dir)
        # scene.draw(falling_piece)

        # solidify piece into scene
        scene.add_piece(falling_piece)

        prev_highest = highest
        highest = min(highest, min(scene.top))

        # Faster not to clear blocks away every time:
        # - 1/100 - clear() dominates move()
        # - 1/10000 - move() takes very long
        # But since we have skipping code, we'd rather be safe
        # if len(scene.blocks) > 1_000:
        scene.clear_blocks()

        # next piece
        curr_piece = (curr_piece + 1) % len(pieces)
        step += 1

        # Look for repetition in height changes
        history.append(prev_highest - highest)
        rep_len = find_last_two_repetitions(history)
        # Short-cut simulation if repetitions found
        steps_left = max_steps - step
        if rep_len is not None and rep_len > 10 and steps_left > rep_len:
            repeated_sum = sum(history[-rep_len:])
            print(f"Found repeating every {rep_len} (each rep adds {repeated_sum})")
            offset = len(history) - 2*rep_len
            print(f"{len(history)} = {offset} + 2*{rep_len}")

            repeats_left = steps_left//rep_len
            print(f"{step}: {highest}")
            # Skip ahead
            jump_height = repeated_sum*repeats_left
            highest -= jump_height
            scene.move_up(jump_height)
            step += repeats_left * rep_len
            print(f"skip to {step}: {abs(highest)}")
            continue

    print(f"{abs(highest)} (full simulation)")


if __name__ == '__main__':
    main()
