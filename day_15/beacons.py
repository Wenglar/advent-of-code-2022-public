import os
import copy
import re

from pathlib import Path


FILE = os.path.join(os.path.dirname(__file__), 'input.txt')


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

line_10 = set()
Y = 10

for line in sensors:
    x = line['sensor']['x']
    y = line['sensor']['y']
    x_b = line['beacon']['x']
    y_b = line['beacon']['y']
    manhattan_distance = abs(x-x_b) + abs(y-y_b)

    y_distance = abs(y-Y)

    spread = manhattan_distance - y_distance + 1

    if spread < 0:
        pass
    elif spread == 0:
        line_10.add((x, Y))
    else:
        for i in range(spread):
            line_10.add((x+i, Y))
            line_10.add((x-i, Y))

for line in sensors:
    x = line['sensor']['x']
    y = line['sensor']['y']
    if (x,y) in line_10:
        line_10.remove((x,y))
    x = line['beacon']['x']
    y = line['beacon']['y']
    if (x,y) in line_10:
        line_10.remove((x,y))

print(len(line_10))

# part 1
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

line_2M = set()
Y = 2000000

for line in sensors:
    x = line['sensor']['x']
    y = line['sensor']['y']
    x_b = line['beacon']['x']
    y_b = line['beacon']['y']
    manhattan_distance = abs(x-x_b) + abs(y-y_b)

    y_distance = abs(y-Y)

    spread = manhattan_distance - y_distance + 1

    if spread < 0:
        pass
    elif spread == 0:
        line_2M.add((x, Y))
    else:
        for i in range(spread):
            line_2M.add((x+i, Y))
            line_2M.add((x-i, Y))

for line in sensors:
    x = line['sensor']['x']
    y = line['sensor']['y']
    if (x,y) in line_2M:
        line_2M.remove((x,y))
    x = line['beacon']['x']
    y = line['beacon']['y']
    if (x,y) in line_2M:
        line_2M.remove((x,y))

print(len(line_2M))
# 5394424 too high
