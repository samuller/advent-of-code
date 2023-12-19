#!/usr/bin/env python3
import fileinput
from copy import deepcopy
import sys; sys.path.append("../..")
from lib import *


def parse_workflows(workflows):
    assert 'in' in workflows
    limits = {'x': [1, 4000], 'm': [1, 4000], 'a': [1, 4000], 's': [1, 4000]}
    curr_states = [('in', limits)]
    while set([st[0] for st in curr_states]) != set(['R', 'A']):
        # print('.', end="")
        next_states = []
        # print(curr_states)
        print('[')
        for cst in curr_states:
            print('  ', cst)
        print(']')
        for curr_state, curr_limits in curr_states:
            if curr_state in ['R', 'A']:
                next_states.append((curr_state, curr_limits))
                continue
            workflow = workflows[curr_state]
            new_limits = deepcopy(curr_limits)
            for rule in workflow:
                cmp, dest = rule
                if cmp == 'true':
                    next_states.append((dest, new_limits))
                elif '<' in cmp:
                    attr, val = cmp.split('<')
                    val = int(val)
                    # if part[attr] < int(val):
                    next_limits = deepcopy(new_limits)
                    limit = next_limits[attr]
                    limit[1] = val - 1
                    next_limits[attr] = limit
                    next_states.append((dest, next_limits))
                    # Opposite limit going forwards
                    limit = new_limits[attr]
                    limit[0] = val
                    new_limits[attr] = limit
                elif '>' in cmp:
                    attr, val = cmp.split('>')
                    val = int(val)
                    # if part[attr] > int(val):
                    next_limits = deepcopy(new_limits)
                    limit = next_limits[attr]
                    limit[0] = val + 1
                    next_limits[attr] = limit
                    next_states.append((dest, next_limits))
                    # Opposite limit going forwards
                    limit = new_limits[attr]
                    limit[1] = val
                    new_limits[attr] = limit
                else:
                    assert False, cmp
        curr_states = next_states
    print('[')
    for cst in curr_states:
        print('  ', cst)
    print(']')
    print(len(curr_states))
    counts = { 'R': 0, 'A': 0 }
    # counts = defaultdict(list)
    for state, limits in curr_states:
        total = 1
        for attr, interval in limits.items():
            assert interval[0] <= interval[1], interval
            total *= 1 + (interval[1] - interval[0])
            # counts[state].append(tuple(interval))
            # counts[state] *= 1 + (interval[1] - interval[0])
        print(state, limits, total)
        counts[state] += total
    return counts


def process(part, workflows):
    assert 'in' in workflows
    curr_state = 'in'
    while curr_state not in ['R', 'A']:
        # print('.', end="")
        workflow = workflows[curr_state]
        for rule in workflow:
            cmp, dest = rule
            if cmp == 'true':
                curr_state = dest
                break
            elif '<' in cmp:
                attr, val = cmp.split('<')
                if part[attr] < int(val):
                    curr_state = dest
                    break
            elif '>' in cmp:
                attr, val = cmp.split('>')
                if part[attr] > int(val):
                    curr_state = dest
                    break
            else:
                assert False, cmp
    # print()
    return curr_state


# [8:15-9:15] break
def main():
    lines = [line.strip() for line in fileinput.input()]

    workflow_lines, parts_lines = grouped(lines)
    workflows = {}
    # state machine
    known_states = set() # set(['R', 'A'])
    for line in workflow_lines:
        name, workflow = line.split('{')
        assert workflow[-1] == '}'
        workflow = workflow[:-1]
        rules = []
        for rule in workflow.split(','):
            rl = ('true', rule)
            if ':' in rule:
                rl = tuple(rule.split(':'))               
            rules.append(rl)
            known_states.add(rl[1])
        workflows[name] = rules
    # assert 'R' in known_states and 'A' in known_states and 'in' in known_states
    # print(workflows)

    # print(known_states)
    for node in known_states:
        assert node in workflows or node in ['R', 'A'], node

    parts = []
    for line in parts_lines:
        assert line[0] == '{' and line[-1] == '}'
        line = line[1:-1]
        # ratings = {cat: val for rating in line.split(',') for cat, val in rating.split('=')}
        ratings = {}
        for rating in line.split(','):
            cat, val = rating.split('=')
            ratings[cat] = int(val)
        parts.append(ratings)
    # print(parts)

    ans1 = 0
    for part in parts:
        if process(part, workflows) == 'A':
            ans1 += sum(part.values())
    print(ans1)

    print(parse_workflows(workflows))

if __name__ == '__main__':
    main()
