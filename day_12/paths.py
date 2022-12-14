import os
import copy
import re

from pathlib import Path


FILE = os.path.join(os.path.dirname(__file__), 'input.txt')


map = []

start = ()
end = ()

y = 0


dummy = [
    'Sabqponm',
    'abcryxxl',
    'accszExk',
    'acctuvwj',
    'abdefghi',
]


# for line_raw in dummy:
with open(FILE, 'r') as f:
    line_raw = f.readline().replace('\n', '')
    while line_raw:
        line = [*line_raw]
        for x, val in enumerate(line):
            if val == 'S':
                start = (x, y)
                line[x] = 'a'
            elif val == 'E':
                end = (x, y)
                line[x] = 'z'
            if start and end:
                break
        map.append(line)
        y += 1
        line_raw = f.readline().replace('\n', '')


x_size = len(line)
y_size = y


used = {}
for y in range(y_size):
    for x in range(x_size):
        used[(x,y)] = False

# print(used)

used[start] = True
opened = [{
    'position': start,
    'steps': 0
}]
result = {}
search = True


while search:
    path = opened.pop(0)
    steps = path['steps'] + 1
    x,y = path['position']
    val = map[y][x]
    opts = []
    if x > 0:
        opts.append((x-1, y))
    if x < (x_size-1):
        opts.append((x+1, y))
    if y > 0:
        opts.append((x, y-1))
    if y < (y_size-1):
        opts.append((x, y+1))
    index = 0
    while index < len(opts):
        if used[opts[index]]:
            opts.pop(index)
        else:
            x,y = opts[index]
            try:
                if ord(map[y][x]) > (ord(val) + 1):
                    opts.pop(index)
                else:
                    index += 1
            except Exception as ex:
                print((x, y), x_size, y_size)
                raise
    for opt in opts:
        output = {
            'position': opt,
            'steps': steps
        }
        if opt == end:
            result = output
            search = False
            break
        used[opt] = True
        opened.append(output)

print(result)

# part 2

for u in used:
    used[u] = False

opened = [{
    'position': end,
    'steps': 0
}]
result = {}
search = True

while search:
    path = opened.pop(0)
    steps = path['steps'] + 1
    x,y = path['position']
    val = map[y][x]
    opts = []
    if x > 0:
        opts.append((x-1, y))
    if x < (x_size-1):
        opts.append((x+1, y))
    if y > 0:
        opts.append((x, y-1))
    if y < (y_size-1):
        opts.append((x, y+1))
    index = 0
    while index < len(opts):
        if used[opts[index]]:
            opts.pop(index)
        else:
            x,y = opts[index]
            try:
                if ord(map[y][x]) < (ord(val) - 1):
                    opts.pop(index)
                else:
                    index += 1
            except Exception as ex:
                print((x, y), x_size, y_size)
                raise
    for opt in opts:
        output = {
            'position': opt,
            'steps': steps
        }
        x,y = opt
        if map[y][x] == 'a':
            result = output
            search = False
            break
        used[opt] = True
        opened.append(output)

print(result)
