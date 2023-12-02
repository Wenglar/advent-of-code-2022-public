import os
import re
import copy


class Elf():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.destination = None

    def set_destination(self, destination):
        self.destination = destination

    def perform_movement(self):
        self.x, self.y = self.destination


class Direction():
    def __init__(self, movement):
        assert movement[0] == 0 or movement[1] == 0
        assert abs(movement[0]) == 1 or abs(movement[1]) == 1

        self.x, self.y = movement
        self.explore = []

        for i in range(-1, 2):
            if movement[0] == 0:
                self.explore.append((i, movement[1]))
            else:
                self.explore.append((movement[0], i))


def print_elves(elves):
    x_min = elves[0].x
    x_max = elves[0].x
    y_min = elves[0].y
    y_max = elves[0].y

    for elf in elves:
        if elf.x < x_min:
            x_min = elf.x
        elif elf.x > x_max:
            x_max = elf.x
        if elf.y < y_min:
            y_min = elf.y
        elif elf.y > y_max:
            y_max = elf.y

    for y in range(y_min, y_max+1):
        line = ['.'] * (x_max - x_min + 1)
        for elf in elves:
            if elf.y == y:
                line[elf.x - x_min] = '#'
        print(''.join(line))

    empty_spaces = (x_max - x_min + 1) * (y_max - y_min + 1) - len(elves)
    print(empty_spaces)


DIRECTION_LIST = ('N', 'S', 'W', 'E')

DIRECTIONS = {
    'N': Direction((0, -1)),
    'S': Direction((0, 1)),
    'W': Direction((-1, 0)),
    'E': Direction((1, 0)),
}

dummy = (
    '....#..\n',
    '..###.#\n',
    '#...#.#\n',
    '.#...##\n',
    '#.###..\n',
    '##.#.##\n',
    '.#..#..\n',
)

FILE = os.path.join(os.path.dirname(__file__), 'input.txt')

elves = []

y = 0
with open(FILE, 'r') as f:
    line_raw = f.readline()
    while line_raw:
    # for line_raw in dummy:
        line = line_raw.replace('\n', '')
        for x, ch in enumerate(line):
            if ch == '#':
                elves.append(Elf(x, y))
        y += 1
        line_raw = f.readline()


ROUNDS = 10

print_elves(elves)

for r in range(ROUNDS):
    positions = set()
    for elf in elves:
        positions.add((elf.x, elf.y))

    destinations = {}

    # elves try to decide their next movement
    for index, elf in enumerate(elves):
        neighbours = (
            (elf.x-1, elf.y+1),
            (elf.x, elf.y+1),
            (elf.x+1, elf.y+1),
            (elf.x-1, elf.y),
            (elf.x+1, elf.y),
            (elf.x-1, elf.y-1),
            (elf.x, elf.y-1),
            (elf.x+1, elf.y-1),
        )
        alone = True
        for neighbour in neighbours:
            if neighbour in positions:
                alone = False
                break
        if alone:
            continue

        for dir_raw in range(r, r+4):
            dir_key = DIRECTION_LIST[dir_raw % 4]
            direction = DIRECTIONS[dir_key]

            other_elf = False
            for x, y in direction.explore:
                expl = (elf.x + x, elf.y + y)
                if expl in positions:
                    other_elf = True
                    break

            if not other_elf:
                dest = (elf.x + direction.x, elf.y + direction.y)
                # print(index, dir_key, dest)
                elf = elves[index]
                elf.set_destination(dest)
                elves[index] = elf
                if dest in destinations:
                    destinations[dest].append(index)
                else:
                    destinations[dest] = [index]
                break

    # print(len(positions))
    # print(positions)
    # print(destinations)
    # if more elves want in the same direction, they dont move
    for dest in destinations.values():
        if len(dest) == 1:
            elf = elves[dest[0]]
            elf.perform_movement()
            elves[dest[0]] = elf

print_elves(elves)
