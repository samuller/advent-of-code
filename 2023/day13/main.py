#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("../..")
from lib import *


class Classy:
    def __init__(self):
        pass


def find_reflection(lines):
    reflect_lines = []
    for split_line in range(len(lines)-1):
        offset = 0
        reflect = True
        while True:
            if lines[split_line - offset] != lines[split_line+1 + offset]:
                reflect = False
                break
            offset += 1
            if ((split_line - offset) < 0) or ((split_line+1 + offset) > (len(lines) - 1)):
                offset -= 1
                break
        # print(f"[{reflect}] {split_line} + {offset}:", lines[split_line - offset], 'vs.', lines[split_line+1 + offset])
        if reflect:
            reflect_lines.append(split_line + 1)
    assert len(reflect_lines) <= 1, reflect_lines
    return reflect_lines


def main():
    lines = [line.strip() for line in fileinput.input()]

    ans1 = 0
    for group in grouped(lines):
        rows = [c for c in group]
        columns = []
        for cc in range(len(rows[0])):
            columns.append("".join([row[cc] for row in rows]))
        print(rows)
        print(columns)

        horz_refl = find_reflection(rows)
        vert_refl = find_reflection(columns)
        if len(horz_refl) == 1:
            ans1 += 100*horz_refl[0]
        if len(vert_refl) == 1:
            ans1 += vert_refl[0]

        # horz_refl = []
        # for refl_cc in range(len(rows)-1):
        #     offset = 0
        #     reflect = True
        #     if rows[refl_cc - offset] != rows[refl_cc+1 + offset]:
        #         reflect = False
        #     if reflect:
        #         horz_refl.append(refl_cc + 1)
        # assert len(horz_refl) == 1, horz_refl
        
        # vert_refl = []
        # for refl_rr in range(len(columns)-1):
        #     offset = 0
        #      reflect = True
        #     if columns[refl_rr + offset = 0] != columns[refl_rr+1 + offset = 0]:
        #         reflect = False
        #     if reflect:
        #         vert_refl.append(refl_rr + 1)
        # assert len(vert_refl) == 1, vert_refl
        print(horz_refl, vert_refl)
    print(ans1)


if __name__ == '__main__':
    main()
