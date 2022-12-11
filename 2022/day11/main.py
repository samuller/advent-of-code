#!/usr/bin/env python3
import fileinput
from collections import Counter
from collections import namedtuple

import sys; sys.path.append("../..")
from lib import *


def parse_operation(operation):
    assert len(operation) == 3
    val1, op, val2 = operation
    assert val1 == "old"
    if op == '+':
        return lambda old: old + int(val2)
    if op == '*' and val2 == 'old':
        return lambda old: old * old
    if op == '*':
        return lambda old: old * int(val2)


# https://stackoverflow.com/questions/15347174/python-finding-prime-factors
def largest_prime_factor(n):
    i = 2
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
    # print(n)
    return n

assert largest_prime_factor(4526634765) == 15882929


# https://stackoverflow.com/questions/15347174/python-finding-prime-factors
def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


def largest_prime_factor_and_not_divisible(n):
    factors = sorted(prime_factors(n), reverse=True)
    # for factor in factors:
    #     if factor % 2 != 0
    # large_prime = largest_prime_factor(n)
    return 1

# print(largest_prime_factor_and_not_divisible(4526634765))
# exit()


def shrink_worry(item):
    new_item = item
    while new_item > 23*19*13*17:  # 29
        new_item -= 23*19*13*17
    assert item % 23 == new_item % 23, f"{item} ({item % 23}) vs. {new_item} ({new_item % 23})"
    return new_item

    # shrink worry count (keep lower prime factors...)
    new_item = item
    largest = largest_prime_factor(item)
    while largest > 23:
        print(largest)
        new_item = new_item // largest
        largest = largest_prime_factor(new_item)
    assert item % 23 == new_item % 23, f"{item} ({item % 23}) vs. {new_item} ({new_item % 23})"

    # for high_prime in reversed([23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]):
    #     if item % high_prime == 0:
    #         new_item = new_item // high_prime
    #         print(item, " -> ", new_item)
    #         # break
    if new_item > 2**32:
        print("Failed:", new_item)
        exit()
    return new_item

def main():
    lines = [line.replace("\n", "") for line in fileinput.input()]
    # print(lines)
    monkeys = []
    Monkey = namedtuple('Monkey', ['items', 'op', 'test_div', 'test_true', 'test_false'])
    for monkey in grouped(lines):
        assert monkey[0].startswith("Monkey ")
        count = int(monkey[0].split()[1].replace(":", ""))
        starting = [int(st.replace(",", "")) for st in monkey[1].split()[2:]]
        operation = parse_operation(monkey[2].split()[3:]) #(10)
        test_div = int(monkey[3].split()[3])
        test_true = int(monkey[4].split()[5])
        test_false = int(monkey[5].split()[5])
        # print(count, test_div, test_true, test_false)  #monkey)
        monkeys.append(Monkey(
            items=starting, op=operation, test_div=test_div, test_true=test_true, test_false=test_false
        ))

    # Part 1
    inspect_count = [0] * len(monkeys)
    for round in range(20):
        for idx in range(len(monkeys)):
            monkey = monkeys[idx]
            inspect_count[idx] += len(monkey.items)
            for item in monkey.items:
                # print(item)
                item = monkey.op(item)
                # print(item)
                item = item // 3
                # print(item)
                if item % monkey.test_div == 0:
                    new_mnk_idx = monkey.test_true
                else:
                    new_mnk_idx = monkey.test_false
                assert new_mnk_idx != idx
                new_mnk = monkeys[new_mnk_idx]
                # Tuple is immutable, but list it's pointing to isn't (alternative: tuple._replace(items=...))
                new_mnk.items.append(item)
                # print()
            # Remove items just moved
            while len(monkey.items) != 0:
                monkey.items.pop()
            # print(len(monkeys), idx, round)
            # print([mnk.items for mnk in monkeys])
        # print(round+1, [mnk.items for mnk in monkeys])
        # if round % 100 == 0:
        #     print(round+1, [mnk.items for mnk in monkeys])
    print(inspect_count)
    print(prod(sorted(inspect_count)[-2:]))
    exit()

    # Part 2
    primes = prod([mnk.test_div for mnk in monkeys])
    print(primes)
    inspect_count = [0] * len(monkeys)
    for round in range(10000):
        for idx in range(len(monkeys)):
            monkey = monkeys[idx]
            inspect_count[idx] += len(monkey.items)
            for item in monkey.items:
                # print(item)
                item = monkey.op(item)
                # print(item)
                # item = item // 3
                # print(item)
                if item % monkey.test_div == 0:
                    new_mnk_idx = monkey.test_true
                else:
                    new_mnk_idx = monkey.test_false
                assert new_mnk_idx != idx
                new_mnk = monkeys[new_mnk_idx]
                # shrink worry count (keep lower prime factors...)
                # new_item = shrink_worry(item)
                new_item = item
                # print(new_item)
                # while new_item >= primes:  # 23*19*13*17:  # 29
                #     new_item -= primes # 23*19*13*17
                new_item = new_item % primes
                # print(new_item)
                # Tuple is immutable, but list it's pointing to isn't (alternative: tuple._replace(items=...))
                new_mnk.items.append(new_item)
                # print()
            # Remove items just moved
            while len(monkey.items) != 0:
                monkey.items.pop()
            # print(len(monkeys), idx, round)
            # print([mnk.items for mnk in monkeys])
        # print(round+1, [mnk.items for mnk in monkeys])
        # if (round+1) % 100 == 0 or (round+1) in [1, 20]:
        #     print(round+1, [mnk.items for mnk in monkeys])
        #     print(inspect_count)
    print(inspect_count)
    print(prod(sorted(inspect_count)[-2:]))
    exit()



if __name__ == '__main__':
    main()
