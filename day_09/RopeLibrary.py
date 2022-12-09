import os
import copy
import enum

from pathlib import Path

from robot.api.logger import info, debug, trace, console  # type:ignore


class RopeLibrary():
    """
    Library for rope knot handling.
    """

    ROBOT_LIBRARY_SCOPE = 'SUITE'

    def __init__(self):
        self.actions = []
        self.knots = []
        self.positions = set([(0, 0)])

    def set_file_and_validate(self, file_path):
        assert isinstance(file_path, str), f'Unexpected type: {type(file_path)}'
        assert os.path.exists(file_path)

        self.file_path = file_path

    def load_directions(self):
        self.actions = []

        with open(self.file_path, 'r') as f:
            line_raw = f.readline().replace('\n', '')

            while line_raw:
                line = line_raw.split(' ')
                self.actions.append({'direction': line[0], 'steps': int(line[1])})
                line_raw = f.readline()

    def verify_knot_count(self, cnt):
        assert cnt > 1, f"There should be at least 2 knots. Got {cnt}."

    def initialize_knots(self, cnt):
        self.knots = []

        for _ in range(cnt):
            self.knots.append([0, 0])

        self.positions = set([(0, 0)])

    def perform_movements(self):
        knot_cnt = len(self.knots)

        for action in self.actions:
            for _ in range(action['steps']):
                self._make_head_step(action['direction'])

                for knot in range(1, knot_cnt):
                    self._make_follower_step(knot)

                self.positions.add(tuple(self.knots[-1]))

    def get_unique_tail_position_count(self):
        return len(self.positions)

    def _make_head_step(self, direction):
        if direction == 'U':
            self.knots[0][1] += 1
        elif direction == 'D':
            self.knots[0][1] -= 1
        elif direction == 'R':
            self.knots[0][0] += 1
        elif direction == 'L':
            self.knots[0][0] -= 1
        else:
            raise ValueError(f'"{direction}" is not a valid input for head movement')

    def _make_follower_step(self, position):
        assert position > 0

        lead = self.knots[position-1]
        follower = self.knots[position]

        x = lead[0] - follower[0]
        y = lead[1] - follower[1]

        x_abs = abs(x)
        y_abs = abs(y)

        manhattan_distance = x_abs + y_abs

        if (x_abs <= 1 and y_abs <= 1):
            # no movement
            pass
        elif (manhattan_distance == 2):
            # straight movement
            if x == 0:
                follower[1] += (y // y_abs)
            else:
                follower[0] += (x // x_abs)
        else:
            # diagonal movement
            if manhattan_distance >> 3 and position == 1:
                raise ValueError(f'Impossible situation for 2nd knot. Lead: {lead}, Follower: {follower}.')
            follower[0] += (x // x_abs)
            follower[1] += (y // y_abs)
