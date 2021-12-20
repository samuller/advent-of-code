#!/usr/bin/env python3
import itertools
import fileinput
import sys; sys.path.append("../..")
from lib import *


def print_img(pixels):
    rs = [r for r,_ in pixels]
    cs = [c for _,c in pixels]
    for r in range(min(rs)-2, max(rs)+1+2):
        for c in range(min(cs)-2, max(cs)+1+2):
            if (r,c) in pixels:
                print('#', end="")
            else:
                print('.', end="")
        print()
    print()


def enhance(pixels, algo, swap=False):
    rs = [r for r,_ in pixels]
    cs = [c for _,c in pixels]
    # print(rs)
    # print(cs)

    new_pixels = set()
    ext = 3
    # for pixel in pixels:
    #     r,c = pixel
    for r in range(min(rs)-ext, max(rs)+1+ext):
        for c in range(min(cs)-ext, max(cs)+1+ext):
            binary_value = []
            for dr, dc in itertools.product([-1,0,1],[-1,0,1]):
                rr,cc = r+dr,c+dc
                if (rr,cc) in pixels:
                    binary_value.append('1' if not swap else '0')
                else:
                    binary_value.append('0' if not swap else '1')
            value = int("".join(binary_value), 2)
            # print(r,c,value)
            if algo[value] == '#':
                new_pixels.add((r,c))
    return new_pixels


def inverse(pixels):
    rs = [r for r,_ in pixels]
    cs = [c for _,c in pixels]
    new_pixels = set()
    for r in range(min(rs), max(rs)+1):
        for c in range(min(cs), max(cs)+1):
            if (r,c) not in pixels:
                new_pixels.add((r,c))
    return new_pixels


# 5991 @ 7:18 (2)
# 6496 @ 7:24 (3)
# 5469 @ 7:25 (1)
# infinite @ 7:31 [4x, 5min delay]
# 5563 @ 7:45 (skipped border) [answer for someone else]
# 5559 @ 7:58 (swapping)
# 5383 @ 8:06 (inversing) [7x, 10min delay]
# 5416 @ 8:16 (inverse & swapping)
# 9:26 (inverse + swapping without re-inverse)
def main():
    lines = [line.strip() for line in fileinput.input()]
    groups = list(grouped(lines))
    algo = groups[0][0]
    assert len(algo) == 512
    assert (algo[0],algo[511]) in [('.','#'), ('#','.')]
    input = groups[1]

    R = len(input)
    C = len(input[0])
    print(f'Input: {R}x{C}')
    pixels = set()
    for r in range(R):
        for c in range(C):
            assert input[r][c] in ['.', '#']
            if input[r][c] == '#':
                pixels.add((r,c))

    print_img(pixels)
    print(len(pixels))
    for i in range(50):
        if i % 2 == 0:
            pixels = enhance(pixels, algo, False)
        else:
            pixels = inverse(pixels)
            pixels = enhance(pixels, algo, True)
            # pixels = inverse(pixels)

        rs = [r for r,_ in pixels]
        cs = [c for _,c in pixels]
        print(f"{max(rs)-min(rs)}x{max(cs)-min(cs)}")
        # img_pixels = {(r,c) for r,c in pixels 
        #     if r != min(rs) and r != max(rs) and c != min(cs) and c != max(cs)}
        # border_pixels = {(r,c) for r,c in pixels 
        #     if r == min(rs) or r == max(rs) or c == min(cs) or c == max(cs)}
        # pixels = img_pixels
        # print_img(pixels)
        # if i % 2 == 1:
        #     print('border ', end="")
            # 4 + 106*4
            # 5,7,9 / 100,103,105
            # print(len(border_pixels))
        # else:
        print(len(pixels))


if __name__ == '__main__':
    main()
