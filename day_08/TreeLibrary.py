import os
import copy
import enum

from pathlib import Path

from robot.api.logger import info, debug, trace, console  # type:ignore

directory_template = {
    'files': {},
    'folders': [],
    'size': 0
}


class TreeLibrary():
    """
    Library for tree height and view calculation.
    """

    ROBOT_LIBRARY_SCOPE = 'SUITE'

    def __init__(self):
        self.file_path = None
        self.forest = []
        self.x_size = 0
        self.y_size = 0
        self.total_size = 0

    def set_file_and_validate(self, file_path):
        assert isinstance(file_path, str), f'Unexpected type: {type(file_path)}'
        assert os.path.exists(file_path)

        self.file_path = file_path

    def load_forest_layout(self):
        with open(self.file_path, 'r') as f:
            line_raw = f.readline()
            while line_raw:
                line = []
                for nr in line_raw.replace('\n', ''):
                    line.append(int(nr))
                self.forest.append(line)
                line_raw = f.readline()

        self.y_size = len(self.forest)
        self.x_size = len(self.forest[0])
        self.total_size = self.x_size * self.y_size

    def get_total_tree_count(self):
        return self.total_size

    def get_visible_tree_count(self):
        visible_cnt = 0

        for y in range(self.y_size):
            for x in range(self.x_size):
                visible = [True] * 4
                for x_l in range(0, x):
                    if self.forest[y][x_l] >= self.forest[y][x]:
                        visible[0] = False
                        break
                for x_r in range(x+1, self.x_size):
                    if self.forest[y][x_r] >= self.forest[y][x]:
                        visible[1] = False
                        break
                for y_u in range(0, y):
                    if self.forest[y_u][x] >= self.forest[y][x]:
                        visible[2] = False
                        break
                for y_l in range(y+1, self.y_size):
                    if self.forest[y_l][x] >= self.forest[y][x]:
                        visible[3] = False
                        break
                if any(visible):
                    visible_cnt += 1

        return visible_cnt

    def get_highest_viewscore(self):
        high_score = 0

        for y in range(self.y_size):
            for x in range(self.x_size):
                scores = [0] * 4
                for x_l in reversed(range(0, x)):
                    scores[0] += 1
                    if self.forest[y][x_l] >= self.forest[y][x]:
                        break
                for x_r in range(x+1, self.x_size):
                    scores[1] += 1
                    if self.forest[y][x_r] >= self.forest[y][x]:
                        break
                for y_u in reversed(range(0, y)):
                    scores[2] += 1
                    if self.forest[y_u][x] >= self.forest[y][x]:
                        break
                for y_l in range(y+1, self.y_size):
                    scores[3] += 1
                    if self.forest[y_l][x] >= self.forest[y][x]:
                        break
                score = scores[0] * scores[1] * scores[2] * scores[3]
                if score > high_score:
                    high_score = score

        return high_score
