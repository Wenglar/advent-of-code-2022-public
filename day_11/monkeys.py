import os
import copy
import re

from pathlib import Path


FILE = os.path.join(os.path.dirname(__file__), 'input.txt')


class Monkey():
    def __init__(self, id, items, operation, operand, test_val, true_val, false_val):
        self._id: int = id
        self.items: list = items
        self._operation: str = operation
        self._operand: str = operand
        self._test_val: int = test_val
        self._true_val: int = true_val
        self._false_val: int = false_val

        self.inspection_cnt: int = 0

    def inspect_item(self):
        if not self.items:
            raise ValueError('self.items is empty, cannot run the function')

        item = self.items.pop(0)
        item = self.perform_operation(item)
        item = item // 3

        if item % self._test_val == 0:
            target = self._true_val
        else:
            target = self._false_val

        self.inspection_cnt += 1

        return (target, item)

    def perform_operation(self, value):
        if self._operand == 'old':
            operand = value
        else:
            operand = int(self._operand)

        if self._operation == '+':
            output = value + operand
        elif self._operation == '*':
            output = value * operand

        return output


pattern = re.compile(r'Monkey (\d+):\s*Starting items: (.*)\s*Operation: new = old ([\*+]) (\S+)\s*Test: divisible by (\d+)\s*If true: throw to monkey (\d+)\s*If false: throw to monkey (\d+)')


with open(FILE, 'r') as f:
    file_raw = f.read()

# file_raw = """
# Monkey 0:
#   Starting items: 79, 98
#   Operation: new = old * 19
#   Test: divisible by 23
#     If true: throw to monkey 2
#     If false: throw to monkey 3

# Monkey 1:
#   Starting items: 54, 65, 75, 74
#   Operation: new = old + 6
#   Test: divisible by 19
#     If true: throw to monkey 2
#     If false: throw to monkey 0

# Monkey 2:
#   Starting items: 79, 60, 97
#   Operation: new = old * old
#   Test: divisible by 13
#     If true: throw to monkey 1
#     If false: throw to monkey 3

# Monkey 3:
#   Starting items: 74
#   Operation: new = old + 3
#   Test: divisible by 17
#     If true: throw to monkey 0
#     If false: throw to monkey 1

# """

matches = pattern.findall(file_raw)

monkeys = []
for match in matches:
    items_raw = match[1].replace(' ', '').split(',')
    items = list(map(int, items_raw))

    monkey = Monkey(
        id=int(match[0]),
        items=items,
        operation=match[2],
        operand=match[3],
        test_val=int(match[4]),
        true_val=int(match[5]),
        false_val=int(match[6])
    )

    monkeys.append(monkey)

monkey_cnt = len(monkeys)


ROUNDS = 20
for _ in range(ROUNDS):
    for monkey in monkeys:
        while monkey.items:
            (target, item) = monkey.inspect_item()
            monkeys[target].items.append(item)


activity = {}
levels = []
for monkey in monkeys:
    activity[monkey.inspection_cnt] = monkey._id
    levels.append(monkey.inspection_cnt)

levels.sort(reverse=True)
first = activity[levels[0]]
second = activity[levels[1]]

monkey_business = monkeys[first].inspection_cnt * monkeys[second].inspection_cnt

print(f'Monkey business for part 1: {monkey_business}')


FILE = os.path.join(os.path.dirname(__file__), 'input.txt')


class Monkey():
    def __init__(self, id, operation, operand, test_val, true_val, false_val):
        self._id: int = id
        self._operation: str = operation
        self._operand: str = operand
        self._test_val: int = test_val
        self._true_val: int = true_val
        self._false_val: int = false_val

        self.inspection_cnt: int = 0
        self.divider: int = 0

    def inspect_item(self, item):
        assert self.divider > 0
        item = self.perform_operation(item)

        item = item % divider

        if item % self._test_val == 0:
            target = self._true_val
        else:
            target = self._false_val

        self.inspection_cnt += 1

        return (target, item)

    def perform_operation(self, value):
        if self._operand == 'old':
            operand = value
        else:
            operand = int(self._operand)

        if self._operation == '+':
            output = value + operand
        elif self._operation == '*':
            output = value * operand

        return output



with open(FILE, 'r') as f:
    file_raw = f.read()

# file_raw = """
# Monkey 0:
#   Starting items: 79, 98
#   Operation: new = old * 19
#   Test: divisible by 23
#     If true: throw to monkey 2
#     If false: throw to monkey 3

# Monkey 1:
#   Starting items: 54, 65, 75, 74
#   Operation: new = old + 6
#   Test: divisible by 19
#     If true: throw to monkey 2
#     If false: throw to monkey 0

# Monkey 2:
#   Starting items: 79, 60, 97
#   Operation: new = old * old
#   Test: divisible by 13
#     If true: throw to monkey 1
#     If false: throw to monkey 3

# Monkey 3:
#   Starting items: 74
#   Operation: new = old + 3
#   Test: divisible by 17
#     If true: throw to monkey 0
#     If false: throw to monkey 1

# """

matches = pattern.findall(file_raw)

monkeys = []
items_all = []

for index, match in enumerate(matches):
    items_raw = match[1].replace(' ', '').split(',')
    items = list(map(int, items_raw))
    
    for item in items:
        items_all.append(
            {'monkey': index, 'value': item, 'index': len(items_all)}
        )

    monkey = Monkey(
        id=int(match[0]),
        operation=match[2],
        operand=match[3],
        test_val=int(match[4]),
        true_val=int(match[5]),
        false_val=int(match[6])
    )

    monkeys.append(monkey)

divider = 1
for monkey in monkeys:
    divider = divider * monkey._test_val
for monkey in monkeys:
    monkey.divider = divider

print(divider)


ROUNDS = 10000
for i in range(ROUNDS):
    if i % 100 == 0:
        print(f'Round: {i}')
    for index, monkey in enumerate(monkeys):
        for item in items_all:
            if item['monkey'] == index:
                (target, value) = monkey.inspect_item(item['value'])
                items_all[item['index']]['value'] = value
                items_all[item['index']]['monkey'] = target


activity = {}
levels = []
for monkey in monkeys:
    activity[monkey.inspection_cnt] = monkey._id
    levels.append(monkey.inspection_cnt)

print(levels)
levels.sort(reverse=True)
first = activity[levels[0]]
second = activity[levels[1]]

monkey_business = monkeys[first].inspection_cnt * monkeys[second].inspection_cnt

print(f'Monkey business: {monkey_business}')

