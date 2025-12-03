#!/usr/bin/env python3
import fileinput
# import sys; sys.path.append("../..")
# from lib import *


def is_invalid(num):
    num = str(num)
    if len(num) % 2 == 1:
        return False
    mid = len(num)//2
    for chr in range(mid):
        if num[chr] != num[mid + chr]:
            return False
    return True


def is_invalid2(num):
    # print("[]", num)
    num = str(num)
    mid = len(num)//2
    for repeat_length in range(1, mid+1):
        # print("len:", repeat_length)
        if len(num) % repeat_length != 0:
            continue
        repeats = len(num) // repeat_length
        matches = True
        for idx in range(repeat_length):
            for jmp in range(1, repeats):
                # print(" =", jmp, num[idx], num[idx + jmp*repeat_length])
                if num[idx] != num[idx + jmp*repeat_length]:
                    matches = False
                    break
        if matches:
            # print("matches", num, repeat_length)
            return True
    return False


# 7:08, 7:27
def main():
    lines = [line.strip() for line in fileinput.input()]

    p1 = 0
    p2 = 0
    for line in lines:
        ranges = line.split(',')
        for beg_end in ranges:
            if beg_end.strip() == "":
                continue
            beg, end = beg_end.split("-")
            for num in range(int(beg), int(end)+1):
                if is_invalid(num):
                    # print(num)
                    p1 += num
                if is_invalid2(num):
                    # print(num)
                    p2 += num
    print(p1)
    print(p2)


if __name__ == '__main__':
    main()
