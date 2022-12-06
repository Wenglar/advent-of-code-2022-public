import os
import copy


FILE = os.path.join(os.path.dirname(__file__), 'input.txt')

packet_start = None
message_start = None

with open(FILE, 'r') as f:
    line = f.readline().strip('\n')
    length = len(line)
    for i in range(4, length+1):
        if len(set(line[i-4:i])) == 4:
            packet_start = i
            break
    for i in range(14, length+1):
        if len(set(line[i-14:i])) == 14:
            message_start = i
            break

print(f'Length: {length}')
print(f'Packet start: {packet_start}')
print(f'Message start: {message_start}')
