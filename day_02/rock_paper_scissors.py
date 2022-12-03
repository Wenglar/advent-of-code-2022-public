
import os


FILE = os.path.join(os.path.dirname(__file__), 'input.txt')

points = {
    'X': {
        'A': 1 + 3,
        'B': 1 + 0,
        'C': 1 + 6,
    },
    'Y': {
        'A': 2 + 6,
        'B': 2 + 3,
        'C': 2 + 0,
    },
    'Z': {
        'A': 3 + 0,
        'B': 3 + 6,
        'C': 3 + 3,
    },
}

strategy = {
    'A': {
        'X': 'Z',
        'Y': 'X',
        'Z': 'Y',
    },
    'B': {
        'X': 'X',
        'Y': 'Y',
        'Z': 'Z',
    },
    'C': {
        'X': 'Y',
        'Y': 'Z',
        'Z': 'X',
    },
}

score = 0

with open(FILE, 'r') as f:
    line = f.readline()
    while line:
        enemy = line[0]
        me = line[2]
        score += points[me][enemy]
        line = f.readline()

print(score)

score = 0

with open(FILE, 'r') as f:
    line = f.readline()
    while line:
        enemy = line[0]
        approach = line[2]
        me = strategy[enemy][approach]
        score += points[me][enemy]
        line = f.readline()

print(score)
