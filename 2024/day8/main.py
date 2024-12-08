#!/usr/bin/env python3
from collections import defaultdict
import fileinput
from itertools import combinations


def print_nodes(freqs, max_rc):
    for r in range(0, max_rc[0]):
        for c in range(0, max_rc[1]):
            found = False
            for freq in freqs:
                nodes = freqs[freq]
                if (r, c) in nodes:
                    print(freq, end="")
                    found = True
                    break
            if not found:
                print(".", end="")
        print()


# 7:19 - 254 is wrong
# 7:40 - <= outer edge...
def main():
    lines = [line.strip() for line in fileinput.input()]

    antenna_locs = {}
    freqs = defaultdict(list)
    for r, row in enumerate(lines):
        for c, loc in enumerate(row):
            if loc != '.':
                antenna_locs[(r,c)] = loc
                freqs[loc].append((r, c))
    width = len(row)
    height = len(lines)
    # print(antenna_locs)
    # print(freqs)
    # print_nodes(freqs, (width, height))
    antinodes = set()
    for freq in freqs:
        antenna = freqs[freq]
        for pair in combinations(antenna, r=2):
            dr, dc = pair[0][0] - pair[1][0], pair[0][1] - pair[1][1]
            # Part 1
            pair_antinodes = [
                (pair[0][0] + dr, pair[0][1] + dc),
                (pair[1][0] - dr, pair[1][1] - dc),
            ]
            # Part 2
            pair_antinodes = set()
            # Forwards
            count = 1
            while True:
                rr = pair[0][0] + dr*count
                cc = pair[0][1] + dc*count
                if 0 <= rr < width and 0 <= cc < height:
                    pair_antinodes.add((rr, cc))
                    count += 1
                else:
                    break
            # Backwards
            count = 1
            while True:
                rr = pair[1][0] - dr*count
                cc = pair[1][1] - dc*count
                if 0 <= rr < width and 0 <= cc < height:
                    pair_antinodes.add((rr, cc))
                    count += 1
                else:
                    break

            # print(pair_antinodes)
            # new_freqs = freqs.copy()
            # new_freqs['*'] = pair_antinodes
            # print_nodes(new_freqs, (width, height))
            # print_nodes({freq: pair, '*': pair_antinodes}, (width, height))
            # input("continue?")
            for node in pair_antinodes:
                # Only those within bounds of map
                if 0 <= node[0] < width and 0 <= node[1] < height:
                    antinodes.add(node)
    # print(antinodes)
    # for freq in freqs:
    #     for node in freqs[freq]:
    #         if node in antinodes:
    #             antinodes.remove(node)

    # print(len(antinodes))
    # new_freqs = freqs.copy()
    # new_freqs['#'] = antinodes
    # print_nodes(new_freqs, (width, height))
    # Part 2
    # len(antinodes) + len(antenna_locs) - overlaps
    all_nodes = set(list(antinodes) + list(antenna_locs.keys()))
    print(len(all_nodes))


if __name__ == '__main__':
    main()
