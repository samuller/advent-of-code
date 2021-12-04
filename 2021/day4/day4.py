#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("../..")
from lib import grouped


def main():
    lines = [line.strip() for line in fileinput.input()]
    print(f'Lines: {len(lines)}')

    balls = [int(num) for num in lines[0].split(',')]
    print(balls)
    boards = list(grouped(lines[2:]))
    print(boards)
    # Convert to numbers
    for board_idx, board in enumerate(boards):
        boards[board_idx] = [[int(val) for val in row.split(' ')] for row in board]
    print(boards)

    markers = []
    bingo_board_idx = None
    bingo_row_idx = None
    bingo_col_idx = None
    bingo_boards = set()
    last_new_added = None
    for ball in balls:
        print(ball)
        for board_idx, board in enumerate(boards):
            for row_idx, row in enumerate(board):
                values = row # [num for num in row.split(' ')]  
                for col_idx, val in enumerate(values):
                    if val == ball:
                        markers.append((board_idx, row_idx, col_idx))
        # print(markers)
        for board_idx, _ in enumerate(boards):
            board_marks = [mark for mark in markers if mark[0] == board_idx]

            for col in range(5):
                row_set = set([r for (b,r,c) in markers if b == board_idx and c == col])
                if row_set == set(range(5)):
                    print(f'Col bingo on board {board_idx} & col {col}')
                    bingo_board_idx = board_idx
                    bingo_col_idx = col
                    break
            
            for row in range(5):
                col_set = set([c for (b,r,c) in markers if b == board_idx and r == row])
                if col_set == set(range(5)):
                    print(f'Row bingo on board {board_idx} & row {row}')
                    # print([(b,row,c) for (b,row,c) in markers if b == board_idx])
                    bingo_board_idx = board_idx
                    bingo_row_idx = row
                    break

            # Part 1
            # if bingo_board_idx is not None:
            #     break
            # Part 2
            if bingo_board_idx is not None:
                if bingo_board_idx not in bingo_boards:
                    last_new_added = bingo_board_idx
                bingo_boards.add(bingo_board_idx)
        # Part 1
        # if bingo_board_idx is not None:
        #     break
        # Part 2
        if len(bingo_boards) == len(boards):
            bingo_board_idx = last_new_added
            break

    print(f'Bingo on {bingo_board_idx}!')
    print(boards[bingo_board_idx])
    if bingo_row_idx is not None:
        bingo_markers = [(b,r,c) for (b,r,c) in markers if b == bingo_board_idx and r == bingo_row_idx]
        print(bingo_markers)
    if bingo_col_idx is not None:
        bingo_markers = [(b,r,c) for (b,r,c) in markers if b == bingo_board_idx and c == bingo_col_idx]
        print(bingo_markers)

    summ = 0
    for row in range(5):
        for col in range(5):
            if (bingo_board_idx, row, col) in markers:
                continue
            summ += boards[bingo_board_idx][row][col]
            # print(boards[bingo_board_idx][row][col])
    print(summ, ball)
    print(summ * ball)


if __name__ == '__main__':
    main()
