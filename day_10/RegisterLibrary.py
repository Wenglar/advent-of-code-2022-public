import os
import copy
import enum

from pathlib import Path

from robot.api.logger import info, debug, trace, console  # type:ignore


class RegisterLibrary():
    """
    Library for register handling.
    """

    ROBOT_LIBRARY_SCOPE = 'TEST'

    def __init__(self):
        self.file_path = None
        self.instructions = []
        self.cycle = 0
        self.cycle_cnt = 0
        self.X = 1
        self.width = 0
        self.display = []
        self.examination = {'index': 0, 'step': 0}
        self.examined = {}
        self._action_cb = None

    def set_file_and_validate(self, file_path):
        assert isinstance(file_path, str), f'Unexpected type: {type(file_path)}'
        assert os.path.exists(file_path)

        self.file_path = file_path

    def load_file(self):
        self.instructions = []
        self.cycle_cnt = 0

        with open(self.file_path, 'r') as f:
            line_raw = f.readline()
            while line_raw:
                line = line_raw.replace('\n', '').split(' ')
                cmd = line[0]
                val = 0
                if len(line) > 1:
                    val = int(line[1])
                    self.cycle_cnt += 2
                else:
                    self.cycle_cnt += 1
                self.instructions.append({'cmd': cmd, 'val': val})
                line_raw = f.readline()

    def set_examined_cycles(self, start, step):
        assert start > 0
        assert step > 0

        self.examination = {'index': start, 'step': step}

    def set_display_width(self, width):
        assert width > 0
        assert width <= self.cycle_cnt

        self.width = width

    def execute_instructions_and_examine_cycles(self):
        self._action_cb = self._examine_cycles

        self._execute_instructions()

    def execute_instructions_and_draw_crt(self):
        self._action_cb = self._get_pixel_illumination

        self._execute_instructions()

    def _execute_instructions(self):
        index = 0
        addition = 0

        while self.cycle < self.cycle_cnt:
            # start of cycle
            instruction = self.instructions[index]
            self.cycle += 1

            # during cycle
            if self._action_cb:
                self._action_cb()

            # end of cycle
            if instruction['cmd'] == 'noop':
                # noop does nothing
                index += 1
            else:
                if addition == 0:
                    # first cycle does nothing
                    addition = instruction['val']
                else:
                    # second cycle performs addition
                    self.X += addition
                    addition = 0
                    index += 1

    def _examine_cycles(self):
        if self.cycle == self.examination['index']:
            self.examined[self.cycle] = self.X
            self.examination['index'] += self.examination['step']

    def _get_pixel_illumination(self):
        position = (self.cycle - 1) % self.width
        if position in [self.X-1, self.X, self.X+1]:
            self.display.append('#')
        else:
            self.display.append('.')

    def get_examined_cycles(self):
        return list([val for val in self.examined])

    def get_sum_of_signal_strengths(self):
        total = 0

        for key, val in self.examined.items():
            total += key * val

        return total

    def get_crt_output(self):
        output = ''

        for i in range(self.cycle_cnt // self.width):
            start = i * self.width
            end = (i + 1) * self.width
            output += ('\n\t\t' + (''.join(self.display[start:end])))

        return output
