#!/usr/bin/env python3
import itertools
import time
import fileinput
from random import random, randint
from collections import defaultdict, namedtuple

import sys; sys.path.append("../..")
from lib import *


ActionAt = namedtuple('ActionAt', ['time_left', 'action', 'location'])


def choose_any(listy):
    assert len(listy) > 0
    return listy[randint(0, len(listy) - 1)]


def find_shortest_route(start, dest, routes):
    """BFS"""
    shortest = []
    if start == dest:
        return shortest

    dist_to_node = {}
    visited = set()
    visited_from = {}

    def get_full_path(end, beg):
        nonlocal visited_from
        curr_node = end
        path = []
        while curr_node != beg:
            path.append(curr_node)
            curr_node = visited_from[curr_node]
        return list(reversed(path))

    queue = [start]
    dist_to_node[start] = 0
    while len(queue) > 0:
        curr_node = queue.pop(0)
        visited.add(curr_node)
        for next_node in routes[curr_node]:
            if next_node not in visited and next_node not in queue:
                queue.append(next_node)
                visited_from[next_node] = curr_node
                dist_to_node[next_node] = dist_to_node[curr_node] + 1

            # print(queue, visited, dist_to_node)

            if next_node == dest:
                # shortest = [next_node]
                shortest = get_full_path(next_node, start)
                assert len(shortest) == dist_to_node[dest], dist_to_node[dest]
                return shortest

    return shortest


def estimate_all_valves_left(sim):
    """Find best valve to open in whole graph, accounting for travel time.

    Ignores opening valves en-route, re-evaluating once we've moved a bit, etc....
    """
    curr_valve = sim.curr_valve
    routes = sim.routes
    flow_rates = sim.flow_rates
    already_opened = sim.opened_valves
    time_left = sim.time_left

    # Calculate to release possible from each valve without travel time
    open_gains = {}
    for valve in routes:
        if valve in already_opened:
            continue
        open_gains[valve] = flow_rates[valve] * time_left
    # print(open_gains)
    # Now subtract travel time
    full_gains = {}
    paths = {}
    for idx, dest_valve in enumerate(open_gains):
        short_route = find_shortest_route(curr_valve, dest_valve, routes)
        pressure_time_lost_while_moving = len(short_route)*flow_rates[dest_valve]
        full_gains[dest_valve] = open_gains[dest_valve] - pressure_time_lost_while_moving
        paths[dest_valve] = short_route
        # print(f"{curr_valve} -> {dest_valve}", short_route)
    # print(full_gains)
    return full_gains, paths


def find_only_point_left(simulation):
    full_gains, paths_taken = estimate_all_valves_left(simulation)
    options_left = [key for key, val in full_gains.items() if val > 0]
    if len(options_left) == 1:
        only_valve = options_left[0]
        return only_valve, paths_taken[only_valve]
    return None, []


def find_any_point_left(simulation):
    full_gains, paths_taken = estimate_all_valves_left(simulation)
    options_left = [key for key, val in full_gains.items() if val > 0]
    if len(options_left) == 0:
        return None, []
    any_valve = choose_any(options_left)
    return any_valve, paths_taken[any_valve]


def find_best_point_left(simulation):
    full_gains, paths_taken = estimate_all_valves_left(simulation)

    best_valve = None
    best_valve_gain = 0
    best_path = []
    for key in full_gains:
        if full_gains[key] > best_valve_gain:
            best_valve_gain = full_gains[key]
            best_valve = key
            best_path = paths_taken[key]
            # # Randomly choose non-optimal path (works on test data...)
            if random() > 0.5:
                return best_valve, best_path
    return best_valve, best_path


class Simulation:
    def __init__(self, routes, flow_rates) -> None:
        self.routes = routes
        self.flow_rates = flow_rates

        self.time_per_route = 1
        self.time_per_valve_open = 1

        self.time_left = 30
        self.curr_valve = 'AA'
        self.opened_valves = set()
        self.opened_at = {}
        self.actions_taken = []

    def done(self):
        assert self.time_left >= 0
        return self.time_left == 0

    def update_time(self):
        if self.done():
            return
        self.time_left -= 1

    def open_valve(self, valve):
        assert valve not in self.opened_valves, valve
        if self.done():
            return
        self.opened_valves.add(valve)
        for _ in range(self.time_per_valve_open):
            self.update_time()
        self.opened_at[valve] = self.time_left
        self.actions_taken.append(ActionAt(self.time_left, 'open', valve))
        # print(f"opened {valve} releasing {flow_rates[valve]}, time left: {time_left}")

    def move_to(self, new_valve):
        if self.done():
            return
        assert new_valve in self.routes[self.curr_valve]
        self.curr_valve = new_valve
        for _ in range(self.time_per_route):
            self.update_time()
        self.actions_taken.append(ActionAt(self.time_left, 'move', new_valve))
        # print(f"moving to {new_valve}, time left: {time_left}")

    def wait(self):
        if self.done():
            return
        self.update_time()
        self.actions_taken.append(ActionAt(self.time_left, 'wait', self.curr_valve))

    def follow_path(self, path):
        if self.done():
            return
        next_valves = self.routes[self.curr_valve]
        for valve in path:
            assert valve in next_valves
            self.move_to(valve)
            next_valves = self.routes[self.curr_valve]
        self.open_valve(self.curr_valve)

    def calc_total_pressure_released(self):
        all_time_open = [self.flow_rates[vlv]*time_open for vlv, time_open in self.opened_at.items()]
        # print(all_time_open)
        return sum(all_time_open)


def simulate(routes, flow_rates):
    # Part 1
    sim = Simulation(routes, flow_rates)

    # if curr_valve not in opened_valves and flow_rates[curr_valve] > 0:
    #     open_valve(curr_valve)
    while sim.time_left > 0:
        # attempt #1 to get needed code in place - just move and open nearby things

        # attempt #2
        # # Find best point in whole graph to move towards
        # best_point, best_path = find_best_point_left(sim)
        # # print(best_point, best_path)
        # if best_point is not None:
        #     sim.follow_path(best_path)
        # else:
        #     # Just wait around
        #     # print(f"waiting at {curr_valve}...")
        #     sim.wait()

        # attempt #3 - try random actions
        # #3.1 If only one option left, then take it
        # maybe, maybe_path = find_only_point_left(curr_valve, routes, flow_rates, opened_valves, time_left)
        # if maybe is not None:
        #     follow_path(maybe_path)
        # else:
        # #3.0 Move fully randomly
        # next_valve = choose_any(routes[curr_valve])
        # #3.2 Move randomly towards any valid node (but only one step)
        goal_valve, path_to_next = find_any_point_left(sim)
        sim.actions_taken.append(ActionAt(sim.time_left, 'goal', goal_valve))
        if goal_valve is None:
            sim.wait()
            continue
        elif goal_valve == sim.curr_valve:
            # Valve should be opened
            pass
        else:
            next_valve = path_to_next[0]
            sim.move_to(next_valve)
        if sim.curr_valve not in sim.opened_valves and flow_rates[sim.curr_valve] > 0:
            # Randomly open currently one (likely)
            if random() > 0.1:
                sim.open_valve(sim.curr_valve)

    # print(opened_at)
    # # Ground truth on test data
    # opened_at = {'DD': 2, 'BB': 5, 'JJ': 9, 'HH': 17, 'EE': 21, 'CC': 24}
    # opened_at = {key: 30-val for key, val in opened_at.items()}

    part1 = sim.calc_total_pressure_released()
    # print(part1)
    return part1, sim.actions_taken


# Attempt #4
def try_all_options(routes, flow_rates):
    # sim = Simulation(routes, flow_rates)
    start = "AA"  #sim.curr_valve
    time_left_start = 30
    # Part 2
    # start = ("AA", "AA")
    # time_left_start = 26

    # Find all possible options (routes + openings)
    all_valid_valves = [valve for valve in flow_rates if flow_rates[valve] > 0]
    State = namedtuple('State', ['time_left', 'curr_valve', 'unopened_valves', 'pressure_released', 'release_rate'])
    curr_states = set([State(time_left_start, start, frozenset(all_valid_valves), 0, 0)])
    best_state = next(iter(curr_states))
    start_time = time.time()
    while len(curr_states) > 0:
        new_states = set()
        start_time_step = time.time()
        for state in curr_states:
            # Remove done states
            if state.time_left <= 0:
                continue
            # States that are done, but their release rate stills needs to be accounted for all the way to time = 0
            if len(state.unopened_valves) == 0:
                new_states.add(State(
                    0,
                    state.curr_valve,
                    state.unopened_valves,
                    state.pressure_released + (state.release_rate*state.time_left),
                    state.release_rate
                ))
                continue

            # for curr_value in state.curr_valve:  # part 2
            for curr_valve in [state.curr_valve]:  # part 1
                # Move to all possible valves (without opening current)
                for next_valve in routes.get_adjacent(curr_valve): #routes[state.curr_valve]:
                    path_len = routes.get_weight(curr_valve, next_valve)
                    if path_len > state.time_left:
                        continue
                    new_states.add(State(
                        state.time_left - path_len,
                        next_valve,
                        state.unopened_valves,
                        state.pressure_released + path_len*state.release_rate,
                        state.release_rate
                    ))
                if curr_valve in state.unopened_valves:
                    # Open current valve (and leave follow-up routes for next round)
                    new_unopened_valves = set(state.unopened_valves)
                    new_unopened_valves.remove(curr_valve)
                    # new_unopened_valves = frozenset([vlv for vlv in state.unopened_valves if vlv != curr_valve])
                    new_states.add(State(
                        state.time_left - 1,
                        curr_valve,
                        frozenset(new_unopened_valves),
                        state.pressure_released + state.release_rate,
                        state.release_rate + flow_rates[curr_valve]
                    ))

        curr_states = new_states
        # print(len(curr_states))
        # for state in curr_states:
        #     print(state)
        # print()

        for state in curr_states:
            # if (state.time_left == 0 or len(state.unopened_valves) == 0)
            if state.pressure_released > best_state.pressure_released:
                best_state = state
        # done_states = [st for st in curr_states if st.time_left == 0]
        # if len(done_states) > 0:
        #     print('done:', len(done_states))
        #     for state in done_states:
        #         print(' ', state)

        # Grab any value
        any_value = best_state
        if len(curr_states) > 0:
            any_value = next(iter(curr_states))
        total_time_taken = time.time() - start_time
        step_time_taken = time.time() - start_time_step
        print(f'{any_value.time_left}: {len(curr_states):,} at {total_time_taken:.2f}s (+{step_time_taken:.2f}s)')
        print(f"{best_state.pressure_released} ({best_state.time_left}/{best_state.curr_valve}/{len(best_state.unopened_valves)}/+{best_state.release_rate})")
    print(best_state)
    print(best_state.pressure_released)


def print_dot(graph, flow_rates):
    # Graphviz: dot test.dot -Tpdf > test.pdf
    print("graph {")
    for id in graph.get_nodes():
        id_str = id
        # Highlight empty paths...
        if flow_rates[id] == 0:
            id_str = f'"{id}*"'
        for valve in graph.get_adjacent(id):
            vlv_str = valve
            if flow_rates[valve] == 0:
                vlv_str = f'"{valve}*"'
            print(f'{id_str} -- {vlv_str}')
    print("}")


def simplify_graph(graph, flow_rates):
    # Simplify graph
    for valve in flow_rates:
        # Skip starting node
        if valve == "AA":
            continue
        if flow_rates[valve] == 0:
            graph.remove_node(valve)
            # print(valve, graph)

# 14:36
class UndirectedGraph:
    def __init__(self) -> None:
        self.neighbours = defaultdict(set)
        self.weights = {}

    def add_edge(self, node1, node2, weight=1):
        self.update_weight(node1, node2, weight)
        self.neighbours[node1].add(node2)
        self.neighbours[node2].add(node1)

    def get_nodes(self):
        return list(self.neighbours.keys())

    def get_adjacent(self, node):
        return self.neighbours[node]

    def get_weight(self, node1, node2):
        return self.weights[tuple(sorted([node1, node2]))]

    def update_weight(self, node1, node2, weight=1):
        key = tuple(sorted([node1, node2]))
        if key in self.weights:
            # Don't override if there's already a shorted edge connection (e.g. when deleting nodes)
            weight = min(weight, self.weights[key])
        self.weights[tuple(sorted([node1, node2]))] = weight

    def delete_weight(self, node1, node2):
        del self.weights[tuple(sorted([node1, node2]))]

    def remove_node(self, node):
        # Find connected nodes
        nears = self.get_adjacent(node).copy()
        # Connect those nodes to each other
        for combo in itertools.combinations(nears, 2):
            new_weight = self.get_weight(node, combo[0]) + self.get_weight(node, combo[1])
            self.add_edge(*combo, weight=new_weight)
        # Remove node and weights
        del self.neighbours[node]
        for near in nears:
            self.delete_weight(node, near)
            self.neighbours[near].remove(node)

    def __str__(self) -> str:
        return f"{self.neighbours} / {self.weights}"

# 8:26 - too low 1662 (#2 sub-optimal + wrong calc - added before subtracting opening time)
# 8:53 - too low 1706 (#3 random)
# 8:59 - too low 1762 (#3 random)
# 9:27 - not right 1907 (#3/#3.1 random)
# 1738 after 28.92s?
# 10:38 - wrong 1724 after 698.12s (right for someone else?)
# 1760 after 4147.84s? (12:09)
# 12:31 - 1944 (#4 all possibilities after 12m30s + 12Gb RAM)
def main():
    lines = [line.replace("\n", "") for line in fileinput.input()]
    # Parse input
    # routes = defaultdict(list)
    flow_rates = {}
    graph = UndirectedGraph()
    for line in lines:
        words = line.split()
        id = words[1]
        flow_rate = int(words[4].replace("rate=", "").replace(";", ""))
        next_valves = [wrd.replace(",", "") for wrd in words[9:]]
        # print(id, flow_rate, next_valves)
        flow_rates[id] = flow_rate
        # routes[id] = next_valves
        for nxt in next_valves:
            graph.add_edge(id, nxt, 1)

    # print(flow_rates)
    # print(routes)
    # print(graph)

    # simplify_graph(graph, flow_rates)

    # print(graph)
    # print_dot(graph, flow_rates)
    # exit()

    # time_started = time.time()
    # best_found = 0
    # count = 0
    # try:
    #     while True:
    #         found, actions = simulate(routes, flow_rates)
    #         if found >= best_found:
    #             best_found = found
    #             # print(actions)
    #             for act in actions:
    #                 if act[2]:
    #                     print('  ', act[0], act[1], act[2])
    #             time_passed = time.time() - time_started
    #             print(f'{best_found} after {time_passed:.2f}s')
    #         count += 1
    # except KeyboardInterrupt:
    #     print()
    #     print("Count:", count)
    #     raise

    try_all_options(graph, flow_rates)


if __name__ == '__main__':
    main()
