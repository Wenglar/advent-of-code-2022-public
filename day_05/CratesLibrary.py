import os
import copy
import enum

from robot.api.logger import info, debug, trace, console  # type:ignore


class Cranes(enum.IntEnum):
    ONE_BY_ONE = 9000
    ALL_IN_ONE = 9001


class CratesLibrary():
    """
    Library for moving crates.
    """

    ROBOT_LIBRARY_SCOPE = 'TEST'

    def __init__(self):
        self.file_path = None
        self.init_state = None
        self.config = None
        self.steps = None
        self.assignment_pairs = []

    def set_file_and_validate(self, file_path):
        assert isinstance(file_path, str), f'Unexpected type: {type(file_path)}'
        assert os.path.exists(file_path)

        self.file_path = file_path

    def extract_initial_state_and_steps(self):
        start = True
        config_raw = []
        steps = []

        with open(self.file_path, 'r') as f:
            line_raw = f.readline()
            while line_raw:
                line = line_raw.replace('\n', '')
                if not line:        # switch between initla state and step parsing
                    start = False
                elif start:         # parse initial state
                    line_list = []
                    size = len(line)
                    index = 1
                    while index < size:
                        char = line[index]
                        if char != ' ':
                            line_list.append(char)
                        else:
                            line_list.append(None)
                        index += 4
                    config_raw.append(line_list)
                else:               # parse steps
                    step_raw = line.split(' ')
                    step = {
                        'cnt': int(step_raw[1]),
                        'from': step_raw[3],
                        'to': step_raw[5],
                    }
                    steps.append(step)
                line_raw = f.readline()

        key = []
        config = {}
        for k in config_raw[-1]:
            key.append(k)
            config[k] = []

        for line in list(reversed(config_raw[:-1])):
            for index, item in enumerate(line):
                if item is not None:
                    config[key[index]].append(item)

        self.init_state = config
        self.steps = steps

    def validate_crane(self, crane):
        assert crane in set(item.value for item in Cranes)

    def apply_steps(self, crane):
        self.config = copy.deepcopy(self.init_state)
        if crane == Cranes.ONE_BY_ONE:
            for step in self.steps:
                for _ in range(1, step['cnt']+1):
                    char = self.config[step['from']].pop(-1)
                    self.config[step['to']].append(char)
        elif crane == Cranes.ALL_IN_ONE:
            for step in self.steps:
                for index in reversed(range(1, step['cnt']+1)):
                    char = self.config[step['from']].pop(-index)
                    self.config[step['to']].append(char)

    def get_top_row(self):
        size = len(self.config)
        msg = [' '] * size
        for i in range(size):
            msg[i] = self.config[str(i+1)][-1]

        return ''.join(msg)
