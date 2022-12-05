import os
import copy


FILE = os.path.join(os.path.dirname(__file__), 'input.txt')

start = True
config_raw = []
steps = []

with open(FILE, 'r') as f:
    line = f.readline()
    while line:
        row_raw = line.replace('\n', '')
        if not row_raw:
            start = False
        elif start:
            line_list = []
            size = len(row_raw)
            index = 1
            while index < size:
                char = row_raw[index]
                if char != ' ':
                    line_list.append(char)
                else:
                    line_list.append(None)
                index += 4
            config_raw.append(line_list)
        else:
            step_raw = row_raw.split(' ')
            step = {
                'cnt': int(step_raw[1]),
                'from': step_raw[3],
                'to': step_raw[5],
            }
            steps.append(step)
        line = f.readline()

config = {}

key = config_raw[-1]
for k in key:
    config[k] = []
for line in list(reversed(config_raw[:-1])):
    for index, item in enumerate(line):
        if item is not None:
            config[key[index]].append(item)

config_backup = copy.deepcopy(config)

for step in steps:
    for _ in range(step['cnt']):
        char = config[step['from']].pop(-1)
        config[step['to']].append(char)

msg = ''
for key, line in config.items():
    msg += line[-1]

print(msg)

config = copy.deepcopy(config_backup)

for step in steps:
    for i in range(step['cnt']):
        index = -step['cnt'] + i
        char = config[step['from']].pop(index)
        config[step['to']].append(char)

msg = ''
for key, line in config.items():
    msg += line[-1]

print(msg)
