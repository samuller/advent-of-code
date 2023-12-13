#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("../..")
from lib import *


def differences(str1, str2):
    assert len(str1) == len(str2)
    diffs = []
    for idx in range(len(str1)):
        if str1[idx] != str2[idx]:
            diffs.append(idx)
    return diffs


def find_smudged_reflection(lines):
    reflect_lines = []
    for split_line in range(len(lines)-1):
        offset = 0
        # Count lines that break reflection
        break_reflection = []
        while True:
            if lines[split_line - offset] != lines[split_line+1 + offset]:
                break_reflection.append(offset)
            offset += 1
            if ((split_line - offset) < 0) or ((split_line+1 + offset) > (len(lines) - 1)):
                offset -= 1
                break
        # print(f"{split_line}:", break_reflection)
        if len(break_reflection) == 1:
            offset = break_reflection[0]
            # Find smudges
            line1, line2 = lines[split_line - offset], lines[split_line+1 + offset]
            diffs = differences(line1, line2)
            # print(f"{diffs}:", line1, 'vs.', line2)
            if len(diffs) == 1:
                # print(f"{diffs}:", lines[split_line], 'vs.', lines[split_line+1])
                reflect_lines.append(split_line + 1)
    assert len(reflect_lines) <= 1, reflect_lines
    return reflect_lines


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
    ans2 = 0
    for group in grouped(lines):
        rows = [c for c in group]
        columns = []
        for cc in range(len(rows[0])):
            columns.append("".join([row[cc] for row in rows]))
        # print(rows)
        # print(columns)

        horz_refl = find_reflection(rows)
        vert_refl = find_reflection(columns)
        if len(horz_refl) == 1:
            ans1 += 100*horz_refl[0]
        if len(vert_refl) == 1:
            ans1 += vert_refl[0]
        # print(horz_refl, vert_refl)
        # Part 2
        horz_refl = find_smudged_reflection(rows)
        vert_refl = find_smudged_reflection(columns)
        if len(horz_refl) == 1:
            ans2 += 100*horz_refl[0]
        if len(vert_refl) == 1:
            ans2 += vert_refl[0]
        # print(horz_refl, vert_refl)
    print(ans1)
    print(ans2)


if __name__ == '__main__':
    main()
