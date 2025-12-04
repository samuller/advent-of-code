#!/usr/bin/env python3
import fileinput
# import sys; sys.path.append("../..")
# from lib import *


def part1(lines):
    p1 = 0
    for line in lines:
        bank = [int(chr) for chr in line]
        largest_seen = 0
        second_largest_seen = 0
        for idx in range(len(bank)-1):
            battery = bank[idx]
            if battery > largest_seen:
                largest_seen = battery
                second_largest_seen = 0
                for idx2 in range(idx+1, len(bank)):
                    if bank[idx2] > second_largest_seen:
                        second_largest_seen = bank[idx2]
        # print(bank)
        # print(largest_seen, second_largest_seen)
        total = str(largest_seen) + str(second_largest_seen)
        # print(total)
        p1 += int(total)
    return p1

cache = {}


def find_next_largest(bank, largest_seen):
    cache_key = (tuple(bank), tuple(largest_seen))
    if cache_key in cache:
        return cache[cache_key]
    # print("  ", bank, largest_seen)
    if len(largest_seen) == 0:
        return []
    if len(largest_seen) > len(bank):
        return largest_seen
    for idx in range(1 + len(bank) - len(largest_seen)):
        battery = bank[idx]
        if battery > largest_seen[0]:
            # largest_seen[1:] = 0
            largest_seen[0] = battery
            # Reset to zero
            largest_seen[1:] = [0] * (len(largest_seen) - 1)
            # print(f"{idx}>", largest_seen)
            largest_seen[1:] = find_next_largest(bank[idx+1:], list(largest_seen[1:]))
            # print(f"<{idx}", largest_seen)
    cache[cache_key] = largest_seen
    return largest_seen


def part2(lines):
    ans = 0
    for line in lines:
        bank = [int(chr) for chr in line]
        largest_seen = [0]*12
        largest_seen = find_next_largest(bank, largest_seen)
        total = "".join([str(seen) for seen in largest_seen])
        ans += int(total)
        # print(bank, "=", total)
        # exit()
    return ans


# 7:32-7:38 realise part2 is less greedy?
# Part2 time lost: forgot to reset to zero
# while waiting for slow run - 3m24s - I quickly added optimization
def main():
    lines = [line.strip() for line in fileinput.input()]
    print(f'Lines: {len(lines)}')

    print(part1(lines))
    print(part2(lines))


if __name__ == '__main__':
    main()
