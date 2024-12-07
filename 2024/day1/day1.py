#!/usr/bin/env python3
import fileinput
from collections import Counter


def main():
    lines = [line.strip() for line in fileinput.input()]
    list1, list2 = [], []
    for line in lines:
        fields = line.split(' ')
        list1.append(int(fields[0]))
        list2.append(int(fields[-1]))
    list1.sort()
    list2.sort()
    res1 = sum([abs(list1[i] - list2[i]) for i in range(len(list1))])
    print(res1)

    count2 = Counter(list2)
    res2 = sum([list1[i] * count2[list1[i]] for i in range(len(list1))])
    print(res2)


if __name__ == '__main__':
    main()
