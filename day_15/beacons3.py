"""
updated beacons2.py for whole map walkthrough
"""

import os
import copy
import re
import time

from pathlib import Path


FILE = os.path.join(os.path.dirname(__file__), 'input.txt')


MAGIC = 4000000

dummy = (
    'Sensor at x=2, y=18: closest beacon is at x=-2, y=15\n'
    'Sensor at x=9, y=16: closest beacon is at x=10, y=16\n'
    'Sensor at x=13, y=2: closest beacon is at x=15, y=3\n'
    'Sensor at x=12, y=14: closest beacon is at x=10, y=16\n'
    'Sensor at x=10, y=20: closest beacon is at x=10, y=16\n'
    'Sensor at x=14, y=17: closest beacon is at x=10, y=16\n'
    'Sensor at x=8, y=7: closest beacon is at x=2, y=10\n'
    'Sensor at x=2, y=0: closest beacon is at x=2, y=10\n'
    'Sensor at x=0, y=11: closest beacon is at x=2, y=10\n'
    'Sensor at x=20, y=14: closest beacon is at x=25, y=17\n'
    'Sensor at x=17, y=20: closest beacon is at x=21, y=22\n'
    'Sensor at x=16, y=7: closest beacon is at x=15, y=3\n'
    'Sensor at x=14, y=3: closest beacon is at x=15, y=3\n'
    'Sensor at x=20, y=1: closest beacon is at x=15, y=3\n'
)

pattern = re.compile(r'Sensor at x=(-{0,1}\d+), y=(-{0,1}\d+): closest beacon is at x=(-{0,1}\d+), y=(-{0,1}\d+)\n')

matches = pattern.findall(dummy)

sensors = []
for match in matches:
    sensors.append({
        'sensor': {
            'x': int(match[0]),
            'y': int(match[1]),
        },
        'beacon': {
            'x': int(match[2]),
            'y': int(match[3]),
        }
    })


for Y in range(0, 20+1):
    line_raw = {}
    occupied_y = set()

    for s in sensors:
        x = s['sensor']['x']
        y = s['sensor']['y']
        if y == Y:
            occupied_y.add(x)
        x_b = s['beacon']['x']
        y_b = s['beacon']['y']
        if y_b == Y:
            occupied_y.add(x_b)
        manhattan_distance = abs(x-x_b) + abs(y-y_b)

        y_distance = abs(y-Y)

        spread = manhattan_distance - y_distance

        if not spread < 0:
            if x not in line_raw:
                line_raw[x] = spread
            else:
                if spread > line_raw[x]:
                    line_raw[x] = spread

    keys = list([key for key in line_raw])
    keys.sort()
    index = 0
    while index < len(keys):
        removed = False
        point = keys[index]
        spread = line_raw[point]
        key_set = set(keys)
        key_set.remove(point)

        for point2 in key_set:
            spread2 = line_raw[point2]
            x1 = point - spread
            x2 = point + spread
            y1 = point2 - spread2
            y2 = point2 + spread2
            if x1 >= y1 and x2 <= y2:
                keys.pop(index)
                removed = True
                break

        if not removed:
            index += 1

    line_filtered = {}
    for key in keys:
        line_filtered[key] = line_raw[key]

    line = []
    for point, spread in line_filtered.items():
        x1 = point - spread
        x2 = point + spread
        if len(line) == 0:
            line.append([x1, x2])
        else:
            if line[-1][1] + 1 >= x1:
                line[-1][1] = x2
            else:
                line.append([x1, x2])

    if len(line) > 1:
        print(line)
        x = line[0][-1] + 1
        print(x, Y, x*MAGIC+Y)

# part 2
with open(FILE, 'r') as f:
    file_raw = f.read()

matches = pattern.findall(file_raw)

sensors = []
for match in matches:
    sensors.append({
        'sensor': {
            'x': int(match[0]),
            'y': int(match[1]),
        },
        'beacon': {
            'x': int(match[2]),
            'y': int(match[3]),
        }
    })

tic = time.perf_counter()
for Y in range(0, MAGIC+1):
    line_raw = {}
    occupied_y = set()

    for s in sensors:
        x = s['sensor']['x']
        y = s['sensor']['y']
        if y == Y:
            occupied_y.add(x)
        x_b = s['beacon']['x']
        y_b = s['beacon']['y']
        if y_b == Y:
            occupied_y.add(x_b)
        manhattan_distance = abs(x-x_b) + abs(y-y_b)

        y_distance = abs(y-Y)

        spread = manhattan_distance - y_distance

        if not spread < 0:
            if x not in line_raw:
                line_raw[x] = spread
            else:
                if spread > line_raw[x]:
                    line_raw[x] = spread

    keys = list([key for key in line_raw])
    keys.sort()
    index = 0
    while index < len(keys):
        removed = False
        point = keys[index]
        spread = line_raw[point]
        key_set = set(keys)
        key_set.remove(point)

        for point2 in key_set:
            spread2 = line_raw[point2]
            x1 = point - spread
            x2 = point + spread
            y1 = point2 - spread2
            y2 = point2 + spread2
            if x1 >= y1 and x2 <= y2:
                keys.pop(index)
                removed = True
                break

        if not removed:
            index += 1

    line_filtered = {}
    for key in keys:
        line_filtered[key] = line_raw[key]

    line = []
    for point, spread in line_filtered.items():
        x1 = point - spread
        x2 = point + spread
        if len(line) == 0:
            line.append([x1, x2])
        else:
            if line[-1][1] + 1 >= x1:
                line[-1][1] = x2
            else:
                line.append([x1, x2])

    if Y % 100000 == 0:
        print(Y, '/', MAGIC)

    if len(line) > 1:
        print(line)
        x = line[0][-1] + 1
        print(x, Y, x*MAGIC+Y)

print(time.perf_counter() - tic, 's')
