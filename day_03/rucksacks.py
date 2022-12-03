import os


FILE = os.path.join(os.path.dirname(__file__), 'input.txt')

ORD_A_L = ord('a')
ORD_Z_L = ord('z')
ORD_A_U = ord('A')
ORD_Z_U = ord('Z')

def get_priority(item):
    output = 0
    item_nr = ord(item)

    if item_nr in range(ORD_A_L, ORD_Z_L+1):
        output = item_nr - ORD_A_L + 1
    elif item_nr in range(ORD_A_U, ORD_Z_U+1):
        output = item_nr - ORD_A_U + 27
    else:
        raise ValueError(f'Unexpected value {item} resulting in ordinal {item_nr}.')

    return output

def get_duplicate(rucksack):
    assert isinstance(rucksack, str)
    size = len(rucksack)
    assert size % 2 == 0

    compartment1 = rucksack[0:size//2]
    compartment2 = rucksack[size//2:]

    output = None

    for char1 in compartment1:
        for char2 in compartment2:
            if char1 == char2:
                output = char1
                break

    return output

def get_duplicate_in_three(rucksacks):
    assert isinstance(rucksacks, (list, tuple))
    assert len(rucksacks) == 3
    (rucksack1, rucksack2, rucksack3) = tuple(rucksacks)
    assert isinstance(rucksack1, str)
    assert isinstance(rucksack2, str)
    assert isinstance(rucksack3, str)

    output = None

    for char1 in rucksack1:
        for char2 in rucksack2:
            for char3 in rucksack3:
                if char1 == char2 and char2 == char3:
                    output = char1

    return output

total = 0

with open(FILE, 'r') as f:
    line = f.readline()
    while line:
        line = line.replace('\n', '')
        duplicate = get_duplicate(line)
        priority = get_priority(duplicate)
        total += priority
        line = f.readline()

print(f"Sum of priorities: {total}")


total = 0

with open(FILE, 'r') as f:
    lines = []
    line = f.readline()
    while line:
        lines.append(line.replace('\n', ''))
        if len(lines) == 3:
            duplicate = get_duplicate_in_three(lines)
            priority = get_priority(duplicate)
            total += priority
            lines = []
        line = f.readline()

print(f"Sum of priorities: {total}")
