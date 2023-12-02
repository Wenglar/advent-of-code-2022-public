import os

order = ('-', '+', 'L', 'I', 'o')

# x == 0: wall -> first column is 1
#   spawning 2 cols from wall -> in column 3
# y == 0: floor -> first row is 1
#   spawning 3 rows from top -> in row 4 if last top point is 0

# found experimentally that for my input:
# 1736 : 1736 : 2738 : 2738
# 3456 : 1720 : 2704 : 5442
# first rock where "+" uses first direction symbol is 1736th rock
# the height at this moment is 2738
# every other occurence is 1720 rock away and gives + 2704 height

# for dummy input it was:
# 36 : 36 : 61 : 61
# 71 : 35 : 53 : 114

shapes = {
    '-': [[3, 4], [4, 4], [5, 4], [6, 4]],
    '+': [[4, 4], [3, 5], [4, 5], [5, 5], [4, 6]],
    'L': [[3, 4], [4, 4], [5, 4], [5, 5], [5, 6]],
    'I': [[3, 4], [3, 5], [3, 6], [3, 7]],
    'o': [[3, 4], [4, 4], [3, 5], [4, 5]]
}

FILE = os.path.join(os.path.dirname(__file__), 'input.txt')

with open(FILE, 'r') as f:
    raw = f.read()
    inputs = ''.join(c for c in raw if c != '\n')
inputs = r'>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'

L_WALL = 0
R_WALL = 8

input_cnt = len(inputs)

index = -1

occupied = set()
for i in range(1, 8):
    occupied.add((i, 0))

# ROCKS = 2022
ROCKS = 1000000000000
rocks = 0
rock = shapes[order[rocks]]

highest_point = 0

current_shape = order[rocks]
last_shape = order[rocks]
last_highest = 0
last_rocks = 0

while rocks < ROCKS:
    # get jet direction
    index = (index + 1) % input_cnt
    dir_raw = inputs[index]
    if dir_raw not in (r'<', r'>'):
        print(f'error: "{bytes(dir_raw, encoding="utf-8")}"')
    if index == 0 and current_shape == order[1]:
        print(rocks, ':', rocks-last_rocks, ':', highest_point-last_highest, ':', highest_point)
        last_highest = highest_point
        last_rocks = rocks
    direction = -1 if dir_raw == r'<' else 1

    # attempt movement sideways
    moved_rock = []
    for point in rock:
        new_x = point[0] + direction
        y = point[1]
        if new_x not in (L_WALL, R_WALL) and (new_x, y) not in occupied:
            moved_rock.append([new_x, y])
        else:
            # if one point cannot move, the whole rock cannot move
            moved_rock = rock
            break

    # attempt movement down
    rock = moved_rock
    moved_rock = []
    moved = True

    for point in rock:
        x = point[0]
        new_y = point[1] - 1
        if (x, new_y) not in occupied:
            moved_rock.append([x, new_y])
        else:
            # if one point cannot move, none can
            moved = False
            break

    if moved:
        # if movement successful, continue
        rock = moved_rock
    else:
        # if movement not successful, make it static and spawn new rock
        # - make rock static
        for point in rock:
            occupied.add(tuple(point))
            if point[1] > highest_point:
                highest_point = point[1]
        # - spawn new rock
        rocks += 1
        # if rocks % 100000 == 0:
        #     print(rocks, ':', highest_point-last_highest, ':', highest_point)
        #     last_highest = highest_point
        current_shape = order[rocks%len(order)]
        new_rock = shapes[order[rocks%len(order)]]

        rock = []
        for point in new_rock:
            x = point[0]
            y = point[1] + highest_point
            rock.append([x, y])


print(highest_point)
