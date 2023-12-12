#!/usr/bin/env python3
import fileinput


def subs(nums):
    if len(nums) == 0:
        return 0
    nums = list(nums)
    num = nums[-2] - nums[-1]
    # print(f"<{num}>", nums[-2], nums[-1])
    nums.pop()
    nums.pop()
    while len(nums) > 0:
        # num -= nums.pop(0)
        # print(f"<{num}>", nums[-1], num)
        num = nums[-1] - num
        nums.pop()
    return num


def main():
    lines = [line.strip() for line in fileinput.input()]
    print(f'Lines: {len(lines)}')

    ans1 = 0
    ans2 = 0
    for line in lines:
        print()
        nums = [int(n) for n in line.split(' ')]
        print(nums)
        diff = []
        steps = 0
        prev = nums
        lasts = [nums[-1]]
        firsts = [nums[0]]
        while len(set(prev)) != 1:
            for idx in range(len(prev) - 1):
                diff.append(prev[idx+1] - prev[idx])
            print(" " * (steps + 1), diff)
            unique = set(diff)
            steps += 1
            # if len(unique) == 1:
            #     print(steps)
            # if steps == 5:
            #     exit()
            prev = diff
            diff = []
            lasts.append(prev[-1])
            firsts.append(prev[0])
        # print(lasts, sum(lasts))
        print(firsts, subs(firsts))
        ans1 += sum(lasts)
        ans2 += subs(firsts)
    print(ans1)
    print(ans2)

if __name__ == '__main__':
    main()
