"""
updated flow_rates.py to two workers
"""

import os
import copy
import re
import itertools

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
valves_for_exploration = set(valves_filtered.keys())
valves_for_exploration.remove('AA')

print('valve count', valve_cnt)
print(valves_filtered['AA'])

MINUTES = 26

path = {
    'paths': [{
        'position': 'AA',
        # 'length': 0,
        'cooldown': 0,
        'addition': 0
    },{
        'position': 'AA',
        # 'length': 0,
        'cooldown': 0,
        'addition': 0
    }],
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

print('AA:', valves_filtered['AA'])

while paths:
    # print(paths)
    path = paths.pop(-1)

    # get minimum cooldown
    steps = min(
        path['paths'][0]['cooldown'],
        path['paths'][1]['cooldown']
    )
    # print(path)
    # print(steps)
    # input()

    # if not zero, increase pressure relief
    if steps > 0:
        # relief pressure
        path['total_release'] += (path['total_flow'] * steps)
        path['length'] += steps
        # increase flow for path that performed all remaining steps
        if path['paths'][0]['cooldown'] - steps == 0 and path['length'] != MINUTES:
            path['total_flow'] += path['paths'][0]['addition']
            path['paths'][0]['addition'] = 0
            path['open'].append(path['paths'][0]['position'])
        if path['paths'][1]['cooldown'] - steps == 0 and path['length'] != MINUTES:
            path['total_flow'] += path['paths'][1]['addition']
            path['paths'][1]['addition'] = 0
            path['open'].append(path['paths'][1]['position'])
        # perform steps
        path['paths'][0]['cooldown'] -= steps
        path['paths'][1]['cooldown'] -= steps

        # print(path)
        # input()

    # if reached length, evaluate
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

    to_end = MINUTES - path['length']

    # if one path cannot perform steps, explore tunnels
    if steps == 0:
        valves = copy.deepcopy(valves_for_exploration)
        for v in path['visited']:
            if v in valves:
                valves.remove(v)
        # print(valves)
        # if both paths can explore
        if path['paths'][0]['cooldown'] == 0 and path['paths'][1]['cooldown'] == 0:
            # print('double')
            stay_still = False
            len_valves = len(valves)
            # print(len_valves)
            if len_valves > 1:
                valve_combos = itertools.combinations(valves, 2)
                # print(len(list(valve_combos)))
                # exit()
            elif len_valves == 1:
                valve_combos = [[list(valves)[0], None]]
            else:
                valve_combos = [[None, None]]
            for combo in valve_combos:
                ends = 0
                # if there is no other valve to be explored, wait till the end
                if combo[0] is None and combo[1] is None:
                    # print('nowhere to move')
                    new_path = copy.deepcopy(path)
                    new_path['paths'][0]['cooldown'] = to_end
                    new_path['paths'][1]['cooldown'] = to_end
                    paths.append(new_path)

                else:
                    # the same valves can be reached by various length, therefore both possibilities shall be explored
                    # print('combo exploration')
                    range_ = 2
                    if path['paths'][0]['position'] == path['paths'][1]['position']:
                        # this should occur only once (at the beginning)
                        range_ = 1
                    for i in range(range_):
                        ends = 0
                        position_0 = path['paths'][0]['position']
                        length_0 = valves_filtered[position_0]['tunnels'][combo[0]]
                        # print(position_0, length_0)
                        new_path = copy.deepcopy(path)
                        if path['length'] + length_0 >= MINUTES:
                            new_path['paths'][i]['cooldown'] = to_end
                            ends += 1
                        else:
                            new_path['paths'][i]['cooldown'] = length_0
                            new_path['paths'][i]['position'] = combo[0]
                            new_path['paths'][i]['addition'] = valves_filtered[combo[0]]['rate']
                            new_path['visited'].add(combo[0])
                        if combo[1]:
                            position_1 = path['paths'][1]['position']
                            length_1 = valves_filtered[position_1]['tunnels'][combo[1]]
                            # print(combo[0], length_0, combo[1], length_1)
                            if path['length'] + length_1 >= MINUTES:
                                new_path['paths'][1-i]['cooldown'] = to_end
                                ends += 1
                            else:
                                new_path['paths'][1-i]['cooldown'] = length_1
                                new_path['paths'][1-i]['position'] = combo[1]
                                new_path['paths'][1-i]['addition'] = valves_filtered[combo[1]]['rate']
                                new_path['visited'].add(combo[1])
                        else:
                            new_path['paths'][1-i]['cooldown'] = to_end

                        if ends < 2:
                            # if at least one path got expanded, add to stack
                            paths.append(new_path)
                            # print(combo[0], length_0, combo[1], length_1)
                            # print(new_path)
                        elif not stay_still:
                            # if neither path got expanded and it is the first time, add to stack
                            paths.append(new_path)
                            stay_still = True
                        else:
                            # if neither path got expanded and it is not the first case, ignore
                            pass
        # if one path can explore
        else:
            # print('single')
            for i in range(2):
                stay_still = False
                if path['paths'][i]['cooldown'] == 0:
                    position = path['paths'][i]['position']
                    tunnels = valves_filtered[position]['tunnels']

                    for tunnel, length in tunnels.items():
                        if len(list(valves)) == 0:
                            stay_still = True
                        elif tunnel not in valves:
                            # print(f'wiggle: tunnel {tunnel}, valves {valves}')
                            pass    # no point wiggling back and forth
                        elif path['length'] + length >= MINUTES:
                            stay_still = True   # if movement cannot be done in time limit, don't move
                        else:
                            if tunnel in path['visited']:
                                print('what')
                            new_path = copy.deepcopy(path)
                            new_path['paths'][i]['position'] = tunnel
                            new_path['paths'][i]['cooldown'] = length
                            new_path['paths'][i]['addition'] = valves_filtered[tunnel]['rate']
                            new_path['visited'].add(tunnel)
                            paths.append(new_path)

                if stay_still:
                    new_path = copy.deepcopy(path)
                    new_path['paths'][i]['cooldown'] = to_end
                    paths.append(new_path)

    else:
        paths.append(path)
    # if stay_still:
    #     print('here')
    #     for i in range(2):
    #         position =  path['paths'][i]['position']
    #         path['paths'][i]['cooldown'] -= 1
    #         if path['paths'][i]['cooldown'] == 0:
    #             path['open'].append(position)
    #             path['total_flow'] += path['paths'][i]['addition']
    #             path['paths'][i]['addition'] = 0
    #     paths.append(new_path)

# progress = []
# flow = 0
# position = 0
# for i in range(30):
#     distance = 
print('explored paths:', paths_explored)
print('best path:', best_path)
# 2308 is too low
