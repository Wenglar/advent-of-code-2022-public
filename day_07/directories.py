import os
import copy

from pathlib import Path


FILE = os.path.join(os.path.dirname(__file__), 'input.txt')

start = True
file_system = {}    # store files and their sizes in paths if there are any
directories = {}    # store directories in paths if there are any
current_dir = str(Path('root'))
directories[current_dir] = []
listing = False

with open(FILE, 'r') as f:
    line_raw = f.readline()
    while line_raw:
        line = line_raw.replace('\n', '').split(' ')
        if line[0] == r'$':         # command
            listing = False
            if line[1] == 'cd':
                if line[2] == r'/':
                    current_dir = str(Path('root'))
                else:
                    tmp = Path(current_dir) / line[2]
                    current_dir = str(tmp.resolve())
                if not current_dir in file_system:
                    file_system[current_dir] = None
                if not current_dir in directories:
                    directories[current_dir] = []
            if line[1] == 'ls':
                listing = True
        elif listing:
            if line[0] == 'dir':
                tmp = Path(current_dir) / line[1]
                new_dir = str(tmp.resolve())
                if not new_dir in file_system:
                    file_system[new_dir] = None
                    directories[current_dir].append(new_dir)
            else:
                size = int(line[0])
                item = line[1]
                if file_system[current_dir] is None:
                    file_system[current_dir] = {}
                file_system[current_dir][item] = size
        line_raw = f.readline()


def get_size(dir):
    size = 0
    if file_system[dir]:
        for value in file_system[dir].values():
            size += value
    if directories[dir]:
        for subdir in directories[dir]:
            size += get_size(subdir)
    return size

sizes = {}
for dir in directories:
    sizes[dir] = get_size(dir)

total = 0
for size in sizes.values():
    if size <= 100000:
        total += size

print(total)

print('part 2 =========================')
free = 70000000 - max(sizes.values())
to_free = 70000000
for size in sizes.values():
    if (free + size >= 30000000) and (size <= to_free):
        to_free = size
print(to_free)
