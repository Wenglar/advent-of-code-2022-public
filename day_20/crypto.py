import os
import re
import copy

dummy = (
    '1\n'
    '2\n'
    '-3\n'
    '3\n'
    '-2\n'
    '0\n'
    '4\n'
)

FILE = os.path.join(os.path.dirname(__file__), 'input.txt')

pattern = re.compile(r'(-{0,1}\d+)')

with open(FILE, 'r') as f:
    file_raw = f.read()

matches = pattern.findall(file_raw)
# matches = pattern.findall(dummy)

numbers = []

index = 0
for match in matches:
    numbers.append((int(match), index))
    index += 1

numbers_len = len(matches)

# print(numbers)

numbers_src = copy.deepcopy(numbers)

for val, index in numbers_src:
    i = 0
    for j in range(numbers_len):
        if numbers[j][1] == index:
            i = j
            break

    # print(i, val)
    new_index = (i + val)
    if i == numbers_len-1 and new_index == numbers_len-1:
        pass
    else:
        new_index = (i + val) % (numbers_len-1)
        if new_index == 0:
            new_index = (numbers_len-1)

    number = numbers.pop(i)
    numbers.insert(new_index, number)
    # print(numbers)
    # input()

# print(numbers)

i = 0
for j in range(numbers_len):
    if numbers[j][0] == 0:
        i = j
        break

i_1000 = (i + 1000) % numbers_len
i_2000 = (i + 2000) % numbers_len
i_3000 = (i + 3000) % numbers_len

a = numbers[i_1000][0]
b = numbers[i_2000][0]
c = numbers[i_3000][0]

print(a, b, c, a+b+c)
