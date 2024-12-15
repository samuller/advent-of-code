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


def create_doubled_map(dimensions, robot, walls, boxes):
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
            # Part2
            r2, c2 = rr, cc*2
            if map[rr, cc] == '@':
                assert robot is None
                # robot = (rr, cc)
                robot = (r2, c2)
            elif map[rr, cc] == '#':
                # walls.add((rr, cc))
                walls.add((r2, c2))
            elif map[rr, cc] == 'O':
                # boxes.append((rr, cc))
                boxes.append((r2, c2))
            else:
                assert map[rr, cc] == '.'
    # print(create_doubled_map((map.rows, map.cols), robot, walls, boxes))
    # print(robot, boxes, walls)
    for ins in instructions:
        assert ins in ['<', '>', 'v', '^']
        move = None
        # print(create_doubled_map((map.rows, map.cols), robot, walls, boxes))
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
        boxes_to_move_idx = set()
        boxes_prevent_movement = False
        # Part 1
        # peek_loc = next_loc
        # while True:
        #     if peek_loc in walls:
        #         if len(boxes_to_move_idx) > 0:
        #             boxes_prevent_movement = True
        #         boxes_to_move_idx = []
        #         break
        #     if peek_loc in boxes:
        #         boxes_to_move_idx.append(boxes.index(peek_loc))
        #     else:
        #         break
        #     peek_loc = (peek_loc[0] + move[0], peek_loc[1] + move[1])
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

            # # Consider both sides of each object (location is left-side)
            # peek2_loc = (peek_loc[0], peek_loc[1]-1)
            # if peek_loc in walls or peek2_loc in walls:
            #     if len(boxes_to_move_idx) > 0:
            #         boxes_prevent_movement = True
            #         boxes_to_move_idx = []
            #         break
            # if peek_loc in boxes:
            #     boxes_to_move_idx.append(boxes.index(peek_loc))
            #     peek_locs.append((peek_loc[0] + move[0], peek_loc[1] + move[1]))
            #     if move[0] != 0:
            #         peek_locs.append((peek_loc[0] + move[0], peek_loc[1] + 1 + move[1]))
            # elif peek2_loc in boxes:
            #     # box2_loc = (peek2_loc[0], peek2_loc[1])
            #     boxes_to_move_idx.append(boxes.index(peek2_loc))
            #     peek_locs.append((peek2_loc[0] + move[0], peek2_loc[1] + move[1]))
            #     if move[0] != 0:
            #         peek_locs.append((peek2_loc[0] + move[0], peek2_loc[1] + 1 + move[1]))
            # # ELSE?
            # assert not (peek_loc in boxes and peek2_loc in boxes)
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
    p2 = 0
    for box in boxes:
        side = box[1]
        # # If closer to right half
        # if side + 1 > map.cols:
        #     side += 1
        p2 += box[0]*100 + side
    print(p2)

        # match ins:
        #     case '<': move = (0,-1)
        #     case '>': move = (0,+1)
        #     case '^': move = (-1,0)
        #     case 'v': move = (+1,0)


if __name__ == '__main__':
    main()
