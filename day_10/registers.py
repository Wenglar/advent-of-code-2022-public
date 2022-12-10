import os
import copy

from pathlib import Path


FILE = os.path.join(os.path.dirname(__file__), 'input.txt')

instructions = []
cycle_max = 0


with open(FILE, 'r') as f:
    line_raw = f.readline()
    while line_raw:
        line = line_raw.replace('\n', '').split(' ')
        if len(line) == 1:
            instructions.append({'cmd': line[0], 'val': 0})
            cycle_max += 1
        else:
            instructions.append({'cmd': line[0], 'val': int(line[1])})
            cycle_max += 2
        line_raw = f.readline()

X = 1
cycle = 0
index = 0
addition = 0

key_point = 20
KEYPOINT_step = 40
key_points = {}

display = []

WIDTH = 40

while cycle < cycle_max:
    # start of cycle
    instruction = instructions[index]
    cycle += 1

    # during cycle
    # part1
    if cycle == key_point:
        key_points[key_point] = X
        key_point += 40

    # part2
    position = (cycle - 1) % WIDTH
    if position in [X-1, X, X+1]:
        display.append('#')
    else:
        display.append('.')

    # end of cycle
    if instruction['cmd'] == 'noop':
        # noop does nothing
        index += 1
    else:
        if addition == 0:
            # first cycle does nothing
            addition = instruction['val']
        else:
            # second cycle performs addition
            X += addition
            addition = 0
            index += 1

print(key_points)

total = 0
for key, val in key_points.items():
    total += (key * val)

print(total)

for i in range(cycle_max//WIDTH):
    start = i*WIDTH
    end = (i+1)*WIDTH
    print(''.join(display[i*WIDTH:(i+1)*WIDTH]))
