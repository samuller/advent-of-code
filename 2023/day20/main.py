#!/usr/bin/env python3
import fileinput
from collections import defaultdict
import sys; sys.path.append("../..")
from lib import *


def init_memory(modules):
    memory = defaultdict(dict)
    for src, (mtype, dests) in modules.items():
        for dest in dests:
            memory[dest][src] = False
    return memory


# [8:08] 569597952 - too low
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

    # { dest: value }
    active = defaultdict(bool)
    count_pulses = {False: 0, True: 0}
    for i in range(1000):
        print(i+1)
        pulses = { 'broadcaster': False }
        while len(pulses) > 0:
            print(' ' * 4, ':', pulses)
            # print(i, ':', states)
            # print('  ', memory)

            # Sum pulses
            for value in pulses.values():
                count_pulses[value] += 1

            new_pulses = {}
            for module, pulse in pulses.items():
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
                    new_pulses[dest] = new_value
                    memory[dest][module] = new_value
            pulses = new_pulses
        print(count_pulses)
        # print(active)
        # exit()
    print(prod(count_pulses.values()))


if __name__ == '__main__':
    main()
