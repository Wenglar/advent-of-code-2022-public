import os
import re
import copy

dummy = (
    '        ...#\n',
    '        .#..\n',
    '        #...\n',
    '        ....\n',
    '...#.......#\n',
    '........#...\n',
    '..#....#....\n',
    '..........#.\n',
    '        ...#....\n',
    '        .....#..\n',
    '        .#......\n',
    '        ......#.\n',
    '\n',
    '10R5L5R10L4R5L5\n',
)

ORIENTATION_POINTS = {
    (1, 0): 0,
    (0, 1): 1,
    (-1, 0): 2,
    (0, -1): 3
}

N = 4   # for the dummy
N = 50  # for real data

FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
MULTIPLY = 811589153

pattern = re.compile(r'(\d+)([RL]){0,1}')

part = 0
maze = {}
directions = []
y = 0
start = None

x_min = 1
x_max = 1
y_min = 1
y_max = 1

with open(FILE, 'r') as f:
    line_raw = f.readline()
    while line_raw:
    # for line_raw in dummy:
        line = line_raw.replace('\n', '')
        if line == '':
            part = 1
        elif part == 0:
            x = 0
            y += 1
            for x, ch in enumerate(line):
                if ch in ('.', '#'):
                    maze[(x+1,y)] = ch
                    if y == 1 and start is None:
                        start = (x + 1, y)
            if x + 1 > x_max:
                x_max = x + 1
            if y > y_max:
                y_max = y
        elif part == 1:
            matches = pattern.findall(line)
            for match in matches:
                directions.append((int(match[0]), match[1]))
        line_raw = f.readline()

print(directions)

position = start
orientation = (1, 0)

print(position)
print(orientation)

for direction in directions:
    length = direction[0]
    turn = direction[1]
    # translation
    x, y = position
    x_new, y_new = position
    for _ in range(length):
        x_new += orientation[0]
        y_new += orientation[1]
        # print('step: ', x_new, y_new)
        # if over edge of maze
        if (x_new, y_new) not in maze:
            # overflow to the other side of map
            if x_new > x:
                x_new = x_min
            elif x_new < x:
                x_new = x_max
            elif y_new > y:
                y_new = y_min
            elif y_new < y:
                y_new = y_max
            # find edge of maze
            while (x_new, y_new) not in maze:
                x_new += orientation[0]
                y_new += orientation[1]
        # obstacle check
        new_position = (x_new, y_new)
        if maze[new_position] == '#':
            break   # if obstacle stop on previous spot
        else:
            x, y = x_new, y_new     # if no obstacle, make step
    position = (x, y)
    # print(position)

    # rotation
    # note: y is 1 at the top and grows to the bottom
    if turn == '':
        print('end')
    elif ((orientation == (1, 0) and turn == 'R') or
            (orientation == (-1, 0) and turn == 'L')):
        orientation = (0, 1)
    elif ((orientation == (1, 0) and turn == 'L') or
            (orientation == (-1, 0) and turn == 'R')):
        orientation = (0, -1)
    elif ((orientation == (0, 1) and turn == 'R') or
            (orientation == (0, -1) and turn == 'L')):
        orientation = (-1, 0)
    elif ((orientation == (0, 1) and turn == 'L') or
            (orientation == (0, -1) and turn == 'R')):
        orientation = (1, 0)
    # print(turn, orientation)

print(position, orientation)

points = 1000 * position[1] + 4 * position[0] + ORIENTATION_POINTS[orientation]

print(points)

# matches = pattern.findall(file_raw)
# # matches = pattern.findall(dummy)