import os


FILE = os.path.join(os.path.dirname(__file__), 'input.txt')

elves = []

with open(FILE, 'r') as f:
    line = f.readline()
    elves.append(0)
    while line:
        nr_str = line.replace('\n', '')
        if nr_str != '':
            elves[-1] += int(nr_str, 10)
        else:
            elves.append(0)
        line = f.readline()

print('MAX: ', max(elves))

elves = sorted(elves)

print(elves[-3:])
print('MAX3: ', sum(elves[-3:]))
