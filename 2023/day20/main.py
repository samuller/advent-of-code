#!/usr/bin/env python3
import difflib
import fileinput
from collections import defaultdict, OrderedDict
import sys; sys.path.append("../..")
from lib import *


def print_nodes(modules):
    shape = {
        '%': 'diamond',
        '&': 'box',
    }
    for key, (mtype, _) in modules.items():
        if mtype in shape:
            print(f"{key} [shape={shape[mtype]}]")
    print()
    nodes = ['broadcaster']
    seen = set()
    count = 0
    while len(nodes) > 0:
        node = nodes.pop()
        if node in seen:
            continue
        seen.add(node)
        if node not in modules:
            # print(node)
            continue
        _, dests = modules[node]
        for dest in dests:
            print(node, '->', dest)
        # print(node, '->', dests)
        nodes.extend(dests)
        count += 1
    exit()


def get_path_lengths(modules):
    """Count of sShortest path to each node."""
    # for key, (mtype, _) in modules.items():
    path_len = {}
    curr_len = 0
    # path = []
    follow = ['broadcaster']
    while len(follow) > 0:
        # print(follow)
        # print([f for f in follow if f not in path_len])
        next_follow = []
        for curr in follow:
            if curr in path_len:
                if path_len[curr] > curr_len:
                    path_len[curr] = curr_len
                continue
            path_len[curr] = curr_len
            if curr not in modules:
                continue
            _, dests = modules[curr]
            next_follow.extend(dests)
        follow = next_follow
        curr_len += 1
    # print(path_len)
    return path_len


def get_flipflop_lengths(modules):
    """Count of shortest flip-flop only path to each node."""
    path_len = {}
    curr_len = 0
    # path = []
    follow = ['broadcaster']
    while len(follow) > 0:
        # print(follow)
        # print([f for f in follow if f not in path_len])
        next_follow = []
        for curr in follow:
            # if already seen
            if curr in path_len:
                # Possibly overwrite with shorter paths
                if path_len[curr] > curr_len:
                    path_len[curr] = curr_len
                continue
            if curr not in modules:
                continue
            mtype, dests = modules[curr]
            if mtype not in ['%', 'broadcaster']:
                continue
            path_len[curr] = curr_len
            next_follow.extend(dests)
        follow = next_follow
        curr_len += 1
    # print(path_len)
    return path_len



def init_memory(modules):
    memory = defaultdict(dict)
    for src, (mtype, dests) in modules.items():
        for dest in dests:
            if dest not in modules:
                continue
            dest_type, _ = modules[dest]
            if dest_type == '&':
                memory[dest][src] = False
    return memory


def pulses_to_bin(pulse_list):
    bin = ""
    for p in pulse_list:
        bin += '1' if p else '0'
    return bin


# [8:08] 569597952 - too low [ordering...]
# [8:49] 606796102 - too low [multiple simultaneous pulses to same destination]
# [9:14] part 1 done
# [9:18] 1
# [10:16] 4294967296 - too low [guess 32-bits are counting... 33-bits and not exactly]
# [14:25] 5852528640000 - too low
def main():
    lines = [line.strip() for line in fileinput.input()]

    modules = {}
    # Last values received from each module's inputs
    # memory = defaultdict(dict)
    # states = {}
    for line in lines:
        src, dests = line.split(' -> ')
        dests = dests.split(', ')
        mtype = src
        if src[0] in ['%', '&']:
            mtype = src[0]
            src = src[1:]
        # states[src] = False
        modules[src] = (mtype, dests)
        # for dest in dests:
        #     memory[dest][src] = False
    # print(modules)
    # print(' '*5, memory)
    # print(' '*5, states)

    memory = init_memory(modules)

    # Part 2
    path_len = get_path_lengths(modules)
    ff_path_len = get_flipflop_lengths(modules)
    # print_nodes(modules)
    ans2 = 1
    for key in memory.keys():
        inputs = memory[key].keys()
        try:
            # input_lens = sorted([path_len[inp] for inp in inputs])
            input_lens = sorted([ff_path_len[inp] for inp in inputs])
        except:
            continue
        # TODO: count correctly
        alignment_count = 2**len(set(input_lens)) #prod(set(input_lens))
        print(key, input_lens, alignment_count)
        if len(inputs) >= 8:
            # TODO: account for loops adding extra counts
            ans2 *= alignment_count
        # path_len
    print(ans2)
    # exit()
    count = 0
    while True:
        count += 1
        if count % 1_000_000 == 0:
            print('.', end="")
        valid = True
        for b in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
            if (count >> (b-1)) & 1 == 0:
                valid = False
                break
        if valid:
            print(count)
            break
    exit()

    # { dest: value }
    active = defaultdict(bool)
    count_pulses = {False: 0, True: 0}
    rx_got_pulse = None
    prev_bin = ""
    # 2048
    for i in range(4098):  # 100_000
        print(i+1)
        # print(' ' * 4, active)

        # Part 2
        bin = ""
        # # for key in memory.keys():
        # # kz low if ['qq', 'sj', 'ls', 'bg'] all high
        # # ['qq', 'sj', 'ls', 'bg'] all high if each of ['hf', 'hb', 'dl', 'lq'] are low
        # # ['hf', 'hb', 'dl', 'lq'] all low if [8, 8, 8, 8] all high
        # # for key in  ['qq', 'sj', 'ls', 'bg']:
        # #     bin += f"{pulses_to_bin(memory[key].values())} "
        for key in ['hf', 'dl', 'lq', 'hb']:
            inputs = list(memory[key].keys())
            inputs.sort(key=lambda k1: path_len[k1], reverse=True)
            bin += f"{pulses_to_bin([memory[key][inp] for inp in inputs])} "
        print(i+1, bin)
        # diffs = [diff for diff in difflib.ndiff(prev_bin, bin) if not diff.startswith('  ')]
        # # print(diffs)
        # # print(len(diffs)//2)
        # prev_bin = bin

        pulses = { 'broadcaster': [False] }
        pulse_order = ['broadcaster']
        while len(pulses) > 0:
            # print(' ' * 4, ':', pulses)
            # print('==', pulse_order)
            # print(i, ':', states)
            # print('  ', memory)
            # print(' ' * 4, active)

            # Part 2
            # # bin = ""
            # # for key in memory.keys():
            # #     bin += f"{pulses_to_bin(memory[key].values())} "
            # # print(i, bin)
            # # if rx_got_pulse is None and 'rx' in pulses and pulses['rx'] == [False]:
            # #     rx_got_pulse = i+1
            # if any(memory['kz'].values()):
            #     print(i, memory['kz'])
            #     bin = pulses_to_bin([memory['kz'][k] for k in ['qq', 'sj', 'ls', 'bg']])
            #     print(i, bin)
            for key in ['dl', 'hb', 'hf', 'lq']:
                if key in pulses and pulses[key] == False:
                    print(i+1, key, pulses)
                    exit()

            # Sum pulses
            for values in pulses.values():
                for val in values:
                    count_pulses[val] += 1

            new_pulses = defaultdict(list)  # already defaults to OrderedDict in current Python?
            new_pulse_order = []
            # for module, pulse_list in pulses.items():
            for module in pulse_order:
                pulse_list = pulses[module]
                pulse = pulse_list.pop(0)
                # print(module)
                # Testing endpoints
                if module not in modules:
                    continue
                new_value = pulse
                mtype, dests = modules[module]
                # % flip-flop
                if mtype == '%':
                    # If input high -> do nothing
                    if pulse:
                        continue
                    # If input low -> flip state
                    if not pulse:
                        # if off, do "on" sequence
                        if not active[module]:
                            # print("on", module)
                            active[module] = True
                            new_value = True
                        # If on, do "off" sequence
                        else:
                            # print("off", module)
                            active[module] = False    
                            new_value = False
                # & conjunction
                elif mtype == '&':
                    mem = memory[module]
                    # print(module, mem)
                    new_value = not all(mem.values())
                for dest in dests:
                    new_pulses[dest].append(new_value)
                    new_pulse_order.append(dest)
                    # print(module, dest)
                    memory[dest][module] = new_value
            assert set(new_pulse_order) == set(new_pulses.keys())
            pulses = new_pulses
            pulse_order = new_pulse_order
            # assert new_pulse_order == list(new_pulses.keys()), f"{new_pulse_order} vs. {list(new_pulses.keys())}"
        # print(count_pulses)
        # print(active)
        # exit()
    print(prod(count_pulses.values()))
    print(rx_got_pulse)


if __name__ == '__main__':
    main()
