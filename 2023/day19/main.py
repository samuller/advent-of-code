#!/usr/bin/env python3
import fileinput
import sys; sys.path.append("../..")
from lib import *


class Classy:
    def __init__(self):
        pass


def process(part, workflows):
    assert 'in' in workflows
    curr_state = 'in'
    while curr_state not in ['R', 'A']:
        workflow = workflows[curr_state]
        print(workflow)
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
    return curr_state


def main():
    lines = [line.strip() for line in fileinput.input()]
    print(f'Lines: {len(lines)}')

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
    print(workflows)

    print(known_states)
    for node in known_states:
        assert node in workflows or node in ['R', 'A'], node

    parts = []
    for line in parts_lines:
        assert line[0] == '{' and line[-1] == '}'
        line = line[1:-1]
        print(line)
        # ratings = {cat: val for rating in line.split(',') for cat, val in rating.split('=')}
        ratings = {}
        for rating in line.split(','):
            cat, val = rating.split('=')
            ratings[cat] = int(val)
        parts.append(ratings)
    print(parts)

    ans1 = 0
    for part in parts:
        if process(part, workflows) == 'A':
            ans1 += sum(part.values())
    print(ans1)

if __name__ == '__main__':
    main()
