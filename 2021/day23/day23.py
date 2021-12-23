#!/usr/bin/env python3
import fileinput
# import sys; sys.path.append("../..")
# from lib import *


MOVE_COST = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}


def in_place(pods):
    return pods == [['A', 'A'], ['B', 'B'], ['C', 'C'], ['D', 'D']]


# 12422 @ 7:33
# 11421 @ 7:37
def main():
    lines = [line.strip() for line in fileinput.input()]
    assert len(lines) == 5
    assert len(lines[1]) == 13
    hallway_spots = 11 - 4
    # Example
    pods_start = [['A1', 'B1'], ['D1', 'C1'], ['C2', 'B2'], ['A2', 'D2']]
    # Actual
    # pods_start = [['B1', 'B2'], ['C1', 'A1'], ['D1', 'A2'], ['C2', 'D2']]
    
    # Borrow: Hallway (h), Side rooms (s)
    # All numbered left to right
    # #############
    # #hh.h.h.h.hh#
    # ###s#s#s#s###
    #   #s#s#s#s#
    #   #########
    network = [
        ('s1lower', 's1upper', 1),
        ('s2lower', 's2upper', 1),
        ('s3lower', 's3upper', 1),
        ('s4lower', 's4upper', 1),
        ('s1upper', 'h2', 2),
        ('s1upper', 'h3', 2),
        ('s2upper', 'h3', 2),
        ('s2upper', 'h4', 2),
        ('s3upper', 'h4', 2),
        ('s3upper', 'h5', 2),
        ('s4upper', 'h5', 2),
        ('s4upper', 'h6', 2),
        ('h1', 'h2', 1),
        ('h2', 'h3', 2),
        ('h3', 'h4', 2),
        ('h4', 'h5', 2),
        ('h5', 'h6', 2),
        ('h6', 'h7', 1),
    ]
    waiting_spot = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7']
    pods_start = [
        ['b1lower', 'b1upper'],
        ['b2lower', 'b2upper'], 
        ['b3lower', 'b3upper'], 
        ['b4lower', 'b4upper']
    ]
    # pods_pos
    # while not in_place(pods):
    #     pass

    #
    # Manual
    #

    #
    # #############
    # #...........#
    # ###B#A#A#D###
    #   #B#C#D#C#
    #   #########
    # Optimal (phasing) - 11211
    moves = [
        [5, 'A'], # end
        [6, 'A'], # end
        [5, 'B'], # end
        [5, 'B'], # end
        [6, 'C'], # end
        [5, 'C'], # end
        [5, 'D'], # out & end
        [5, 'D'], # end
    ]
    #
    # AA..v.v
    #   B#C#D#
    #
    # 11421
    moves = [
        [4, 'A'], # left
        [3, 'C'], # right
        [5, 'B'], # end - opt
        [5, 'B'], # end - opt
        [3, 'A'], # end - opt+2
    #
    # #############
    # #.....C.....#
    # ###.#B#A#D###
    #   #A#B#D#C#
    #   #########
        [5, 'A'], # right
        [2, 'D'], # left
        [3, 'C'], # right
        [3, 'D'], # end - opt
        [5, 'D'], # end - opt (out & back)
        [3, 'C'], # end - opt
        [4, 'C'], # end - opt + 2
        [9, 'A'], # end
    ]

    # Alternate start - 11417
    moves = [
        [5, 'A'], # left
        [6, 'A'], # left
        [2, 'D'], # right
        [5, 'C'], # left
        [3, 'D'], # end
    #
    # #############
    # #AA...C.....#
    # ###B#.#.#.###
    #   #B#C#D#D#
    #   #########
        [5, 'D'], # end
        [3, 'C'], # end
        [5, 'C'], # end
        [5, 'B'], # end - opt
        [5, 'B'], # end - opt
        [3, 'A'], # end
        [3, 'A'], # end
    ]

    # Example
    # moves = [
    #     [4, 'B'], # left
    #     [4, 'C'], # end
    #     [3, 'D'], # end
    #     [3, 'B'], # end
    #     [4, 'B'], # end
    #     [2, 'D'], # end
    #     [3, 'A'], # right
    #     [3, 'D'], # end
    #     [4, 'D'], # end
    #     [8, 'A'], # end
    # ]
    cost = 0
    for move in moves:
        cost += move[0] * MOVE_COST[move[1]]
    print(cost)


if __name__ == '__main__':
    main()
