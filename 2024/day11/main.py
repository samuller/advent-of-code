#!/usr/bin/env python3
from collections import defaultdict
import fileinput


def blink_count(stones, max_depth, depth=0):
    if depth > max_depth:
        return 1
    count = 0
    for stone in stones:
        num = str(stone)
        if stone == 0:
            count += blink_count([1], max_depth, depth+1)
        elif len(num) % 2 == 0:
            num1 = int(num[0:len(num)//2])
            num2 = int(num[len(num)//2:])
            count += blink_count([num1, num2], max_depth, depth+1)
        else:
            count += blink_count([stone*2024], max_depth, depth+1)
    return count


cache = {}
def blink_count_cache(stones, max_depth, depth=0):
    if depth > max_depth:
        return 1
    count = 0
    # print(depth, stones)
    for stone in stones:
        if (stone, depth) in cache:
            new_stones = cache[(stone, depth)]
        else:
            num = str(stone)
            new_stones = 0
            if stone == 0:
                new_stones += blink_count_cache([1], max_depth, depth+1)
            elif len(num) % 2 == 0:
                num1 = int(num[0:len(num)//2])
                num2 = int(num[len(num)//2:])
                new_stones += blink_count_cache([num1, num2], max_depth, depth+1)
            else:
                new_stones += blink_count_cache([stone*2024], max_depth, depth+1)
            cache[(stone, depth)] = new_stones
        count += new_stones
    # print(count)
    return count


# def blink_count_stack(stones, max_depth):
#     count = len(stones)
#     stones = [(s, 0) for s in stones]
#     while len(stones) > 0:
#         # print(len(stones))
#         stone, depth = stones.pop()
#         # if depth > max_depth:
#         #     continue
#         count += 1
#         for step in range(depth, max_depth):
#             num = str(stone)
#             if stone == 0:
#                 stone = 1
#             elif len(num) % 2 == 0:
#                 num1 = int(num[0:len(num)//2])
#                 num2 = int(num[len(num)//2:])
#                 stone = num1
#                 stones.append((num2, step+1))
#             else:
#                 stone = stone*2024
#     return count


# # print(blink_count_stats(stones, max_depth=25))
# # print(stats)
# stats = defaultdict(int)
# def blink_count_stats(stones, max_depth, depth=0):
#     if depth > max_depth:
#         return 1
#     count = 0
#     new_stones = 0
#     for stone in stones:
#         num = str(stone)
#         if stone == 0:
#             count += blink_count_stats([1], max_depth, depth+1)
#         elif len(num) % 2 == 0:
#             num1 = int(num[0:len(num)//2])
#             num2 = int(num[len(num)//2:])
#             count += blink_count_stats([num1, num2], max_depth, depth+1)
#             new_stones += 1
#         else:
#             count += blink_count_stats([stone*2024], max_depth, depth+1)
#     if new_stones > 0:
#         stats[depth] += new_stones
#         # print(f"{new_stones} new at depth {depth}")
#     return count


def main():
    lines = [line.strip() for line in fileinput.input()]
    stones = [int(n) for n in lines[0].split()]
    # print(stones)
    print(blink_count(stones, max_depth=25))
    # Clear cache between runs
    global cache
    cache = {}
    print(blink_count_cache(stones, max_depth=75))


if __name__ == '__main__':
    main()
