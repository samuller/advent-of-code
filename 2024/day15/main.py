#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("../..")
from lib import *


def create_map(dimensions, robot, walls, boxes):
    rows, cols = dimensions
    map = Map2D()
    map.load_from_data(["".join(['.' for _ in range(cols)]) for _ in range(rows)])
    for rr in range(map.rows):
        for cc in range(map.cols):
            if (rr, cc) == robot:
                map.set(rr, cc, '@')
            elif (rr, cc) in walls:
                map.set(rr, cc, '#')
            elif (rr, cc) in boxes:
                map.set(rr, cc, 'O')
    return map


def create_map_p2(dimensions, robot, walls, boxes):
    """Part2: create a "doubled-up" map."""
    rows, cols = dimensions
    map = Map2D()
    map.load_from_data(["".join(['.' for _ in range(cols*2)]) for _ in range(rows)])
    for rr in range(map.rows):
        for cc in range(map.cols):
            if (rr, cc) == robot:
                map.set(rr, cc, '@')
            elif (rr, cc) in walls:
                map.set(rr, cc, '#')
                map.set(rr, cc+1, '#')
            elif (rr, cc) in boxes:
                map.set(rr, cc, '[')
                map.set(rr, cc+1, ']')
    return map


def collides_with_obj2(pos, obj):
    if pos == obj:
        return True
    if pos == (obj[0], obj[1]+1):
        return True
    return False


def extract_from_map(map, p2=False):
    robot = None
    walls = set()
    boxes = []
    for rr in range(map.rows):
        for cc in range(map.cols):
            nr, nc = rr, cc
            if p2:
                nr, nc = rr, cc*2
            if map[rr, cc] == '@':
                assert robot is None
                robot = (nr, nc)
            elif map[rr, cc] == '#':
                walls.add((nr, nc))
            elif map[rr, cc] == 'O':
                boxes.append((nr, nc))
            else:
                assert map[rr, cc] == '.'
    return robot, walls, boxes


def update_physics(robot, robot_move, walls, boxes):
    move = robot_move
    next_loc = (robot[0] + move[0], robot[1] + move[1])
    boxes_to_move_idx = set()
    boxes_prevent_movement = False
    peek_loc = next_loc
    while True:
        if peek_loc in walls:
            if len(boxes_to_move_idx) > 0:
                boxes_prevent_movement = True
            boxes_to_move_idx = []
            break
        if peek_loc in boxes:
            boxes_to_move_idx.add(boxes.index(peek_loc))
        else:
            break
        peek_loc = (peek_loc[0] + move[0], peek_loc[1] + move[1])
    # print(boxes_to_move_idx)
    for box_idx in boxes_to_move_idx:
        box = boxes[box_idx]
        boxes[box_idx] = (box[0] + move[0], box[1] + move[1])
    if next_loc not in walls and not boxes_prevent_movement:
        robot = next_loc
    return robot, walls, boxes


def update_physics_p2(robot, robot_move, walls, boxes):
    """Part 2: update physics for larger boxes and walls."""
    move = robot_move
    next_loc = (robot[0] + move[0], robot[1] + move[1])
    boxes_to_move_idx = set()
    boxes_prevent_movement = False
    # Part 2
    peek_locs = [next_loc]
    while len(peek_locs) > 0:
        # print(peek_locs)
        peek_loc = peek_locs.pop()
        walls_hit = []
        for idx, wall in enumerate(walls):
            if collides_with_obj2(peek_loc, wall):
                walls_hit.append(wall)
        if len(walls_hit) > 0:
            assert len(walls_hit) == 1
            boxes_prevent_movement = True
            boxes_to_move_idx = set()
            break
        collisions = False
        for idx, box in enumerate(boxes):
            if collides_with_obj2(peek_loc, box):
                boxes_to_move_idx.add(idx)
                # Moving up/down
                if move[0] != 0:
                    peek_locs.append((box[0] + move[0], box[1] + move[1]))
                    peek_locs.append((box[0] + move[0], box[1] + 1 + move[1]))
                else:
                    peek_locs.append((peek_loc[0] + move[0], peek_loc[1] + move[1]))
                assert collisions == False
                collisions = True
    # print(boxes_to_move_idx)
    for box_idx in boxes_to_move_idx:
        box = boxes[box_idx]
        boxes[box_idx] = (box[0] + move[0], box[1] + move[1])
    if next_loc not in walls and not boxes_prevent_movement:
        robot = next_loc
    return robot, walls, boxes


def ins_to_mov(ins):
    """Convert instruction into move direction."""
    move = None
    if ins == '<':
        move = (0,-1)
    elif ins ==  '>':
        move = (0,+1)
    elif ins ==  '^':
        move = (-1,0)
    elif ins ==  'v':
        move = (+1,0)
    return move  


def main():
    lines = [line.strip() for line in fileinput.input()]
    groups = list(grouped(lines))
    map = Map2D()
    map.load_from_data(groups[0])
    instructions = "".join(groups[1])
    # print(map)
    # print(instructions)
    robot, walls, boxes = extract_from_map(map, p2=False)
    # print(create_doubled_map((map.rows, map.cols), robot, walls, boxes))
    # print(robot, boxes, walls)
    for ins in instructions:
        assert ins in ['<', '>', 'v', '^']
        # print(create_map((map.rows, map.cols), robot, walls, boxes))
        # print(f"Step {ins}:")
        robot, walls, boxes = update_physics(robot, ins_to_mov(ins), walls, boxes)
    # print(robot)
    p1 = 0
    for box in boxes:
        p1 += box[0]*100 + box[1]
    print(p1)
    # Part 2
    robot, walls, boxes = extract_from_map(map, p2=True)
    for ins in instructions:
        assert ins in ['<', '>', 'v', '^']
        # print(create_doubled_map((map.rows, map.cols), robot, walls, boxes))
        # print(f"Step {ins}:")
        robot, walls, boxes = update_physics_p2(robot, ins_to_mov(ins), walls, boxes)
    p2 = 0
    for box in boxes:
        p2 += box[0]*100 + box[1]
    print(p2)


if __name__ == '__main__':
    main()
