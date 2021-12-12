#!/usr/bin/env python3
import re
import fileinput
from copy import copy
from collections import defaultdict, Counter


def is_small_cave(name):
    return re.fullmatch(r'[a-z]+', name) is not None


assert is_small_cave('a') == True, is_small_cave('a')
assert is_small_cave('abc') == True
assert is_small_cave('aBc') == False


def part1_is_valid_path(current_path):
    counts = Counter(current_path)
    for node, count in counts.items():
        if is_small_cave(node) and count > 1:
            return False
        if node in ['start', 'end'] and count > 1:
            return False
    return True


def part2_is_valid_path(current_path):
    counts = Counter(current_path)
    duplicate_exists = False
    for node, count in counts.items():
        if is_small_cave(node):
            if count > 1 and duplicate_exists:
                return False
            if count > 2:
                return False
            if count > 1:
                duplicate_exists = True
        if node in ['start', 'end'] and count > 1:
                return False

    return True

assert part2_is_valid_path(['start', 'A', 'c', 'A', 'c']) == True
assert part2_is_valid_path(['start', 'A', 'c', 'A', 'c', 'A', 'c']) == False


all_paths = []
def unique_paths(network, current_node='start', current_path=None, validation_func=part2_is_valid_path):
    if current_path is None:
        current_path = []
    current_path.append(current_node)
    # print(current_path)

    if not validation_func(current_path):
        return None

    if current_node == 'end':
        # print(current_path)
        all_paths.append(current_path)
        return current_path

    next_nodes = network[current_node]
    for node in next_nodes:
        unique_paths(network, node, copy(current_path), validation_func)

    return None


def main():
    lines = [line.strip() for line in fileinput.input()]

    nodes = set()
    next_nodes = defaultdict(list)
    for line in lines:
        left, right = line.split('-')
        nodes.add(left)
        nodes.add(right)
        next_nodes[left].append(right)
        next_nodes[right].append(left)
    assert 'start' in nodes
    assert 'end' in nodes

    global all_paths
    unique_paths(next_nodes, 'start', [], validation_func=part1_is_valid_path)
    print('P1:', len(all_paths))
    all_paths = []
    unique_paths(next_nodes, 'start', [], validation_func=part2_is_valid_path)
    print('P2:', len(all_paths))
    
    # Part 1
    # assert unique_paths(test1) == 10
    # assert unique_paths(test2) == 19
    # assert unique_paths(test3) == 226

    # Part 2
    # assert unique_paths(test1) == 36
    # assert unique_paths(test2) == 103
    # assert unique_paths(test3) == 3509


if __name__ == '__main__':
    main()
