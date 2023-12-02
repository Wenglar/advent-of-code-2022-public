import os
import re
import copy

dummy = (
    '1=-0-2\n',
    '12111\n',
    '2=0=\n',
    '21\n',
    '2=01\n',
    '111\n',
    '20012\n',
    '112\n',
    '1=-1=\n',
    '1-12\n',
    '12\n',
    '1=\n',
    '122\n',
)

FILE = os.path.join(os.path.dirname(__file__), 'input.txt')


numbers = []

with open(FILE, 'r') as f:
    line_raw = f.readline()
    while line_raw:
    # for line_raw in dummy:
        line = line_raw.replace('\n', '')
        power = 1
        number = 0
        chars = [*line]
        chars.reverse()
        for ch in chars:
            if ch == '=':
                multiple = -2
            elif ch == '-':
                multiple = -1
            else:
                multiple = int(ch)
            number += (power * multiple)
            power *= 5

        numbers.append(number)
        line_raw = f.readline()

print(numbers)

total = sum(numbers)

print(total)

output = []

while total > 0:
    nr = total % 5
    total = total // 5

    output.append(nr)

output.reverse()

print(output)

for i in range(len(output)-1, 0, -1):
    if output[i] > 2:
        output[i] = output[i] - 5
        output[i-1] += 1
    # output[i] = output[i] - 2

if output[0] > 2:
    output[0] = output[0] - 5
    output.insert(0, 1)

# if output[0] < 0:
#     output.insert(0, 1)

print(output)

snafu = ''

for n in output:
    if n >= 0:
        snafu += str(n)
    elif n == -1:
        snafu += '-'
    elif n == -2:
        snafu += '='

# 2 = - 1 = 0
print(snafu)

