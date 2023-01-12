#!/usr/bin/env python3
import fileinput
from dataclasses import dataclass
from collections import namedtuple

import sys; sys.path.append("../..")
from lib import *


def get_loc(mapp, pos):
    row_line = mapp[pos.row]
    return row_line[pos.column]


@dataclass
class Pos:
    row: int  # absolute
    column: int  # relative to offset
    facing: str


def get_offsets(full_col):
    offsets = [0, 0]  # [before ,after]
    idx = 0
    for ch in full_col:
        if ch == " ":
            offsets[idx] += 1
        else:
            idx = 1
    return offsets

# Part 1
# def move_forwards(mapp, curr_pos, count):
#     line = mapp[curr_pos.row % len(mapp)]
#     offsets = get_offsets(line)
#     diff = len(line.strip())  #len(line) - (offsets[0] + offsets[1])
#     # assert diff == len(line.strip()), f"{offsets} -> {diff} '{line.strip()}'"
#     if curr_pos.facing == '<':
#         for _ in range(count):
#             prev = curr_pos.column
#             curr_pos.column = (curr_pos.column - 1)
#             if curr_pos.column < offsets[0]:
#                 curr_pos.column = offsets[0] + diff - 1
#             elif curr_pos.column >= offsets[0] + diff:
#                 curr_pos.column = offsets[0]
#             if line[curr_pos.column] == "#":
#                 curr_pos.column = prev
#                 break
#         return
#     if curr_pos.facing == '>':
#         for _ in range(count):
#             prev = curr_pos.column
#             curr_pos.column = (curr_pos.column + 1)
#             if curr_pos.column < offsets[0]:
#                 curr_pos.column = offsets[0] + diff - 1
#             elif curr_pos.column >= offsets[0] + diff:
#                 curr_pos.column = offsets[0]
#             if line[curr_pos.column] == "#":
#                 curr_pos.column = prev
#                 break
#         return

#     full_col = [line[curr_pos.column] if len(line) > curr_pos.column else " " for line in mapp]
#     offsets = get_offsets(full_col)
#     # print(full_col)
#     diff = len("".join(full_col).strip())  #len(line) - (offsets[0] + offsets[1])
#     # assert diff == len("".join(full_col).strip())
#     if curr_pos.facing == '^':
#         for _ in range(count):
#             prev = curr_pos.row
#             curr_pos.row = (curr_pos.row - 1)
#             if curr_pos.row < offsets[0]:
#                 curr_pos.row = offsets[0] + diff - 1
#             elif curr_pos.row >= offsets[0] + diff:
#                 curr_pos.row = offsets[0]
#             # print(curr_pos.row+1, diff, offsets, curr_pos.row, full_col)
#             if full_col[curr_pos.row] == "#":
#                 curr_pos.row = prev
#                 break
#         return
#     if curr_pos.facing == 'v':
#         for _ in range(count):
#             prev = curr_pos.row
#             curr_pos.row = (curr_pos.row + 1)
#             if curr_pos.row < offsets[0]:
#                 curr_pos.row = offsets[0] + diff - 1
#             elif curr_pos.row >= offsets[0] + diff:
#                 curr_pos.row = offsets[0]
#             if full_col[curr_pos.row] == "#":
#                 curr_pos.row = prev
#                 break
#         return

# Part 2 - 3D!
def move_forwards(mapp, curr_pos, count):
    line = mapp[curr_pos.row % len(mapp)]
    offsets = get_offsets(line)
    diff = len(line.strip())  #len(line) - (offsets[0] + offsets[1])
    # assert diff == len(line.strip()), f"{offsets} -> {diff} '{line.strip()}'"
    if curr_pos.facing == '<':
        for _ in range(count):
            prev = curr_pos.column
            curr_pos.column = (curr_pos.column - 1)
            if curr_pos.column < offsets[0]:
                curr_pos.column = offsets[0] + diff - 1
            elif curr_pos.column >= offsets[0] + diff:
                curr_pos.column = offsets[0]
            if line[curr_pos.column] == "#":
                curr_pos.column = prev
                break
        return
    if curr_pos.facing == '>':
        for _ in range(count):
            prev = curr_pos.column
            curr_pos.column = (curr_pos.column + 1)
            if curr_pos.column < offsets[0]:
                curr_pos.column = offsets[0] + diff - 1
            elif curr_pos.column >= offsets[0] + diff:
                curr_pos.column = offsets[0]
            if line[curr_pos.column] == "#":
                curr_pos.column = prev
                break
        return

    full_col = [line[curr_pos.column] if len(line) > curr_pos.column else " " for line in mapp]
    offsets = get_offsets(full_col)
    # print(full_col)
    diff = len("".join(full_col).strip())  #len(line) - (offsets[0] + offsets[1])
    # assert diff == len("".join(full_col).strip())
    if curr_pos.facing == '^':
        for _ in range(count):
            prev = curr_pos.row
            curr_pos.row = (curr_pos.row - 1)
            if curr_pos.row < offsets[0]:
                curr_pos.row = offsets[0] + diff - 1
            elif curr_pos.row >= offsets[0] + diff:
                curr_pos.row = offsets[0]
            # print(curr_pos.row+1, diff, offsets, curr_pos.row, full_col)
            if full_col[curr_pos.row] == "#":
                curr_pos.row = prev
                break
        return
    if curr_pos.facing == 'v':
        for _ in range(count):
            prev = curr_pos.row
            curr_pos.row = (curr_pos.row + 1)
            if curr_pos.row < offsets[0]:
                curr_pos.row = offsets[0] + diff - 1
            elif curr_pos.row >= offsets[0] + diff:
                curr_pos.row = offsets[0]
            if full_col[curr_pos.row] == "#":
                curr_pos.row = prev
                break
        return


DIR_TO_NUM = {'>': 0, 'v': 1, '<': 2, '^': 3}
NUM_TO_DIR = {0: '>', 1: 'v', 2: '<', 3: '^'}


def shift_facing(curr_pos, dir):
    num_facing = DIR_TO_NUM[curr_pos.facing]
    if dir == 'R':
        num_facing = (num_facing + 1) % 4
        curr_pos.facing = NUM_TO_DIR[num_facing]
    elif dir == 'L':
        num_facing = (num_facing - 1) % 4
        curr_pos.facing = NUM_TO_DIR[num_facing]
    else:
        assert False


def print_on_map(mapp, pos):
    for row, line in enumerate(mapp):
        if row != pos.row:
            print(line)
            continue
        # Print row char-by-char
        for col, ch in enumerate(line):
            if pos.column == col:
                print(pos.facing, end="")
            else:
                print(ch, end="")
        print()
    print()

# 8:37 - cubed!
def main():
    lines = [line.replace("\n", "") for line in fileinput.input()]
    print(lines)
    groups = grouped(lines)
    mapp = next(groups)

    instruction_str = next(groups)[0]
    instructions = []
    curr_num = ""
    for ch in instruction_str:
        if ch.isdigit():
            curr_num += ch
            continue
        if curr_num != "":
            instructions.append(int(curr_num))
            curr_num = ""
        instructions.append(ch)
    if curr_num != "":
        instructions.append(int(curr_num))
    print(instructions)

    # Starting position
    curr = Pos(row=0, column=get_offsets(mapp[0])[0], facing='>')
    for cnt, ins in enumerate(instructions):
        print(f"{cnt}: [{ins}]")
        # print_on_map(mapp, curr)
        loc = get_loc(mapp, curr)
        assert loc not in ['#', ' ']
        if type(ins) == int:
            move_forwards(mapp, curr, ins)
        else:
            shift_facing(curr, ins)
        # if cnt == 1:
        #     print_on_map(mapp, curr)
        #     exit()
    # print_on_map(mapp, curr)

    password = 1000*(curr.row + 1) + 4*(curr.column + 1) + DIR_TO_NUM[curr.facing]
    print(password)

if __name__ == '__main__':
    main()
