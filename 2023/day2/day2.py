#!/usr/bin/env python3
import fileinput
from collections import Counter, defaultdict
import sys; sys.path.append("../..")
from lib import *


def main():
    lines = [line.strip() for line in fileinput.input()]

    valid = {'red': 12, 'green': 13, 'blue': 14}
    valid_ids = []
    min_valid_powers = {}
    for line in lines:
        game_id_str, data = line.split(': ')
        game_id = int(game_id_str.split()[1])
        sets = data.split('; ')
        # sets_counter = Counter()
        valid_sets = []
        # all min_valid uses are for part 2
        min_valid = defaultdict(int)
        for set_ in sets:
            set_counter = defaultdict(int)
            for cubes in set_.split(', '):
                # print(cubes)
                val, type = cubes.split(' ')
                set_counter[type] += int(val)
                min_valid[type] = max(min_valid[type], int(val))
            # print(game_id_str, set_counter, valid)
            is_valid = True
            for type, count in valid.items():
                if set_counter.get(type, 0) > count:
                    is_valid = False
                    break
            valid_sets.append(is_valid)
        # print("min_valid:", game_id_str, min_valid)
        min_valid_powers[game_id] = prod(min_valid.values())
        if all(valid_sets):
            valid_ids.append(game_id)
    # print(valid_ids)
    print(sum(valid_ids))

    print(sum(min_valid_powers.values()))


if __name__ == '__main__':
    main()
