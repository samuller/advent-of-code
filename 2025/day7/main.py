#!/usr/bin/env python3
from collections import defaultdict
import fileinput
# import sys; sys.path.append("../..")
# from lib import *


def main():
    lines = [line.strip() for line in fileinput.input()]
    splitters = defaultdict(list)
    for row_idx, line in enumerate(lines):
        for col_idx, chr in enumerate(line):
            if chr == '^':
                splitters[row_idx].append(col_idx)
    # print(splitters)

    p1 = 0
    # p2 = 1
    start = lines[0].index("S")
    beams = set([start])
    # Part 2 - slow & memory  (memory crash)
    # paths = set([(start,)])
    # Part 2 - faster & less memory, but still might crash much later? (started 7:20)
    # - only ran for 19.5mins before approach 3 was completed
    # path_ends = [start]
    # Part 2 - more faster (started 7:36)
    timeline_ends = defaultdict(int)
    timeline_ends[start] = 1
    for row_idx in splitters:
        # print(row_idx, len(beams), len(timeline_ends))
        # print(timeline_ends)
        new_beams = set()
        # new_paths = set()
        # new_path_ends = []
        new_timeline_ends = defaultdict(int)
        splitters_in_row = splitters[row_idx]
        for beam in beams:
            if beam not in splitters_in_row:
                new_beams.add(beam)
                # for path in paths:
                #     if path[-1] == beam:
                #         new_paths.add((*path, beam))
                # for end in path_ends:
                #     if end == beam:
                #         new_path_ends.append(beam)
                #         # p2 += 1 * p2
                for end in timeline_ends:
                    if end == beam:
                        new_timeline_ends[end] += timeline_ends[end]
            else:
                p1 += 1
                new_beams.add(beam-1)
                new_beams.add(beam+1)
                # for path in paths:
                #     if path[-1] == beam:
                #         new_paths.add((*path, beam-1))
                #         new_paths.add((*path, beam+1))
                # for end in path_ends:
                #     if end == beam:
                #         new_path_ends.append(beam-1)
                #         new_path_ends.append(beam+1)
                #        # p2 += 2 * p2
                for end in timeline_ends:
                    if end == beam:
                        new_timeline_ends[beam-1] += timeline_ends[end]
                        new_timeline_ends[beam+1] += timeline_ends[end]
            # for splitter in splitters_in_row:
        beams = new_beams
        # paths = new_paths
        # path_ends = new_path_ends
        # p2 += len(path_ends) * p2
        timeline_ends = new_timeline_ends
    print(p1)
    # print(paths)
    # for path in sorted(list(paths)):
    #     print(path)
    # print(len(paths))
    # print(len(path_ends))
    # print(p2)
    print(sum(new_timeline_ends.values()))


if __name__ == '__main__':
    main()
