import os

from robot.api.logger import info, debug, trace, console  # type:ignore


ORD_A_L = ord('a')
ORD_Z_L = ord('z')
ORD_A_U = ord('A')
ORD_Z_U = ord('Z')


class RucksackLibrary():
    """
    Library for Rucksack payload duplicate finding, evaluation and summing.
    """

    ROBOT_LIBRARY_SCOPE = 'TEST'

    def __init__(self):
        self.rucksacks = []
        self.duplicates = []

    def load_file(self, file_path):
        assert isinstance(file_path, str), f'Unexpected type: {type(file_path)}'
        assert os.path.exists(file_path)

        with open(file_path, 'r') as f:
            line = f.readline()

            while line:
                rucksack = line.strip('\n')
                self.rucksacks.append(rucksack)
                line = f.readline()

    def validate_rucksacks(self):
        for rucksack in self.rucksacks:
            size = len(rucksack)
            if size % 2 != 0:
                raise ValueError(
                    f'Rucksack should have even number of events. '
                    f'Rucksack containing "{rucksack}" has length {size}.'
                )

        rucksack_cnt = len(self.rucksacks)
        if rucksack_cnt % 3 != 0:
            raise ValueError(
                f'Rucksack count shall be integer multiple of 3. '
                f'Total rucksacks "{rucksack_cnt}".'
            )

    def get_compartment_duplicates(self):
        for rucksack in self.rucksacks:
            split = len(rucksack) // 2
            compartment1 = rucksack[:split]
            compartment2 = rucksack[split:]
            found = False
            for char1 in compartment1:
                for char2 in compartment2:
                    if char1 == char2:
                        self.duplicates.append(char1)
                        found = True
                        break
                if found:
                    break

    def get_triplet_duplicates(self):
        rucksack_cnt = len(self.rucksacks)
        for group in range(rucksack_cnt // 3):
            duplicate = self._get_duplicate_from_triplet(self.rucksacks[3*group:3*group+3])
            self.duplicates.append(duplicate)

    def _get_duplicate_from_triplet(self, triplet):
        assert len(triplet) == 3

        for char1 in triplet[0]:
            for char2 in triplet[1]:
                for char3 in triplet[2]:
                    if char1 == char2 and char1 == char3:
                        return char1

        raise AssertionError(
            f'No duplicate found in triplet: "{triplet[0]}", "{triplet[1]}", "{triplet[2]}".'
        )

    def evaluate_duplicates(self):
        for index, item in enumerate(self.duplicates):
            item_ord = ord(item)
            if item_ord in range(ORD_A_L, ORD_Z_L+1):
                self.duplicates[index] = item_ord - ORD_A_L + 1
            elif item_ord in range(ORD_A_U, ORD_Z_U+1):
                self.duplicates[index] = item_ord - ORD_A_U + 27
            else:
                raise ValueError(
                    f'Duplicates should be letters (a-z;A-Z). '
                    f'Got "{item}".'
                )

    def validate_duplicate_values(self):
        for duplicate in self.duplicates:
            if not isinstance(duplicate, int):
                raise ValueError(
                    f'Duplicates should be integer. '
                    f'Found "{type(duplicate)}".'
                )

    def sum_duplicates(self):
        return sum(self.duplicates)
