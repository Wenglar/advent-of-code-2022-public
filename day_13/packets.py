import os

FILE = os.path.join(os.path.dirname(__file__), 'input.txt')

# inputs = [
#     '[1,1,3,1,1]',
#     '[1,1,5,1,1]',
#     '\n',
#     '[[1],[2,3,4]]',
#     '[[1],4]',
#     '\n',
#     '[9]',
#     '[[8,7,6]]',
#     '\n',
#     '[[4,4],4,4]',
#     '[[4,4],4,4,4]',
#     '\n',
#     '[7,7,7,7]',
#     '[7,7,7]',
#     '\n',
#     '[]',
#     '[3]',
#     '\n',
#     '[[[]]]',
#     '[[]]',
#     '\n',
#     '[1,[2,[3,[4,[5,6,7]]]],8,9]',
#     '[1,[2,[3,[4,[5,6,0]]]],8,9]',
# ]


pairs = []
left = True
pair = {'index': 1}
packets = []



with open(FILE, 'r') as f:
    line_raw = f.readline()
    # for line_raw in inputs:
    while line_raw:
        line = line_raw.replace('\n', '')
        if line:
            packet = eval(line)
            packets.append({'value': packet, 'src': line})

            if left:
                pair['L'] = packet
                left = False
            else:
                pair['R'] = packet
                pairs.append(pair)
        else:
            pair = {'index': pair['index'] + 1}
            left = True
        line_raw = f.readline()




def are_in_order(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return True
        elif left > right:
            return False
        else:
            return None
    elif isinstance(left, int):
        left = [left]
    elif isinstance(right, int):
        right = [right]

    l_size = len(left)
    r_size = len(right)
    compares = min([l_size, r_size])
    for i in range(compares):
        result = are_in_order(left[i], right[i])
        if result is not None:
            return result

    if l_size < r_size:
        return True
    elif l_size > r_size:
        return False
    else:
        return None

in_order = []
out_of_order = []

# part 1
for pair in pairs:
    if are_in_order(pair['L'], pair['R']):
        in_order.append(pair['index'])
    else:
        out_of_order.append(pair['index'])

print(f'Part one result: {sum(in_order)}')

# part 2
packets.insert(0, {'value': [[2]], 'src': '[[2]]'})
packets.insert(1, {'value': [[6]], 'src': '[[6]]'})

packet_cnt = len(packets)

for index in range(1, packet_cnt):
    L_index = index - 1
    R_index = index
    ok = are_in_order(packets[L_index]['value'], packets[R_index]['value'])

    while not ok:
        buffer = packets[L_index]
        packets[L_index] = packets[R_index]
        packets[R_index] = buffer
        if L_index != 0:
            L_index -= 1
            R_index -= 1
        ok = are_in_order(packets[L_index]['value'], packets[R_index]['value'])

two = None
six = None
for index, packet in enumerate(packets):
    if packet['src'] == '[[2]]':
        two = index + 1
    elif packet['src'] == '[[6]]':
        six = index + 1
    if two is not None and six is not None:
        break

print(f'Part two result: {two} * {six} = {two*six}')
