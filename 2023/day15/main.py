#!/usr/bin/env python3
import fileinput
from collections import defaultdict


def calc_hash(string):
    hash = 0
    for c in string:
        hash += ord(c)
        hash *= 17
        hash = hash % 256
    return hash

assert calc_hash("HASH") == 52


def main():
    lines = [line.strip() for line in fileinput.input()]

    ans1 = 0
    hashmap = defaultdict(list)
    for line in lines:
        fields = line.split(',')
        for field in fields:
            # print(field)
            ans1 += calc_hash(field)
            # Part 2
            if '=' in field:
                label, lens = field.split('=')
                box = calc_hash(label)
                lens = int(lens)

                index = None
                for idx, clens in enumerate(hashmap[box]):
                    if clens[0] == label:
                        index = idx
                        break
                if index is None:
                    hashmap[box].append((label, lens))
                else:
                    hashmap[box][index] = (label,lens)
                assert '-' not in field
            elif '-' in field:
                assert '-' not in field[:-1]
                label = field[:-1]
                box = calc_hash(label)
                index = None
                for idx, clens in enumerate(hashmap[box]):
                    if clens[0] == label:
                        index = idx
                        break
                if index is not None:
                    hashmap[box].pop(index)
                # del hashmap[box]
            else:
                assert False
            # print(hashmap)
    print(ans1)

    # Focusing power
    ans2 = 0
    for box in hashmap:
        for idx, lbl_lens in enumerate(hashmap[box]):
            _, lens = lbl_lens
            power = (box + 1)*(idx + 1)*lens
            # print(box + 1, (idx + 1), lens)
            ans2 += power
    print(ans2)





if __name__ == '__main__':
    main()
