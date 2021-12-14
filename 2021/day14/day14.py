#!/usr/bin/env python3
import fileinput
from collections import Counter


def list_in_list(small_list, big_list):
    print(''.join(small_list), '---', ''.join(big_list))
    return ''.join(small_list) in ''.join(big_list)


def main():
    lines = [line.strip() for line in fileinput.input()]
    print(f'Lines: {len(lines)}')

    polymer = None
    steps = {}
    for line in lines:
        if polymer is None:
            polymer = line #list(line)
            continue
        if not line:
            continue
        frm,to = line.split(' -> ')
        assert len(frm) == 2
        assert len(to) == 1
        assert frm not in steps
        steps[frm] = to
        # steps.append((frm,to))
    print(polymer)
    poly = []
    for i in range(len(polymer)-1):
        poly.append(polymer[i:i+2])
    print(poly)
    print(len(poly)+1)
    print(steps)
    for i in range(40):
        new_poly = list(poly)
        for idx in range(len(poly)-1,0-1,-1):
            p = poly[idx]
            if p in steps:
                frm, to = p, steps[p]
                becomes = [frm[0]+to, to+frm[1]]
                new_poly = new_poly[:idx] + becomes + new_poly[idx+1:]
        poly = new_poly
        # changes = []
        # for step in steps:
        #     frm, to = step
        #     # frm = list(frm)
        #     if frm in poly:  # list_in_list(frm, poly):
        #         changes.append((poly.index(frm), step))
        #         # print(step)
        # # print('selected:', changes)
        # for idx_step in sorted(changes, key=lambda c: c[0], reverse=True):
        #     # print('___', idx_step)
        #     idx, step = idx_step
        #     frm, to = step
        #     becomes = [frm[0]+to, to+frm[1]]
        #     print('becomes', becomes)
        #     poly = poly[:idx] + becomes + poly[idx+1:]

        # print(poly)
        # polymer = ''
        # for p in poly:
        #     polymer += p[0]
        # polymer += poly[-1][1]
        # print(polymer)
        print(f'step {i+1}: {len(poly)+1}')
    polymer = ''
    for p in poly:
        polymer += p[0]
    polymer += poly[-1][1]
    print(polymer)
    counts = Counter(polymer).most_common()
    print(counts)
    print(counts[0][1] - counts[-1][1])



if __name__ == '__main__':
    main()
