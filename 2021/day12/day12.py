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


def is_valid_path(current_path):
    counts = Counter(current_path)
    duplicate_exists = False
    for node, count in counts.items():
        if is_small_cave(node):
            # Part 1
            # if count > 1:
            #     return False
            # Part 2
            if count > 1 and duplicate_exists:
                return False
            if count > 2:
                return False
            if count > 1:
                duplicate_exists = True
        if node in ['start', 'end'] and count > 1:
                return False

    return True

# Part 2
assert is_valid_path(['start', 'A', 'c', 'A', 'c']) == True
assert is_valid_path(['start', 'A', 'c', 'A', 'c', 'A', 'c']) == False


all_paths = []
def unique_paths(network, current_node='start', current_path=None):
    if current_path is None:
        current_path = []
    current_path.append(current_node)
    # print(current_path)

    if not is_valid_path(current_path):
        return None

    if current_node == 'end':
        # print(current_path)
        all_paths.append(current_path)
        return current_path

    next_nodes = network[current_node]
    for node in next_nodes:
        # if is_small_cave(node):
        #     if node in current_path:
        #         continue
        unique_paths(network, node, copy(current_path))

    return None

# Original part1
# def unique_paths(network, current_node='start', current_path=None):
#     if current_path is None:
#         current_path = []
#     current_path.append(current_node)

#     if current_node == 'end':
#         all_paths.append(current_path)
#         return current_path

#     next_nodes = network[current_node]
#     for node in next_nodes:
#         if is_small_cave(node):
#             if node in current_path:
#                 continue
#         unique_paths(network, node, copy(current_path))

#     return current_path


def main():
    lines = [line.strip() for line in fileinput.input()]
    print(f'Lines: {len(lines)}')

    nodes = set()
    network = defaultdict(list)
    for line in lines:
        left, right = line.split('-')
        nodes.add(left)
        nodes.add(right)
        network[left].append(right)
        network[right].append(left)
    assert 'start' in nodes
    assert 'end' in nodes
    print(nodes)
    print(network)

    unique_paths(network, 'start', [])
    print(len(all_paths))
    
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
