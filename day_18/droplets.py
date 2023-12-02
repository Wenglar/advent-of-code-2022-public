
import os
import copy
import re

from pathlib import Path


FILE = os.path.join(os.path.dirname(__file__), 'input.txt')


dummy = (
    '2,2,2\n'
    '1,2,2\n'
    '3,2,2\n'
    '2,1,2\n'
    '2,3,2\n'
    '2,2,1\n'
    '2,2,3\n'
    '2,2,4\n'
    '2,2,6\n'
    '1,2,5\n'
    '3,2,5\n'
    '2,1,5\n'
    '2,3,5\n'
)

pattern = re.compile(r'(\d+),(\d+),(\d+)')

with open(FILE, 'r') as f:
    file_raw = f.read()
matches = pattern.findall(file_raw)

# matches = pattern.findall(dummy)

boulder = set()
x_s = set()
y_s = set()
z_s = set()

for match in matches:
    x = int(match[0])
    y = int(match[1])
    z = int(match[2])
    x_s.add(x)
    y_s.add(y)
    z_s.add(z)
    cube = (x, y, z)
    boulder.add(cube)

total_surface = 0
for point in boulder:
    surface = 6
    x, y, z = point
    neighbours = (
        (x+1, y, z),
        (x-1, y, z),
        (x, y+1, z),
        (x, y-1, z),
        (x, y, z+1),
        (x, y, z-1)
    )
    for neighbour in neighbours:
        if neighbour in boulder:
            surface -= 1
    total_surface += surface

print('part1:', total_surface)

# 10 min

x_min = min(x_s)
x_max = max(x_s)
y_min = min(y_s)
y_max = max(y_s)
z_min = min(z_s)
z_max = max(z_s)

# get rid of 1 cube bubbles
for x in range(x_min, x_max+1):
    for y in range(y_min, y_max+1):
        for z in range(z_min, z_max+1):
            if (x, y, z) not in boulder:
                surface = 6
                neighbours = (
                    (x+1, y, z),
                    (x-1, y, z),
                    (x, y+1, z),
                    (x, y-1, z),
                    (x, y, z+1),
                    (x, y, z-1)
                )
                for neighbour in neighbours:
                    if neighbour in boulder:
                        surface -= 1
                if surface == 0:
                    # if enclosed
                    boulder.add((x,y,z))

total_surface = 0
for point in boulder:
    surface = 6
    x, y, z = point
    neighbours = (
        (x+1, y, z),
        (x-1, y, z),
        (x, y+1, z),
        (x, y-1, z),
        (x, y, z+1),
        (x, y, z-1)
    )
    for neighbour in neighbours:
        if neighbour in boulder:
            surface -= 1
    total_surface += surface

# 4120 is too high
print('part2:', total_surface)
