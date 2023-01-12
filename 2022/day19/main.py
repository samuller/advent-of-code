#!/usr/bin/env python3
import time
import fileinput
from dataclasses import dataclass
from collections import namedtuple

import sys; sys.path.append("../..")
from lib import *


ResourceTypes = namedtuple('ResourceTypes', ['ore', 'clay', 'obsidian', 'geode'])

# State = namedtuple('State', ['mins_left', 'resources', 'robots'])
@dataclass
class State:
    mins_left: int
    resources: list
    robots: list


def calc_blueprint(blueprint):
    mins_per_ore = 1
    mins_per_robot = 1
    mins_left = 24

    # blueprint = costs

    # possible_timelines = [
    #     State(
    #         mins_left,
    #         resources=list(ResourceTypes(0, 0, 0, 0)),
    #         robots=list(ResourceTypes(ore=1, clay=0, obsidian=0, geode=0))
    #     )
    # ]
    # # completed_options = []
    # most_geodes = 0

    # start_time = time.time()
    # count = 0
    # while len(possible_timelines) > 0:
    #     print(f"#{count+1} timelines: {len(possible_timelines)} (time taken: {time.time() - start_time:.2f}s)")
    #     count += 1
    #     # Process any completed timelines
    #     for idx in range(len(possible_timelines)-1, -1, -1):
    #         timeline = possible_timelines[idx]
    #         if timeline.mins_left == 0:
    #             geodes = ResourceTypes(*timeline.resources).geode
    #             if geodes > most_geodes:
    #                 most_geodes = geodes
    #             # completed_options.append(timeline)
    #             del possible_timelines[idx]

    #     # Process current timelines
    #     new_timelines = []
    #     for timeline in possible_timelines:
    #         resources_before = list(timeline.resources)
    #         # Mine ore
    #         for idx, robot_count in enumerate(timeline.robots):
    #             timeline.resources[idx] += 1*robot_count
    #         timeline.mins_left -= 1
    #         # Create new timelines where we constructed each option of whatever we can
    #         for idx, robot in enumerate(reversed(list(blueprint))):
    #             # Check if we can afford to build it
    #             # Have to use resources before we mined it (the robot is only constructed after this point in time)
    #             if all([(a >= b) for a, b in zip(resources_before, robot)]):
    #                 # print(f"Build: {robot} ({resources})")
    #                 new_resources = [r1 - r2 for r1, r2 in zip(resources_before, robot)]
    #                 new_robots = list(timeline.robots)
    #                 new_robots[3 - idx] += 1
    #                 new_timelines.append(
    #                     State(
    #                         timeline.mins_left,
    #                         resources=new_resources,
    #                         robots=new_robots
    #                     )
    #                 )

    #     possible_timelines.extend(new_timelines)

    # return most_geodes

    # =rate
    robots = list(ResourceTypes(ore=1, clay=0, obsidian=0, geode=0))
    resources = list(ResourceTypes(0, 0, 0, 0))

    while mins_left > 0:
        print(mins_left, resources, ResourceTypes(*robots))  # ResourceTypes(*resources))

        # future_value = []
        # for idx, robot in enumerate(list(blueprint)):
        #     value = ResourceTypes(0, 0, 0, 0)
        #     value[idx] = mins_left - 1
        #     future_value.append(value)

        # # Greedily construct best onoe robot we can
        # for idx, robot in enumerate(reversed(list(blueprint))):
        #     # future_value = 
        #     # print([(a >= b) for a, b in zip(resources,robot)])
        #     # If we can build it, do it
        #     if all([(a >= b) for a, b in zip(resources, robot)]):
        #         # print(f"Build: {robot} ({resources})")
        #         resources = [r1 - r2 for r1, r2 in zip(resources, robot)]
        #         robots[3 - idx] += 1
        #         break
        #         # mins_left -= mins_per_robot
        #         # if mins_left <= 0:
        #         #     break

        resources_before = list(resources)

        # Mine ore
        for idx, robot_count in enumerate(robots):
            resources[idx] += 1*robot_count

        # 9:52 Build only ore-makers and see what the optimum is
        # if mins_left > 4 and ResourceTypes(*resources_before).ore >= ResourceTypes(*blueprint[0]).ore:
        #     resources = [r1 - r2 for r1, r2 in zip(resources, blueprint[0])]
        #     print(f"+{robots[0]}* (={resources[0]})")
        #     robots[0] += 1
        # else:
        #     print(f"+{robots[0]} (={resources[0]})")

        # 14:15 - always build geode-bot if we've reached max-production rate
        build = None
        if all([rate >= cost for rate, cost in zip(robots, blueprint.geode)]):
            build = ResourceTypes._fields.index('geode')

        if build is not None and all([have >= cost for have, cost in zip(resources_before, blueprint[build])]):
            resources = [r1 - r2 for r1, r2 in zip(resources, blueprint[build])]
            robots[build] += 1

        # All ore mining and construction of 1 robot happen simultaneously
        mins_left -= 1
        if mins_left <= 0:
            break

        # if mins_left == 18:
        #     exit()
    print(resources, robots)
    exit()
    return ResourceTypes(*resources).geode


# 7:47 - think about optimization problem...
# 8:25 - take break (have brute force approach that takes 5 mins per blueprint...)
# 9:30-10:00 - back thinking
# 14:15-14:45 - back for a bit
def main():
    lines = [line.replace("\n", "") for line in fileinput.input()]

    fluff = None
    nums_in_line = [6, 12, 18, 21, 27, 30]
    blueprints = []
    for idx, line in enumerate(lines):
        words = line.split()
        id = int(words[1].replace(":", ""))
        assert id == idx + 1
        costs = [int(w) for idx, w in enumerate(words) if idx in nums_in_line]

        if fluff is None:
            fluff = [w for idx, w in enumerate(words) if idx not in [1, *nums_in_line]]
        curr_fluff = [w for idx, w in enumerate(words) if idx not in [1, *nums_in_line]]
        assert fluff == curr_fluff, f"\n{' '.join(fluff)} vs. \n{' '.join(curr_fluff)}"

        cost_per_robot = ResourceTypes(
            ore=ResourceTypes(ore=costs[0], clay=0, obsidian=0, geode=0),
            clay=ResourceTypes(ore=costs[1], clay=0, obsidian=0, geode=0), 
            obsidian=ResourceTypes(ore=costs[2], clay=costs[3], obsidian=0, geode=0),
            geode=ResourceTypes(ore=costs[4], clay=0, obsidian=costs[5], geode=0)
        )
        blueprints.append(cost_per_robot)

    # for idx, bp in enumerate(blueprints):
    #     print(idx)
    #     for rbt in bp:
    #         print("  ", rbt)

    # calc_blueprint(blueprints[0])

    qualities = []
    for idx, bp in enumerate(blueprints):
        id = idx + 1
        geodes = calc_blueprint(bp)
        quality = id * geodes
        qualities.append(quality)
        print(id, geodes, quality)
    print(sum(qualities))


if __name__ == '__main__':
    main()

# 9:40
# +1
# +1
# +1
# +1
# +1* (=1)
# +2
# +2
# +2* (=3)
# +3
# +3* (=5)
# +4* (=5)
# +5* (=6)
# +6* (=8)
# +7* (=11)
# +8* (=15)
# +9* (=20)
# +10* (=26)
# +11* (=33)
# +12* (=41)            45
# +13* (=50)        54  58
# +14* (=60)    64  68  72
# +15 (=71) 75  79  83  87
# +16 (=83) 91  95  99  103
# +17 (=96) 108 112 116 120