import os

from robot.api.logger import info, debug, trace, console  # type:ignore

RANGE_1_L = 0   # lower bound of first range (assignment)
RANGE_1_U = 1   # upper bound of first range (assignment)
RANGE_2_L = 2   # lower bound of second range (assignment)
RANGE_2_U = 3   # upper bound of second range (assignment)


class AssignmentsLibrary():
    """
    Library for Assignment evaluation.
    """

    ROBOT_LIBRARY_SCOPE = 'TEST'

    def __init__(self):
        self.assignment_pairs = []

    def load_file(self, file_path):
        assert isinstance(file_path, str), f'Unexpected type: {type(file_path)}'
        assert os.path.exists(file_path)

        with open(file_path, 'r') as f:
            line = f.readline()

            while line:
                assignment_pair_raw = line.strip('\n').split(',')
                assignment_pair = []
                for assignment_raw in assignment_pair_raw:
                    assignment = assignment_raw.split('-')
                    assignment_pair.extend([int(assignment[0]), int(assignment[1])])
                self.assignment_pairs.append(assignment_pair)
                line = f.readline()

    def get_count_of_firsts_in_seconds(self):
        cnt = 0

        for assignment_pair in self.assignment_pairs:
            if ((assignment_pair[RANGE_1_L] >= assignment_pair[RANGE_2_L]) and
                    (assignment_pair[RANGE_1_U] <= assignment_pair[RANGE_2_U])):
                cnt += 1

        return cnt

    def get_count_of_seconds_in_firsts(self):
        cnt = 0

        for assignment_pair in self.assignment_pairs:
            if ((assignment_pair[RANGE_2_L] >= assignment_pair[RANGE_1_L]) and
                    (assignment_pair[RANGE_2_U] <= assignment_pair[RANGE_1_U])):
                cnt += 1

        return cnt

    def get_count_of_identical(self):
        cnt = 0

        for assignment_pair in self.assignment_pairs:
            if ((assignment_pair[RANGE_2_L] == assignment_pair[RANGE_1_L]) and
                    (assignment_pair[RANGE_2_U] == assignment_pair[RANGE_1_U])):
                cnt += 1

        return cnt

    def get_count_of_overlaps(self):
        cnt = 0

        for assignment_pair in self.assignment_pairs:
            lower_1 = assignment_pair[RANGE_1_L]
            upper_1 = assignment_pair[RANGE_1_U]
            lower_2 = assignment_pair[RANGE_2_L]
            upper_2 = assignment_pair[RANGE_2_U]

            if ((lower_1 >= lower_2) and (lower_1 <= upper_2) or
                    (upper_1 >= lower_2) and (upper_1 <= upper_2) or
                    (lower_2 >= lower_1) and (lower_2 <= upper_1) or
                    (upper_2 >= lower_1) and (upper_2 <= upper_1)):
                cnt += 1

        return cnt
