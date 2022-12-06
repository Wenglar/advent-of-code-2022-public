import os
import copy
import enum

from robot.api.logger import info, debug, trace, console  # type:ignore


class TuningLibrary():
    """
    Library for finding unique sets.
    """

    ROBOT_LIBRARY_SCOPE = 'SUITE'

    def __init__(self):
        self.file_path = None

    def set_file_and_validate(self, file_path):
        assert isinstance(file_path, str), f'Unexpected type: {type(file_path)}'
        assert os.path.exists(file_path)

        self.file_path = file_path

    def get_first_unique_set(self, element_nr):
        window = ''
        index = element_nr

        with open(self.file_path, 'r') as f:
            char = f.read(element_nr)
            while char:
                window = window[1:] + char
                if len(set(window)) == element_nr:
                    break
                char = f.read(1)
                index += 1

        return index
