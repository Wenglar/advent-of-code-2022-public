import os
import re
import copy
import enum

from pathlib import Path

from robot.api.logger import info, debug, trace, console  # type:ignore


class ExplorationLibrary():
    """
    Library for hill exploration.
    """

    ROBOT_LIBRARY_SCOPE = 'TEST'

    def __init__(self):
        self.file_path = None
        self._map = []
        self._start = None
        self._end = None
        self._x_size = None
        self._y_size = None
        self._used = {}
        self._opened = []

    def set_file_and_validate(self, file_path):
        assert isinstance(file_path, str), f'Unexpected type: {type(file_path)}'
        assert os.path.exists(file_path)

        self.file_path = file_path

    def load_file(self):
        self._map = []
        y = 0

        with open(self.file_path, 'r') as f:
            line_raw = f.readline().replace('\n', '')
            while line_raw:
                line = [*line_raw]
                for x, val in enumerate(line):
                    if val == 'S':
                        self._start = (x, y)
                        line[x] = 'a'
                    elif val == 'E':
                        self._end = (x, y)
                        line[x] = 'z'
                    if self._start and self._end:
                        break
                self._map.append(line)
                y += 1
                line_raw = f.readline().replace('\n', '')

        self._x_size = len(line)
        self._y_size = y

    def set_start(self, point):
        if point == 'start':
            self._opened = [{
                'position': self._start,
                'steps': 0
            }]
        elif point == 'end':
            self._opened = [{
                'position': self._end,
                'steps': 0
            }]
        else:
            raise ValueError('Invalid input')

        self._used = {}
        for y in range(self._y_size):
            for x in range(self._x_size):
                self._used[(x,y)] = False

    def get_the_shortest_path_to_z(self):
        result = None
        search = True

        while search:
            path = self._opened.pop(0)
            steps = path['steps'] + 1
            x,y = path['position']
            val = self._map[y][x]
            opts = []
            if x > 0:
                opts.append((x-1, y))
            if x < (self._x_size-1):
                opts.append((x+1, y))
            if y > 0:
                opts.append((x, y-1))
            if y < (self._y_size-1):
                opts.append((x, y+1))
            index = 0
            while index < len(opts):
                if self._used[opts[index]]:
                    opts.pop(index)
                else:
                    x,y = opts[index]
                    try:
                        if ord(self._map[y][x]) > (ord(val) + 1):
                            opts.pop(index)
                        else:
                            index += 1
                    except Exception as ex:
                        raise ValueError(f'Coords: ({x},{y}), Dimensions: ({self._x_size}, {self._y_size})')
            for opt in opts:
                output = {
                    'position': opt,
                    'steps': steps
                }
                if opt == self._end:
                    result = output
                    search = False
                    break
                self._used[opt] = True
                self._opened.append(output)

        return result

    def get_the_shortest_path_down(self):
        result = None
        search = True

        while search:
            path = self._opened.pop(0)
            steps = path['steps'] + 1
            x,y = path['position']
            val = self._map[y][x]
            opts = []
            if x > 0:
                opts.append((x-1, y))
            if x < (self._x_size-1):
                opts.append((x+1, y))
            if y > 0:
                opts.append((x, y-1))
            if y < (self._y_size-1):
                opts.append((x, y+1))
            index = 0
            while index < len(opts):
                if self._used[opts[index]]:
                    opts.pop(index)
                else:
                    x,y = opts[index]
                    try:
                        if ord(self._map[y][x]) < (ord(val) - 1):
                            opts.pop(index)
                        else:
                            index += 1
                    except Exception as ex:
                        raise ValueError(f'Coords: ({x},{y}), Dimensions: ({self._x_size}, {self._y_size})')
            for opt in opts:
                output = {
                    'position': opt,
                    'steps': steps
                }
                x,y = opt
                if self._map[y][x] == 'a':
                    result = output
                    search = False
                    break
                self._used[opt] = True
                self._opened.append(output)

        return result
