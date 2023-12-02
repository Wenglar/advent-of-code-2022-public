import os
import copy

FILE = os.path.join(os.path.dirname(__file__), 'input.txt')

inputs = [
    '498,4 -> 498,6 -> 496,6\n',
    '503,4 -> 502,4 -> 502,9 -> 494,9\n'
]


pairs = []
left = True
pair = {'index': 1}
borders = set()

y_max = 0

with open(FILE, 'r') as f:
    line_raw = f.readline()
    # for line_raw in inputs:
    while line_raw:
        line = line_raw.replace(' -> ', ';').split(';')
        line_len = len(line)
        for i in range(line_len-1):
            left = list(map(int, line[i].split(',')))
            right = list(map(int, line[i+1].split(',')))
            if left[0] == right[0]:
                min_ = min(left[1], right[1])
                max_ = max(left[1], right[1])
                for y in range(min_, max_+1):
                    borders.add((left[0], y))
                    if y > y_max:
                        y_max = y
            elif left[1] == right[1]:
                min_ = min(left[0], right[0])
                max_ = max(left[0], right[0])
                if right[1] > y_max:
                    y_max = right[1]
                for x in range(min_, max_+1):
                    borders.add((x, left[1]))
        line_raw = f.readline()

# part 1
border_len = len(borders)
blocked = copy.deepcopy(borders)

active = False

sand_start = (500, 0)

while True:
    if not active:
        active = True
        sand_x, sand_y = sand_start

    if (sand_x, sand_y+1) not in blocked:
        sand_y += 1
    elif (sand_x-1, sand_y+1) not in blocked:
        sand_y += 1
        sand_x -= 1
    elif (sand_x+1, sand_y+1) not in blocked:
        sand_y += 1
        sand_x += 1
    else:
        active = False
        blocked.add((sand_x, sand_y))

    if sand_y > y_max:
        break

print(len(blocked)-border_len)

# part 2
border_len = len(borders)
blocked = copy.deepcopy(borders)
print(len(blocked))
y_max += 2

active = False

sand_start = (500, 0)

while True:
    if not active:
        active = True
        sand_x, sand_y = sand_start

    if sand_y+1 == y_max:
        active = False
        blocked.add((sand_x, sand_y))
    elif (sand_x, sand_y+1) not in blocked:
        sand_y += 1
    elif (sand_x-1, sand_y+1) not in blocked:
        sand_y += 1
        sand_x -= 1
    elif (sand_x+1, sand_y+1) not in blocked:
        sand_y += 1
        sand_x += 1
    else:
        active = False
        blocked.add((sand_x, sand_y))

    if sand_y == 0:
        break


print(len(blocked)-border_len)
