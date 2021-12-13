#!/usr/bin/env python3
import fileinput


def get_limits(dots):
    x_min = None
    x_max = None
    y_min = None
    y_max = None
    for x,y in dots:
        if x_min is None or x < x_min:
            x_min = x
        if x_max is None or x > x_max:
            x_max = x
        if y_min is None or y < y_min:
            y_min = y
        if y_max is None or y > y_max:
            y_max = y
    return x_min, x_max, y_min, y_max


def print_dots(dots):
    x_min, x_max, y_min, y_max = get_limits(dots)
    print(x_min, x_max, y_min, y_max)
    for y in range(y_min,y_max+1):
        for x in range(x_min,x_max+1):
    # for x in range(x_min,x_max+1):
    #     for y in range(y_min,y_max+1):
            if (x,y) in dots:
                print('█',end="")
            else:
                print(' ',end="")
        print()
    print()


def fold_up(dots, y_axis):
    # example unclear: axis is halve? axis determines limits?
    dots = list(dots)
    for idx, dot in enumerate(dots):
        x,y = dot
        # dots on axis?
        assert y != y_axis
        if y > y_axis:
            diff = y-y_axis
            dots[idx] = (x,y_axis-diff)
            # print('YY:',x,y,'=>',x,y_axis-diff)
    return set(dots)


def fold_left(dots, x_axis):
    # example unclear: left-right mirror
    x_min, x_max, y_min, y_max = get_limits(dots)
    dots = list(dots)
    for idx, dot in enumerate(dots):
        x,y = dot
        assert x != x_axis
        if x > x_axis:
            diff = x-x_axis
            dots[idx] = (x_axis-diff,y)
            # print('XX:',x,y,'=>',x_axis-diff,y)
    return set(dots)


# 421 @ 7:28
def main():
    lines = [line.strip() for line in fileinput.input()]
    part1 = False

    dots = set()
    instructions = []
    gap_found = False
    for line in lines:
        if gap_found:
            axis = line.split()[2]
            ax, val = axis.split('=')
            instructions.append((ax, int(val)))
            continue
        if not line:
            gap_found = True
            continue
        x,y = line.split(',')
        dots.add((int(x),int(y)))
        # print(x,y)

    # print(dots)
    for ins in instructions:
        print(ins)
        axis, value = ins
        if axis == 'y':
            dots = fold_up(dots, value)
        elif axis == 'x':
            dots = fold_left(dots, value)
        else:
            assert False
        if part1:
            print(len(dots))
            exit()
    # print(sorted(list(dots)))
    # print(len(dots))

    print_dots(dots)


if __name__ == '__main__':
    main()
