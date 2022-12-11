#!/usr/bin/env python3
import fileinput
from copy import deepcopy
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


def play_keep_away(monkeys, rounds, part1=True):
    primes = prod([mnk.test_div for mnk in monkeys])
    inspect_count = [0] * len(monkeys)
    for round in range(rounds):
        for idx in range(len(monkeys)):
            monkey = monkeys[idx]
            inspect_count[idx] += len(monkey.items)
            # Inspect items
            for item in monkey.items:
                # Increase worry level
                item = monkey.op(item)
                # Decrease worry level
                if part1:
                    item = item // 3
                # Check if it is divisible
                if item % monkey.test_div == 0:
                    new_mnk_idx = monkey.test_true
                else:
                    new_mnk_idx = monkey.test_false
                assert new_mnk_idx != idx
                new_item = item
                if not part1:
                    # Shrink worry count without losing divisible property...
                    new_item = new_item % primes
                # Pass item to a new monkey
                # Tuple is immutable, but list it's pointing to isn't (alternative: tuple._replace(items=...))
                monkeys[new_mnk_idx].items.append(new_item)
            # Remove items just moved
            while len(monkey.items) != 0:
                monkey.items.pop()
        # print(round+1, [mnk.items for mnk in monkeys])
        # if (round+1) % 100 == 0 or (round+1) in [1, 20]:
        #     print(round+1, [mnk.items for mnk in monkeys])
    # print(inspect_count)
    print(prod(sorted(inspect_count)[-2:]))


def main():
    lines = [line.replace("\n", "") for line in fileinput.input()]
    # Parse input
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
    # Part 1 (need a deepcopy for part 2 since we alter lists)
    play_keep_away(deepcopy(monkeys), rounds=20)
    # Part 2
    play_keep_away(monkeys, rounds=10000, part1=False)
    exit()


if __name__ == '__main__':
    main()
