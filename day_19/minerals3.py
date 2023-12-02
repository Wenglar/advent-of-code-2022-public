
import os
import copy
import re
import json
import time


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
    def __init__(self, blueprint):
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

    def __deepcopy__(self, memodict={}):
        output = Blueprint()
        output.id_nr = self.id_nr
        output.costs = self.costs
        output.max_costs = self.max_costs
        output.robots = self.robots
        output.resources = self.resources
        output.progress = self.progress

        return output


class MyPath():
    def __init__(self):
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

    # def __deepcopy__(self, memodict={}):
    #     output = MyPath()
    #     output.robots = json.loads(json.dumps(self.robots))
    #     output.resources = json.loads(json.dumps(self.resources))
    #     output.progress = json.loads(json.dumps(self.progress))

    #     return output


TIME_LIMIT = 24

matches = pattern.findall(file_raw)
matches = pattern.findall(dummy)

blueprints = []
evaluations = []

for match in matches:
    blueprints.append(Blueprint(match))

tic = time.perf_counter()
for nr, blueprint in enumerate(blueprints):
    if nr == 3:
        break
    progresses = set()
    # paths = (MyPath(),)
    paths = [MyPath()]
    print(f'Examining blueprint {blueprint.id_nr} / {len(blueprints)}')

    minute = 0
    max_geode = 0
    while minute < TIME_LIMIT:
        minute += 1
        print(f'minute {minute}')

        new_paths = []

        i = 0
        # while paths:
        for path in paths:
            i += 1
            if i % 10000 == 0:
                print(i)
            skip_waiting = False
            # path = paths.pop(0)

            # production
            for key in RESOURCES:
                path.resources[key] += path.robots[key]

            # finish building
            if path.building:
                path.robots[path.building] += 1
                path.building = None

            if minute == TIME_LIMIT:
                if max_geode < path.resources['geode']:
                    max_geode = path.resources['geode']
            else:
                # spend resources and start building (if possible)
                for robot, costs in blueprint.costs.items():
                    # if as many robots as maximum costs, do not produce more
                    if robot in blueprint.max_costs and blueprint.max_costs[robot] <= path.robots[robot]:
                        continue
                    # for round 23 there is no point in creating support robots (23)
                    # no point creating support robots when new geode robot cannot be made afterwards (22)
                    # no point creating support robots when their yield would be first in round 23 (21)
                    if minute in (TIME_LIMIT-3, TIME_LIMIT-2, TIME_LIMIT-1) and robot in ('clay', 'ore', 'obsidian'):
                        continue
                    if minute in (TIME_LIMIT-5, TIME_LIMIT-4) and robot in ('clay', 'ore'):
                        continue
                    if minute in (TIME_LIMIT-7, TIME_LIMIT-6) and robot == 'ore':
                        continue
                    # arbitrary maximum on robots
                    # if robot in blueprint.max_costs and path.robots[robot] >= 6:
                    #     continue
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
                            progresses.add(prog)
                        new_path = copy.deepcopy(path)
                        for resource, cost in costs.items():
                            new_path.resources[resource] -= cost
                        new_path.building = robot
                        new_path.progress.append(robot)

                        new_paths.append(new_path)

                # no spent resources -> wait and accumulate (unless already too many resources)
                skip_waiting = True
                for key in blueprint.max_costs:
                    # if path.robots[key] > 0 and path.resources[key] >= path.max_costs[key]:
                    #     continue
                    # else:
                    #     skip_waiting = False
                    #     break
                    if path.robots[key] > 0:
                        if path.resources[key] >= blueprint.max_costs[key]:
                            continue
                        else:
                            skip_waiting = False
                if not skip_waiting:
                    # new_paths.append(copy.deepcopy(path))
                    new_paths.append(path)

        # paths = copy.deepcopy(new_paths)
        # paths = tuple(new_paths)
        paths = new_paths

    print(blueprint.id_nr, max_geode)
    evaluations.append((blueprint.id_nr, max_geode))

total_score = 0
for evaluation in evaluations:
    score = evaluation[0] * evaluation[1]
    print(f'Score of id {evaluation[0]} with {evaluation[1]} geodes is {score}.')
    total_score += score

toc = time.perf_counter()

print(f'Total score is {total_score}')
# 106 is too low
print(toc - tic)
