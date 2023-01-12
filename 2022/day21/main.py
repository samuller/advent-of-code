#!/usr/bin/env python3
import itertools
import fileinput

import sys; sys.path.append("../..")
from lib import *


op_to_func = {
    '+': lambda x,y: x + y,
    '-': lambda x,y: x - y,
    '*': lambda x,y: x * y, 
    '/': lambda x,y: x / y,
    # Part 2
    '=': lambda x,y: x == y,
}


def calc(node, known, funcs):
    if node in known:
        return known[node]
    assert node in funcs
    deps, op = funcs[node]
    result = op_to_func[op](calc(deps[0], known, funcs), calc(deps[1], known, funcs))
    if result not in known:
        known[node] = result
    return result

# 7:34
def newton_estimation(func, start):
    pass


def main():
    lines = [line.replace("\n", "") for line in fileinput.input()]
    consts = {}
    funcs = {}
    for line in lines:
        name, process = line.split(": ")
        # print(name, process)
        try:
            val = int(process)
            consts[name] = val
        except ValueError:
            op = process[4:4+3].strip()
            deps = [process[0:4], process[4+3:]]
            assert op in ['+', '-', '*', '/']
            funcs[name] = (deps ,op)
    assert "root" in funcs
    # print(consts)
    # print(funcs)

    find_graph = None
    known = consts.copy()
    # need_to_know_queue = ["root"]
    # path_to_calc = []
    # #while "root" not in known:
    # while len(need_to_know_queue) > 0:
    #     curr = need_to_know_queue.pop(0)
    #     print(curr)
    #     if curr in known:
    #         continue
    #     assert curr in funcs, curr
    #     deps, op = funcs[curr]
    #     need_to_know_queue.extend(deps)
    #     path_to_calc.append(curr)

    calc("root", known, funcs)
    part1 = known["root"]
    assert part1 == int(part1)
    print(int(part1))

    # Part 2
    assert "humn" in consts
    root_deps, _ = funcs["root"]
    num1 = int(known[root_deps[0]])
    num2 = int(known[root_deps[1]])
    print(num1, "vs.", num2, "when humn =", known["humn"])


    def calc_func(x):
        new_known = consts.copy()
        new_known["humn"] = x
        calc("root", new_known, funcs)
        num1 = int(new_known[root_deps[0]])
        num2 = int(new_known[root_deps[1]])
        return num1, num2
    # newton_estimation()

    #curr_x = 0
    # curr_x = 6_200_000_000_000
    # diff_rng = 10
    # count = 0
    # while count < 20:
    #     num1, num2 = calc_func(curr_x)
    #     if num1 == num2:
    #         print("ANS:", curr_x)
    #         break
    #     num1_d1, num2_d1 = calc_func(curr_x - diff_rng)
    #     diff1 = num2_d1 - num1_d1
    #     num1_d2, num2_d2 = calc_func(curr_x + diff_rng)
    #     diff2 = num2_d2 - num1_d2
    #     if diff2 == 0:
    #         print("NOT")
    #         curr_x = curr_x + diff_rng
    #         continue
    #     diff = diff1/diff2
    #     if diff == 1.0:
    #         break
    #     change = max(1, abs(num2-num1)/diff)
    #     print(f"{curr_x} / {diff:.2f} / +{change:.2f} ({num1:,} vs. {num2:,})")
    #     curr_x = int(curr_x - change)
    #     count += 1

    # limits = [-10_000_000_000_000, 10_000_000_000_000]
    start = 3_305_669_213_692
    rng = 10
    for humn_add in range(start, start + rng):
        new_known = consts.copy()
        new_known["humn"] += humn_add
        calc("root", new_known, funcs)
        num1 = int(new_known[root_deps[0]])
        num2 = int(new_known[root_deps[1]])
        print(f"{num1:,} vs. {num2:,} when humn = {new_known['humn']}")
    if num1 < num2:
        print("below!")



if __name__ == '__main__':
    main()
