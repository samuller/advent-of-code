#!/usr/bin/env python3
import fileinput


def main():
    lines = [line.strip() for line in fileinput.input()]
    assert len(lines) == 1
    nums = [int(n) for n in lines[0].split(',')]
    print(nums)
    print(max(nums))
    # min_cost = sys.maxsize
    costs = []
    for i in range(0, max(nums)):
        cost = 0
        for n in nums:
            # Part 1
            # cost += abs(n - i)
            # Part 2
            cost += sum(range(1, 1+abs(n - i)))
            # print(n, i, sum(range(1, 1+abs(n - i))))
        # print(cost)
        costs.append(cost)
    print(min(costs))


if __name__ == '__main__':
    main()
