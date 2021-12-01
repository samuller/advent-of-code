#!/usr/bin/env python3
import fileinput
from collections import Counter


# bugs:
# 1509 - off by one error on indices
# 1998 - same, on 2nd prev + if offset
def main():
    nums = [int(line.strip()) for line in fileinput.input()]
    print('Lines: {}'.format(len(nums)))

    # Part 1
    nums1 = nums[:-1]
    nums2 = nums[1:]
    assert len(nums1) == len(nums2)
    # Previous approach with for-loop is probably more adaptable
    larger = [nums2[i] > nums1[i] for i in range(len(nums1))]
    count = Counter(larger)[True]
    print(count)

    # Part 2
    larger = [sum(nums[i+1:i+1+3]) > sum(nums[i:i+3]) for i in range(len(nums1)-2)]
    count = Counter(larger)[True]
    print(count)


if __name__ == '__main__':
    main()
