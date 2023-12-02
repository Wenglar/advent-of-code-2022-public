
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

point = (x_min-1, y_min-1, z_min-1)
paths = [point]
flooded = set()
flooded.add(point)

# flood outside area of the boulder
while paths:
    point = paths.pop(0)
    x, y, z = point
    if point in boulder:
        # point is not outside areay but part of boulder -> loose it
        continue
    neighbours = (
        (x+1, y, z),
        (x-1, y, z),
        (x, y+1, z),
        (x, y-1, z),
        (x, y, z+1),
        (x, y, z-1)
    )
    add = set([0, 1, 2, 3, 4, 5])
    for index, neighbour in enumerate(neighbours):
        x, y, z = neighbour
        if neighbour in boulder:
            add.remove(index)
        elif (x < x_min - 1 or x > x_max + 2 or
                y < y_min - 1 or y > y_max + 2 or
                z < z_min - 1 or z > z_max + 2):
            add.remove(index)
        elif neighbour in flooded:
            add.remove(index)
    for i in add:
        flooded.add(neighbours[i])
        paths.append(neighbours[i])

# reconstruct the boulder
boulder = set()
for x in range(x_min, x_max+1):
    for y in range(y_min, y_max+1):
        for z in range(z_min, z_max+1):
            if (x, y, z) not in flooded:
                boulder.add((x,y,z))
                surface = 6

# calculate the surface
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

# 45 min
print('part2:', total_surface)
