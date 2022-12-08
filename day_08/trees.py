import os
import copy

from pathlib import Path


FILE = os.path.join(os.path.dirname(__file__), 'input.txt')

forrest = []


with open(FILE, 'r') as f:
    line_raw = f.readline()
    while line_raw:
        line = []
        for nr in line_raw.replace('\n', ''):
            line.append(int(nr))
        forrest.append(line)
        line_raw = f.readline()

y_size = len(forrest)
x_size = len(forrest[0])

high_score = 0
v_cnt = 0
total_cnt = x_size * y_size

for y in range(y_size):
    for x in range(x_size):
        visible = [True] * 4
        for x_l in range(0, x):
            if forrest[y][x_l] >= forrest[y][x]:
                visible[0] = False
                break
        for x_r in range(x+1, x_size):
            if forrest[y][x_r] >= forrest[y][x]:
                visible[1] = False
                break
        for y_u in range(0, y):
            if forrest[y_u][x] >= forrest[y][x]:
                visible[2] = False
                break
        for y_l in range(y+1, y_size):
            if forrest[y_l][x] >= forrest[y][x]:
                visible[3] = False
                break
        v = any(visible)
        if v:
            v_cnt += 1

print(f"Visible {v_cnt} out of total {total_cnt}")

for y in range(y_size):
    for x in range(x_size):
        scores = [0] * 4
        for x_l in reversed(range(0, x)):
            scores[0] += 1
            if forrest[y][x_l] >= forrest[y][x]:
                break
        for x_r in range(x+1, x_size):
            scores[1] += 1
            if forrest[y][x_r] >= forrest[y][x]:
                break
        for y_u in reversed(range(0, y)):
            scores[2] += 1
            if forrest[y_u][x] >= forrest[y][x]:
                break
        for y_l in range(y+1, y_size):
            scores[3] += 1
            if forrest[y_l][x] >= forrest[y][x]:
                break
        score = scores[0] * scores[1] * scores[2] * scores[3]
        if score > high_score:
            high_score = score

print(f"Highest viewing score: {high_score}")
