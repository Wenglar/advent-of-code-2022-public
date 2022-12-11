import os
import re
import copy
import enum

from pathlib import Path

from robot.api.logger import info, debug, trace, console  # type:ignore


class Monkey():
    LEVEL_MANAGEMENT = {'operation': '//', 'operand': 1}

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

        if self.LEVEL_MANAGEMENT['operation'] == '//':
            item = item // self.LEVEL_MANAGEMENT['operand']
        else:
            item = item % self.LEVEL_MANAGEMENT['operand']

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


PATTERN = re.compile(r'Monkey (\d+):\s*Starting items: (.*)\s*Operation: new = old ([\*+]) (\S+)\s*Test: divisible by (\d+)\s*If true: throw to monkey (\d+)\s*If false: throw to monkey (\d+)')


class MonkeyLibrary():
    """
    Library for register monkey and item handling.
    """

    ROBOT_LIBRARY_SCOPE = 'TEST'

    def __init__(self):
        self.file_path = None
        self.monkeys = []
        self.interactions = []

    def set_file_and_validate(self, file_path):
        assert isinstance(file_path, str), f'Unexpected type: {type(file_path)}'
        assert os.path.exists(file_path)

        self.file_path = file_path

    def load_file(self):
        self.monkeys = []

        with open(self.file_path, 'r') as f:
            file_raw = f.read()

        matches = PATTERN.findall(file_raw)

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

            self.monkeys.append(monkey)

    def set_worry_level_management(self, operation, operand):
        assert isinstance(operation, str)
        assert operation in ('//', '%')
        assert operand > 0

        Monkey.LEVEL_MANAGEMENT = {'operation': operation, 'operand': operand}

    def get_product_of_test_dividors(self):
        output = 1

        for monkey in self.monkeys:
            output = output * monkey._test_val

        return output

    def execute_rounds(self, cnt):
        assert cnt > 0

        for _ in range(cnt):
            for monkey in self.monkeys:
                while monkey.items:
                    (target, item) = monkey.inspect_item()
                    self.monkeys[target].items.append(item)

    def get_all_monkey_interactions(self):
        self.interactions = []

        for monkey in self.monkeys:
            self.interactions.append(monkey.inspection_cnt)

        return self.interactions

    def get_monkey_business_level(self):
        levels = self.interactions

        activity = {}
        for monkey in self.monkeys:
            activity[monkey.inspection_cnt] = monkey._id

        levels.sort(reverse=True)
        monkey_business = levels[0] * levels[1]

        return monkey_business
