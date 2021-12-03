#!/usr/bin/env python3
import fileinput
from collections import Counter


def bit_criteria_filter(report, prefer_common_bits=True):
    major_bit, minor_bit = '0', '1'
    if prefer_common_bits:
        major_bit, minor_bit = '1', '0'

    new_report = report
    for idx in range(len(report[0])):
        bit = major_bit if count_idx_ones(new_report, idx) >= (len(new_report)/2) else minor_bit
        new_report = [line for line in new_report if line[idx] == bit]
        if len(new_report) == 1:
            return new_report
    return None


def count_idx_ones(report, idx):
    return sum([int(line[idx]) for line in report])


def main():
    report = [line.strip() for line in fileinput.input()]
    # Part 1
    common_vals = ['1' if count_idx_ones(report, idx) > (len(report)/2) else '0'
        for idx in range(len(report[0]))
    ]
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
    print('Part 2:', oxy * co2)


if __name__ == '__main__':
    main()
