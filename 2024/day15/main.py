#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("../..")
from lib import *


def create_map(dimensions, robot, walls, boxes):
    rows, cols = dimensions
    map = Map2D()
    map.load_from_data([['.' for _ in range(cols)] for _ in range(rows)])
    for rr in range(map.rows):
        for cc in range(map.cols):
            if (rr, cc) == robot:
                map.set(rr, cc, '@')
            elif (rr, cc) in walls:
                map.set(rr, cc, '#')
            elif (rr, cc) in boxes:
                map.set(rr, cc, 'O')
    return map


def main():
    lines = [line.strip() for line in fileinput.input()]
    groups = list(grouped(lines))
    map = Map2D()
    map.load_from_data(groups[0])
    instructions = "".join(groups[1])
    # print(map)
    # print(instructions)
    robot = None
    walls = set()
    boxes = []
    for rr in range(map.rows):
        for cc in range(map.cols):
            if map[rr, cc] == '@':
                assert robot is None
                robot = (rr, cc)
            elif map[rr, cc] == '#':
                walls.add((rr, cc))
            elif map[rr, cc] == 'O':
                boxes.append((rr, cc))
            else:
                assert map[rr, cc] == '.'
    # print(robot, boxes, walls)
    for ins in instructions:
        assert ins in ['<', '>', 'v', '^']
        move = None
        # print(create_map((map.rows, map.cols), robot, walls, boxes))
        # print(f"Step {ins}:")
        if ins == '<':
            move = (0,-1)
        elif ins ==  '>':
            move = (0,+1)
        elif ins ==  '^':
            move = (-1,0)
        elif ins ==  'v':
            move = (+1,0)
        next_loc = (robot[0] + move[0], robot[1] + move[1])
        boxes_to_move_idx = []
        boxes_prevent_movement = False
        peek_loc = next_loc
        while True:
            if peek_loc in walls:
                if len(boxes_to_move_idx) > 0:
                    boxes_prevent_movement = True
                boxes_to_move_idx = []
                break
            if peek_loc in boxes:
                boxes_to_move_idx.append(boxes.index(peek_loc))
            else:
                break
            peek_loc = (peek_loc[0] + move[0], peek_loc[1] + move[1])
        # print(boxes_to_move_idx)
        for box_idx in boxes_to_move_idx:
            box = boxes[box_idx]
            boxes[box_idx] = (box[0] + move[0], box[1] + move[1])
        if next_loc in walls or boxes_prevent_movement:
            continue
        robot = next_loc
    # print(robot)
    p1 = 0
    for box in boxes:
        p1 += box[0]*100 + box[1]
    print(p1)

        # match ins:
        #     case '<': move = (0,-1)
        #     case '>': move = (0,+1)
        #     case '^': move = (-1,0)
        #     case 'v': move = (+1,0)


if __name__ == '__main__':
    main()
