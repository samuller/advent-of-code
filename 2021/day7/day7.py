#!/usr/bin/env python3
import sys
import fileinput


def sum_range(end):
    # Slower summation
    return sum(range(1, 1+end))


def arithmetic_series(start, end):
    # Arithmetic progression (sum of terms)
    num_of_terms = 1 + (end - start)
    return (num_of_terms*(start + end)) // 2


def sum_equation(end):
    return arithmetic_series(1, end)


def main():
    lines = [line.strip() for line in fileinput.input()]
    assert len(lines) == 1
    nums = [int(n) for n in lines[0].split(',')]
    # print(nums)

    identity = lambda x: x
    # Parts 1 & 2
    for cost_calc in [identity, sum_equation]:
        min_cost = sys.maxsize
        for i in range(0, max(nums)):
            total_cost = 0
            for n in nums:
                diff = abs(n - i)
                total_cost += cost_calc(diff)
                # print(n, i, cost_calc(diff))
            if total_cost < min_cost:
                min_cost = total_cost
            # print(total_cost)
        print(min_cost)


if __name__ == '__main__':
    main()
