import os
import copy

from pathlib import Path


FILE = os.path.join(os.path.dirname(__file__), 'input.txt')

actions = []

def make_head_step(position, direction):
    if direction == 'U':
        position[1] += 1
    elif direction == 'D':
        position[1] -= 1
    elif direction == 'R':
        position[0] += 1
    elif direction == 'L':
        position[0] -= 1
    else:
        raise ValueError(f'"{direction}" is not a valid input for head movement')

    return position


def make_tail_step(head_position, tail_position):
    x = head_position[0] - tail_position[0]
    y = head_position[1] - tail_position[1]

    tail = copy.deepcopy(tail_position)

    x_abs = abs(x)
    y_abs = abs(y)
    manhattan_distance = x_abs + y_abs

    if (x_abs <= 1 and y_abs <= 1):
        pass    # no movement
    elif (manhattan_distance == 2):
        # straight movement
        if x == 0:
            tail[1] += (y // y_abs)
        else:
            tail[0] += (x // x_abs)
    else:
        # diagonal movement
        tail[0] += (x // x_abs)
        tail[1] += (y // y_abs)

    return tail


with open(FILE, 'r') as f:
    line_raw = f.readline()
    while line_raw:
        line = line_raw.replace('\n', '').split(' ')
        action = {'direction': line[0], 'cnt': int(line[1])}
        actions.append(action)
        line_raw = f.readline()

visited = set([(0, 0)])

head_position = [0, 0]
tail_position = [0, 0]

for action in actions:
    for _ in range(action['cnt']):
        head_position = make_head_step(head_position, action['direction'])
        tail_position = make_tail_step(head_position, tail_position)
        visited.add(tuple(tail_position))

print(len(visited))


visited = set([(0, 0)])

head_position = [0, 0]
tail_cnt = 9
tails = []
for i in range(tail_cnt):
    tails.append([0, 0])

for j, action in enumerate(actions):
    for _ in range(action['cnt']):
        head_position = make_head_step(head_position, action['direction'])
        for i in range(tail_cnt):
            if i == 0:
                tails[0] = make_tail_step(head_position, tails[0])
            else:
                tails[i] = make_tail_step(tails[i-1], tails[i])

        visited.add(tuple(tails[-1]))

print(len(visited))
