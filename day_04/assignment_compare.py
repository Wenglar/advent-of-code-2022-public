import os


FILE = os.path.join(os.path.dirname(__file__), 'input.txt')

fully_contained = 0
overlaps = 0
with open(FILE, 'r') as f:
    line = f.readline()
    while line:
        sections = line.replace('\n', '').split(',')
        section1_raw = sections[0].split('-')
        section2_raw = sections[1].split('-')
        section1 = (int(section1_raw[0]), int(section1_raw[1]))
        section2 = (int(section2_raw[0]), int(section2_raw[1]))
        # one is fully contained by the other
        if ((section1[0] >= section2[0] and section1[1] <= section2[1]) or
                section2[0] >= section1[0] and section2[1] <= section1[1]):
            fully_contained += 1
        # there is an overlap
        if ((section1[0] >= section2[0] and section1[0] <= section2[1]) or
                (section1[1] >= section2[0] and section1[1] <= section2[1]) or
                (section2[0] >= section1[0] and section2[0] <= section1[1]) or
                (section2[1] >= section1[0] and section2[1] <= section1[1])):
            overlaps += 1
        line = f.readline()

print(f'Fully contained: {fully_contained}')
print(f'Overlaps: {overlaps}')
