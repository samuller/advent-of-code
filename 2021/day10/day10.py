#!/usr/bin/env python3
import fileinput
from collections import defaultdict, deque


def main():
    lines = [line.strip() for line in fileinput.input()]
    print(f'Lines: {len(lines)}')

    open = ['(','[','{','<']
    close = [')',']','}','>']
    costs = {
        ')': 3,
        ']': 57,  # 3*19
        '}': 1197,  # 3*19*21
        '>': 25137  # 3*19*21*21
    }
    completion_costs = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4
    }
    p1 = 0
    p2_scores = []
    for line in lines:
        # brackets = defaultdict(int)
        valid = True
        opening = deque()  # stack
        score = 0
        for chr in line:
            assert chr in open or chr in close
            if chr in open:
                opening.append(chr)
                # brackets[open.index(chr)] += 1
            elif chr in close:
                last = opening.pop()
                last_idx = open.index(last)
                # Corrupt
                if close.index(chr) != last_idx:
                    valid = False
                    p1 += costs[chr]
                    break
                # brackets[close.index(chr)] -= 1
            else:
                print(chr)
                assert False
            # print(opening)
        if not valid:
            # print(line)
            pass
        else:
            # print(opening)
            line_score = 0
            while opening:
                last = opening.pop()
                last_idx = open.index(last)
                close_char = close[last_idx]
                # print(close_char,end="")
                line_score *= 5
                line_score += completion_costs[close_char]
            # print()
            p2_scores.append(line_score)
        # exit()
        # if 0 in brackets.values():
        #     # corrupt
        #     print(line, brackets)
    print(p1)
    # print(p2_scores)
    p2 = sorted(p2_scores)[len(p2_scores)//2]
    print(p2)


if __name__ == '__main__':
    main()
