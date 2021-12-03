#!/usr/bin/env python3
import fileinput
from collections import Counter


def keep_only_with_val(report, val, idx):
    # keep those with val at idx
    new_report = []
    for line in report:
        if line[idx] == val:
            new_report.append(line)
    return new_report


def bit_criteria_filter(report, prefer_common_bits= True):
    major_bit = '0'
    minor_bit = '1'
    if prefer_common_bits:
        major_bit = '1'
        minor_bit = '0'        

    new_report = report
    for idx in range(len(report[0])):
        one_counts = count_ones(new_report)
        if one_counts[idx] >= (len(new_report)/2):
            new_report = keep_only_with_val(new_report, major_bit, idx)
        else:
            new_report = keep_only_with_val(new_report, minor_bit, idx)
        if len(new_report) == 1:
            break
    return new_report


def count_ones(report):
    one_counts = [0]*len(report[0])
    for line in report:
        for idx, char in enumerate(line):
            if char == '1':
                one_counts[idx] += 1
    return one_counts


def main():
    report = [line.strip() for line in fileinput.input()]
    print('Lines: {}'.format(len(report)))

    # Part 1
    one_counts = count_ones(report)
    common_vals = ['1' if o > (len(report)/2) else '0' for o in one_counts]
    # gamma & epsilon are inverses...
    gamma_bin = ''.join(common_vals)
    epsilon_bin = gamma_bin.replace('0','_').replace('1','0').replace('_','1')
    gamma = int(gamma_bin, 2)
    epsilon = int(epsilon_bin, 2)
    print('Part 1:', gamma * epsilon)

    # Part 2
    oxy_report = bit_criteria_filter(report, True)
    co2_report = bit_criteria_filter(report, False)
    assert len(oxy_report) == 1
    assert len(co2_report) == 1
    oxy = int(oxy_report[0], 2)
    co2 = int(co2_report[0], 2)
    print('Part 2:', oxy, co2)
    print('Part 2:', oxy * co2)


if __name__ == '__main__':
    main()
