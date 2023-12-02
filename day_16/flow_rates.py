
import os
import copy
import re

from pathlib import Path


FILE = os.path.join(os.path.dirname(__file__), 'input.txt')


inputs = (
    'Valve AA has flow rate=0; tunnels lead to valves DD, II, BB\n'
    'Valve BB has flow rate=13; tunnels lead to valves CC, AA\n'
    'Valve CC has flow rate=2; tunnels lead to valves DD, BB\n'
    'Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE\n'
    'Valve EE has flow rate=3; tunnels lead to valves FF, DD\n'
    'Valve FF has flow rate=0; tunnels lead to valves EE, GG\n'
    'Valve GG has flow rate=0; tunnels lead to valves FF, HH\n'
    'Valve HH has flow rate=22; tunnel leads to valve GG\n'
    'Valve II has flow rate=0; tunnels lead to valves AA, JJ\n'
    'Valve JJ has flow rate=21; tunnel leads to valve II\n'
)

pattern = re.compile(r'Valve (\S+) has flow rate=(\d+); tunnels{0,1} leads{0,1} to valves{0,1} (.*)\n')

with open(FILE, 'r') as f:
    file_raw = f.read()
matches = pattern.findall(file_raw)

# matches = pattern.findall(inputs)

valves = {}

for match in matches:
    key = match[0]
    rate = int(match[1])
    connections = match[2].replace(' ', '').split(',')

    valves[key] = {
        'rate': rate,
        'tunnels': connections
    }

valves_filtered = {}
keys_filtered = [key for key, content in valves.items() if (content['rate'] != 0 or key == 'AA')]

for key in keys_filtered:
    to_explore = set(keys_filtered)
    to_explore.remove(key)

    tunnels_processed = {}

    for destination in to_explore:
        paths = [{'position': key, 'cost': 0}]
        visited = set([key])
        while True:
            path = paths.pop(0)
            position = path['position']
            if position == destination:
                # break and output
                tunnels_processed[destination] = path['cost'] + 1   # +1 for valve activation
                break
            else:
                tunnels = valves[position]['tunnels']
                for tunnel in tunnels:
                    if tunnel not in visited:
                        visited.add(tunnel)
                        paths.append(
                            {'position': tunnel, 'cost': path['cost'] + 1}
                        )
    valves_filtered[key] = {
        'rate': valves[key]['rate'],
        'tunnels': tunnels_processed
    }

valve_cnt = len(valves_filtered)
print('valve count', valve_cnt)

MINUTES = 30

path = {
    'position': 'AA',
    'open': [],
    'visited': set(['AA']),
    'total_flow': 0,
    'total_release': 0,
    'length': 0,
}
paths = [path]

total_release = 0
paths_explored = 0

best_path = path

while paths:
    stay_still = False
    path = paths.pop(-1)

    if path['length'] == MINUTES:
        paths_explored += 1
        if paths_explored % 10000 == 0:
            print('paths explored:', paths_explored, 'best path pressure release: ', best_path['total_release'])
        if path['total_release'] > best_path['total_release']:
            best_path = path
        continue    # in last turn there is no point in opening valves or moving
    if path['length'] > MINUTES:
        print('error', path)
        break

    # path['total_release'] += path['total_flow']

    position = path['position']
    path['visited'].add(position)

    # open valve if possible
    # if valves_filtered[position]['rate'] == 0 or position in path['open']:
    #     pass    # do not open valves with flow rate 0 or already opened valves
    # else:
    #     new_path = copy.deepcopy(path)
    #     new_path['open'].append(position)
    #     new_path['total_flow'] += valves_filtered[position]['rate']
    #     paths.append(new_path)

    # print(len(path['visited']), valve_cnt)

    # explore tunnels
    if len(path['visited']) < valve_cnt:
        tunnels = valves_filtered[position]['tunnels']
        # print(tunnels)
        for tunnel, length in tunnels.items():
            if tunnel in path['visited']:
                pass    # no point wiggling back and forth
            elif path['length'] + length > MINUTES:
                stay_still = True   # if movement cannot be done in time limit, don't move
            else:
                new_path = copy.deepcopy(path)
                new_path['position'] = tunnel
                new_path['length'] += length
                new_path['total_release'] += (new_path['total_flow'] * length)
                new_path['open'].append(tunnel)
                new_path['total_flow'] += valves_filtered[tunnel]['rate']
                paths.append(new_path)
    else:
        # if all valves have been visited, just wait
        stay_still = True

    if stay_still:
        length = MINUTES - path['length']
        path['total_release'] += (path['total_flow'] * length)
        path['length'] = MINUTES
        paths.append(path)

# progress = []
# flow = 0
# position = 0
# for i in range(30):
#     distance = 
print('explored paths:', paths_explored)
print('best path:', best_path)
# 5406 too high
# 5036 too high
