#!/usr/bin/env python3
import fileinput
from collections import Counter
# import sys; sys.path.append("../..")
# from lib import *


class Classy:
    def __init__(self):
        pass


def keep_only_with_val(report, val, idx):
    # keep those with val at idx
    new_report = []
    for line in report:
        if line[idx] == val:
            new_report.append(line)
    return new_report

def transpose(report):
    if len(report) == 0:
        return []
    transpose = ['' for _ in range(len(report[0]))]
    for line in report:
        for idx, char in enumerate(line):
            transpose[idx] += char
    return transpose


def main():
    report = [line.strip() for line in fileinput.input()]
    print('Lines: {}'.format(len(report)))

    gamma = 0
    epsilon = 0
    trans = transpose(report)
    # print(report)
    # print(trans)

    # Part 1
    gamma_bin = ''
    epsilon_bin = ''
    for line in trans:
        cnt = Counter(line)
        if cnt['1'] > cnt['0']:
            gamma_bin += '1'
            epsilon_bin += '0'
        else:
            gamma_bin += '0'
            epsilon_bin += '1'
    # Part 2
    ox_report = report
    final_ox_report = ox_report
    for idx in range(len(report[0])):
        trans = transpose(ox_report)
        cnt = Counter(trans[idx])
        print(cnt)
        if cnt['1'] >= cnt['0']:
            ox_report = keep_only_with_val(ox_report, '1', idx)
        else:
            ox_report = keep_only_with_val(ox_report, '0', idx)
        if len(ox_report) == 1:
            final_ox_report = ox_report
            break

    co2_report = report
    final_co2_report = co2_report
    for idx in range(len(report[0])):
        trans = transpose(co2_report)
        cnt = Counter(trans[idx])
        if cnt['1'] >= cnt['0']:
            co2_report = keep_only_with_val(co2_report, '0', idx)
        else:
            co2_report = keep_only_with_val(co2_report, '1', idx)
        if len(co2_report) == 1:
            final_co2_report = co2_report
            break

    print(final_ox_report)
    assert len(final_ox_report) == 1
    print(final_co2_report)
    assert len(final_co2_report) == 1
    oxy = int(final_ox_report[0], 2)
    co2 = int(final_co2_report[0], 2)

    print(gamma_bin)
    print(epsilon_bin)
    gamma = int(gamma_bin, 2)
    epsilon = int(epsilon_bin, 2)

    print(gamma, epsilon)
    print(gamma * epsilon)

    print(oxy, co2)
    print(oxy * co2)


if __name__ == '__main__':
    main()
