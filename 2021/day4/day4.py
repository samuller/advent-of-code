#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("../..")
from lib import grouped, ANSIColor
from collections import namedtuple


BOARD_SIZE = 5
BingoMatch = namedtuple('BingoMatch', ['board_idx', 'row_matches', 'col_matches'])


def parse_boards(lines):
    boards = list(grouped(lines))
    for board_idx, board in enumerate(boards):
        # Convert to numbers
        boards[board_idx] = [[int(val) for val in row.split(' ') if val != ''] for row in board]
    return boards


def print_boards(boards, markers=None, highlight=None):
    width = 2 # if markers is None else 4
    for board_idx, board in enumerate(boards):
        for row_idx, row in enumerate(board):
            for col_idx, val in enumerate(row):
                if highlight is not None and highlight(board_idx, row_idx, col_idx):
                    print(f'{ANSIColor.YELLOW}{val:>{width}}{ANSIColor.END} ', end='')
                elif markers is not None and (board_idx, row_idx, col_idx) in markers:
                    # box = f'[{val}]'
                    # print(f'{box:>{width}} ', end='')
                    print(f'{ANSIColor.RED}{val:>{width}}{ANSIColor.END} ', end='')
                else:
                    print(f'{val:>{width}} ', end='')
            print()
        print()


def find_bingos(boards, markers):
    bingo_matches = []
    for board_idx, _ in enumerate(boards):
        # Count matches per column
        col_matches = []
        for col in range(BOARD_SIZE):
            row_set = set([r for (b,r,c) in markers if b == board_idx and c == col])
            col_matches.append(len(row_set))
        # Count matches per row
        row_matches = []
        for row in range(BOARD_SIZE):
            col_set = set([c for (b,r,c) in markers if b == board_idx and r == row])
            row_matches.append(len(col_set))

        if BOARD_SIZE in row_matches or BOARD_SIZE in col_matches:
            bingo_matches.append(BingoMatch(board_idx, row_matches, col_matches))
    return bingo_matches


def mark_locations(boards, ball):
    latest_markers = []
    for board_idx, board in enumerate(boards):
        for row_idx, row in enumerate(board):
            for col_idx, val in enumerate(row):
                if val == ball:
                    latest_markers.append((board_idx, row_idx, col_idx))
    # print(markers)
    # print_boards(boards, markers)
    return latest_markers


def sum_unmarked(boards, winning_board_idx, markers):
    summ = 0
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if (winning_board_idx, row, col) in markers:
                continue
            summ += boards[winning_board_idx][row][col]
            # print(boards[winning_board_idx][row][col])
    return summ


def print_winner(boards, markers, winning_board_match):
    bingo_board_idx = winning_board_match.board_idx
    print(f'Bingo on board {bingo_board_idx+1}!')
    if BOARD_SIZE in winning_board_match.row_matches:
        bingo_row_idx = winning_board_match.row_matches.index(BOARD_SIZE)
        print_boards([boards[bingo_board_idx]], markers, highlight=lambda b,r,c: r == bingo_row_idx)
    if BOARD_SIZE in winning_board_match.col_matches:
        bingo_col_idx = winning_board_match.col_matches.index(BOARD_SIZE)
        print_boards([boards[bingo_board_idx]], markers, highlight=lambda b,r,c: c == bingo_col_idx)


def get_last_new_value_added(listy):
    """Returns index of the last new value added.
    
    A "new" value is any value that has not been seen earlier in the list.
    """
    last_added = None
    last_added_idx = None
    for idx, val in enumerate(listy):
        if val not in listy[:idx]:
            last_added = val
            last_added_idx = idx
    return last_added_idx


def main():
    lines = [line.strip() for line in fileinput.input()]
    print(f'Lines: {len(lines)}')

    part1 = True

    balls = [int(num) for num in lines[0].split(',')]
    print(balls)
    boards = parse_boards(lines[2:])
    print_boards(boards)

    markers = []
    bingo_matches = []
    for ball in balls:
        print(f'Pull {ANSIColor.BLUE}{ball}{ANSIColor.END}')
        # Mark matching locations
        latest_markers = mark_locations(boards, ball)
        markers.extend(latest_markers)
        # Find BINGOs 
        all_bingos = find_bingos(boards, markers)
        if len(all_bingos) > 0:
            print(*all_bingos, sep='\n')
        # add bingos to track progress (although we re-add ALL bingos, not just newest ones)
        bingo_matches.extend(all_bingos)
        # Part 1 - stop at first win
        if part1 and len(bingo_matches) > 0:
            break
        # Part 2 - stop once all boards have a win
        uniq_bingo_boards = set([b.board_idx for b in bingo_matches])
        if len(uniq_bingo_boards) == len(boards):
            break
    print()

    # Part 1
    winning_board_match = bingo_matches[0]
    # Part 2
    if not part1:
        win_boards = [b.board_idx for b in bingo_matches]
        last_added_idx = get_last_new_value_added(win_boards)
        last_added = win_boards[last_added_idx]
        winning_board_match = bingo_matches[last_added_idx]

    print_winner(boards, markers, winning_board_match)
    summ = sum_unmarked(boards, winning_board_match.board_idx, markers)
    print(summ, ball)
    print(summ * ball)


if __name__ == '__main__':
    main()
