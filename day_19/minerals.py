
import os
import copy
import re

from pathlib import Path


FILE = os.path.join(os.path.dirname(__file__), 'input.txt')


dummy = (
    'Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.\n'
    'Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.\n'
)

pattern = re.compile(
    r'Blueprint (\d+): Each ore robot costs (\d+) ore. '
    r'Each clay robot costs (\d+) ore. '
    r'Each obsidian robot costs (\d+) ore and (\d+) clay. '
    r'Each geode robot costs (\d+) ore and (\d+) obsidian.'
)

with open(FILE, 'r') as f:
    file_raw = f.read()

RESOURCES = ('ore', 'clay', 'obsidian', 'geode')


class Blueprint():
    def __init__(self, blueprint=None):
        if blueprint is not None:
            self.id_nr = int(blueprint[0])
            self.costs = {
                'ore': {
                    'ore': int(blueprint[1])
                },
                'clay': {
                    'ore': int(blueprint[2])
                },
                'obsidian': {
                    'ore': int(blueprint[3]),
                    'clay': int(blueprint[4])
                },
                'geode': {
                    'ore': int(blueprint[5]),
                    'obsidian': int(blueprint[6])
                }
            }
            self.max_costs = {
                'ore': max(int(blueprint[1]), int(blueprint[2]), int(blueprint[3]), int(blueprint[5])),
                'clay': int(blueprint[4]),
                'obsidian': int(blueprint[6])
            }
            self.robots = {
                'ore': 1,
                'clay': 0,
                'obsidian': 0,
                'geode': 0
            }
            self.resources = {
                'ore': 0,
                'clay': 0,
                'obsidian': 0,
                'geode': 0
            }
            self.progress = []
        self.building = None

    def __deepcopy__(self, memodict={}):
        output = Blueprint()
        output.id_nr = self.id_nr
        output.costs = self.costs
        output.max_costs = self.max_costs
        output.robots = self.robots
        output.resources = self.resources
        output.progress = self.progress

        return output


matches = pattern.findall(file_raw)
matches = pattern.findall(dummy)

blueprints = []

for match in matches:
    blueprints.append(Blueprint(match))

for blueprint in blueprints:
    progresses = []
    paths = [copy.deepcopy(blueprint)]

    minute = 0
    while minute < 24:
        minute += 1
        print(f'minute {minute}, paths {len(paths)}')

        new_paths = []

        i = 0
        while paths:
            i += 1
            if i % 1000 == 0:
                print(i)
            skip_waiting = False
            path = paths.pop(0)

            # production
            for key in RESOURCES:
                path.resources[key] += path.robots[key]

            # finish building
            if path.building:
                path.robots[path.building] += 1
                path.building = None

            # spend resources and start building (if possible)
            for robot, costs in path.costs.items():
                # if as many robots as maximum costs, do not produce more
                if robot in path.max_costs and path.max_costs[robot] <= path.robots[robot]:
                    continue
                affordable = True
                for resource, cost in costs.items():
                    if path.resources[resource] < cost:
                        affordable = False
                        break
                if affordable:
                    prog = tuple(path.progress + [robot])
                    # if the same progress path already exists, no point following it in later stages
                    if prog in progresses:
                        continue
                    else:
                        progresses.append(prog)
                    new_path = copy.deepcopy(path)
                    for resource, cost in costs.items():
                        new_path.resources[resource] -= cost
                    new_path.building = robot
                    new_path.progress.append(robot)

                    new_paths.append(new_path)

            # no spent resources -> wait and accumulate (unless already too many resources)
            skip_waiting = True
            for key in path.max_costs:
                # if path.robots[key] > 0 and path.resources[key] >= path.max_costs[key]:
                #     continue
                # else:
                #     skip_waiting = False
                #     break
                if path.robots[key] > 0:
                    if path.resources[key] >= path.max_costs[key]:
                        continue
                    else:
                        skip_waiting = False
            if not skip_waiting:
                new_paths.append(copy.deepcopy(path))

        # paths = copy.deepcopy(new_paths)
        paths = new_paths

