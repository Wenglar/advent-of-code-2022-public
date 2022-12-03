from robot.api.logger import info, debug, trace, console  # type:ignore


class CustomLibrary:
    '''
    This is a user written keyword library.
    '''

    ROBOT_LIBRARY_SCOPE = 'SUITE'

    def __init__(self) -> None:
        self.file_path = ''
        self.elves: list = []

    def load_and_process_file(self, file_path):
        self.elves = []

        with open(file_path, 'r') as f:
            line = f.readline()
            self.elves.append(0)
            while line:
                nr_str = line.replace('\n', '')
                if nr_str != '':
                    self.elves[-1] += int(nr_str, 10)
                else:
                    self.elves.append(0)
                line = f.readline()

    def sort_values(self):
        self.elves = sorted(self.elves)

    def get_last_n_values(self, n):
        return self.elves[-n:]

    def get_maximum_value(self):
        return max(self.elves)
