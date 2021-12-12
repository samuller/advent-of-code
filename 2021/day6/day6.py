#!/usr/bin/env python3
import fileinput
from collections import Counter, defaultdict


def main():
    lines = [line.strip() for line in fileinput.input()]
    print(f'Lines: {len(lines)}')
    assert len(lines) == 1
    fish = [int(n) for n in lines[0].split(',')]

    part1 = True

    # Part 1
    # # what are the possible correct orderings of these commands?
    # for i in range(256):
    #     # print(fish)
    #     zeroes = [idx for idx, num in enumerate(fish) if num == 0]
    #     # print(zeroes)

    #     fish = [n-1 if n >= 1 else 0 for n in fish]
    #     for z in zeroes:
    #         fish[z] = 6
    #     fish.extend([8]*len(zeroes))

    # print(len(fish))

    fish = Counter(fish)
    for i in range(80 if part1 else 256):
        # print(fish)
        newlings = fish[0]

        new_fish = defaultdict(int)
        for age, count in fish.items():
            if age >= 1 and count > 0:
                new_fish[age-1] += count
            else:
                new_fish[age] += count
            assert -1 not in new_fish
        # print(newlings, new_fish[0]) #, fish)
        new_fish[6] += newlings
        new_fish[8] += newlings
        # new_fish[0] = 0
        new_fish[0] -= newlings
        fish = new_fish
    print(sum(fish.values()))


if __name__ == '__main__':
    main()
