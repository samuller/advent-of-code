#!/usr/bin/env python3
import fileinput


def main():
    lines = [line.strip() for line in fileinput.input()]
    print('Lines: {}'.format(len(lines)))

    xpos = 0
    depth = 0
    aim = 0

    count_valid = 0
    for line in lines:
        direction, num = line.split(' ')
        num = int(num)
        # Part 1
        # if direction == "forward":
        #     xpos += num
        # if direction == "down":
        #     depth += num
        # if direction == "up":
        #     depth -= num

        # Part 2
        if direction == "forward":
            xpos += num
            depth += aim * num
        if direction == "down":
            aim += num
        if direction == "up":
            aim -= num
    print(xpos, depth)
    print(xpos*depth)


if __name__ == '__main__':
    main()
