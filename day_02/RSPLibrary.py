import os

POINTS = {
    'X': {
        'A': 1 + 3,
        'B': 1 + 0,
        'C': 1 + 6,
    },
    'Y': {
        'A': 2 + 6,
        'B': 2 + 3,
        'C': 2 + 0,
    },
    'Z': {
        'A': 3 + 0,
        'B': 3 + 6,
        'C': 3 + 3,
    },
}

STRATEGY = {
    'A': {
        'X': 'Z',
        'Y': 'X',
        'Z': 'Y',
    },
    'B': {
        'X': 'X',
        'Y': 'Y',
        'Z': 'Z',
    },
    'C': {
        'X': 'Y',
        'Y': 'Z',
        'Z': 'X',
    },
}

class RSPLibrary():
    """
    Library for Rock, Paper, Scissors support
    """
    ROBOT_LIBRARY_SCOPE = 'TEST'

    def __init__(self):
        self.events = []

    def load_file(self, file_path):
        assert isinstance(file_path, str), f'Unexpected type: {type(file_path)}'
        assert os.path.exists(file_path)

        with open(file_path, 'r') as f:
            line = f.readline()
            self.events = []

            while line:
                event = {
                    'me': line[2],
                    'enemy': line[0]
                }
                self.events.append(event)
                line = f.readline()

    def get_events(self):
        return self.events

    def get_points(self, input_enemy, input_me):
        # Commented out for performance reasons

        # assert isinstance(input_enemy, str)
        # assert isinstance(input_me, str)
        # assert input_enemy in ('A', 'B', 'C')
        # assert input_me in ('X', 'Y', 'Z')

        # return POINTS[input_me][input_enemy]

        raise NotImplementedError()

    def get_strategic_event(self, input_enemy, strategy):
        # Commented out for performance reasons

        # assert isinstance(input_enemy, str)
        # assert isinstance(strategy, str)
        # assert input_enemy in ('A', 'B', 'C')
        # assert strategy in ('X', 'Y', 'Z')

        # return STRATEGY[input_enemy][strategy]

        raise NotImplementedError()

    def calculate_points_from_events_and_sum_them(self):
        points = 0
        for event in self.events:
            points += POINTS[event['me']][event['enemy']]

        return points

    def evaluate_actions_based_on_strategy(self):
        for index, strategy in enumerate(self.events):
            self.events[index]['me'] = STRATEGY[strategy['enemy']][strategy['me']]
