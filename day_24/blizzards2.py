import os
import re
import copy

dummy = (
    '#.######\n',
    '#>>.<^<#\n',
    '#.<..<<#\n',
    '#>v.><>#\n',
    '#<^v^^>#\n',
    '######.#\n',
)

FILE = os.path.join(os.path.dirname(__file__), 'input.txt')


class Blizzard():
    X_MIN = 1
    X_MAX = 1
    Y_MIN = 1
    Y_MAX = 1

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        if direction == '>':
            self.direction = (1, 0)
        elif direction == '<':
            self.direction = (-1, 0)
        elif direction == '^':
            self.direction = (0, -1)
        elif direction == 'v':
            self.direction = (0, 1)

    def move(self):
        x = self.x + self.direction[0]
        y = self.y + self.direction[1]

        if x < self.X_MIN:
            x = self.X_MAX
        if x > self.X_MAX:
            x = self.X_MIN
        if y < self.Y_MIN:
            y = self.Y_MAX
        if y > self.Y_MAX:
            y = self.Y_MIN

        self.x = x
        self.y = y

    def get_position(self):
        return (self.x, self.y)

    def __str__(self):
        return f'(Position: ({self.x}, {self.y}); direction: {self.direction})'

    def __repr__(self):
        return f'(Position: ({self.x}, {self.y}); direction: {self.direction})'


def validate_position(position):
    x, y = position
    if ((y >= Blizzard.Y_MIN and y <= Blizzard.Y_MAX) and 
            (x >= Blizzard.X_MIN and x <= Blizzard.X_MAX)):
        return True
    elif position in ((1, 0), (Blizzard.X_MAX, Blizzard.Y_MAX+1)):
        return True
    else:
        return False


blizzards = []

y = 0
start = (1, 0)

x_max = 1

with open(FILE, 'r') as f:
    line_raw = f.readline()
    while line_raw:
    # for line_raw in dummy:
        line = line_raw.replace('\n', '')
        if y == 0:
            x_max = len(line) - 2

        for x, ch in enumerate(line):
            if ch in ('<', '>', '^', 'v'):
                blizzards.append(Blizzard(x, y, ch))
        y += 1
        line_raw = f.readline()

y_max = y - 2

end = (x_max, y_max+1)

Blizzard.X_MAX = x_max
Blizzard.Y_MAX = y_max

paths = [(start[0], start[1], 0)]

minute = 0
end_found = False

while not end_found:
    minute += 1
    if minute % 10 == 0:
        print(f'Running minute {minute}')
    bl_positions = set()
    for blizzard in blizzards:
        blizzard.move()
        bl_positions.add(blizzard.get_position())

    new_paths = set()
    while paths:
        path = paths.pop(0)
        x, y, stage = path
        candidates = (
            (x-1, y),
            (x+1, y),
            (path[0], path[1]),
            (x, y-1),
            (x, y+1),
        )
        for candidate in candidates:
            if validate_position(candidate) and candidate not in bl_positions:
                if stage == 0 and candidate == end:
                    new_path = (candidate[0], candidate[1], 1)
                elif stage == 1 and candidate == start:
                    new_path = (candidate[0], candidate[1], 2)
                elif stage == 2 and candidate == end:
                    end_found = True
                    break
                else:
                    new_path = (candidate[0], candidate[1], stage)
                new_paths.add(new_path)

        if end_found:
            break

    paths = list(new_paths)

print(f'Result: {minute} minutes')
