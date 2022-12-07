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


class SpaceLibrary():
    """
    Library for space management.
    """

    ROBOT_LIBRARY_SCOPE = 'SUITE'

    def __init__(self):
        self.file_path = None
        self.file_system = {}

    def set_file_and_validate(self, file_path):
        assert isinstance(file_path, str), f'Unexpected type: {type(file_path)}'
        assert os.path.exists(file_path)

        self.file_path = file_path

    def extract_file_system(self):
        listing = False
        with open(self.file_path, 'r') as f:
            line_raw = f.readline()
            while line_raw:
                line = line_raw.replace('\n', '').split(' ')
                if line[0] == r'$':         # command
                    listing = False
                    if line[1] == 'cd':
                        if line[2] == r'/':
                            current_dir = str(Path('root'))
                        else:
                            tmp = Path(current_dir) / line[2]
                            current_dir = str(tmp.resolve())
                        if not current_dir in self.file_system:
                            self.file_system[current_dir] = copy.deepcopy(directory_template)
                    if line[1] == 'ls':
                        listing = True
                elif listing:
                    if line[0] == 'dir':
                        tmp = Path(current_dir) / line[1]
                        new_dir = str(tmp.resolve())
                        if not new_dir in self.file_system:
                            self.file_system[new_dir] = copy.deepcopy(directory_template)
                            self.file_system[current_dir]['folders'].append(new_dir)
                    else:
                        size = int(line[0])
                        item = line[1]
                        self.file_system[current_dir]['files'][item] = size
                line_raw = f.readline()

        self._get_dir_sizes()

    def _get_size(self, dir):
        size = 0
        if self.file_system[dir]['files']:
            for value in self.file_system[dir]['files'].values():
                size += value
        if self.file_system[dir]['folders']:
            for subdir in self.file_system[dir]['folders']:
                size += self._get_size(subdir)
        return size

    def _get_dir_sizes(self):
        for dir in self.file_system:
            self.file_system[dir]['size'] = self._get_size(dir)

    def get_sum_of_sizes_where_maxsize(self, size):
        output = 0
        for dir in self.file_system:
            folder_size = self.file_system[dir]['size']
            if folder_size <= size:
                output += folder_size
        return output

    def get_lowest_to_free_enough(self, needed, total):
        to_free = total
        free = total - max(item['size'] for item in self.file_system.values())
        for size in (item['size'] for item in self.file_system.values()):
            if (free + size >= needed) and (size <= to_free):
                to_free = size
        return to_free
