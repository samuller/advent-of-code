#!/usr/bin/env python3
import fileinput
# import sys; sys.path.append("..")
# from lib import *


class Classy:
    def __init__(self):
        pass


def function(input):
    return False


def main():
    lines = [line.strip() for line in fileinput.input()]
    print('Lines: {}'.format(len(lines)))

    count_valid = 0
    for line in lines:
        fields = line.split(' ')


if __name__ == '__main__':
    main()
