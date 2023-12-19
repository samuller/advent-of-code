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
        print(curr_states)
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
                    # if part[attr] < int(val):
                    next_limits = deepcopy(new_limits)
                    limit = next_limits[attr]
                    limit[1] = val
                    next_limits[attr] = limit
                    next_states.append((dest, new_limits))
                    # Opposite
                    new_limits

                elif '>' in cmp:
                    attr, val = cmp.split('>')
                    # if part[attr] > int(val):
                    limit = new_limits[attr]
                    limit[0] = val
                    new_limits[attr] = limit
                    next_states.append((dest, new_limits))
                else:
                    assert False, cmp
        curr_states = next_states
    return curr_states


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
