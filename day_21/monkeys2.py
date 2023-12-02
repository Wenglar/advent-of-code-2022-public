from decimal import ROUND_05UP
import os
import re

dummy = (
    'root: pppw + sjmn\n'
    'dbpl: 5\n'
    'cczh: sllz + lgvd\n'
    'zczc: 2\n'
    'ptdq: humn - dvpt\n'
    'dvpt: 3\n'
    'lfqf: 4\n'
    'humn: 5\n'
    'ljgn: 2\n'
    'sjmn: drzm * dbpl\n'
    'sllz: 4\n'
    'pppw: cczh / lfqf\n'
    'lgvd: ljgn * ptdq\n'
    'drzm: hmdt - zczc\n'
    'hmdt: 32\n'
)

FILE = os.path.join(os.path.dirname(__file__), 'input.txt')

pattern_not_resolved = re.compile(r'(\S+): (\S+) ([+\-\*\/]) (\S+)')
pattern_resolved = re.compile(r'(\S+): (\d+)')

with open(FILE, 'r') as f:
    file_raw = f.read()

matches_n = pattern_not_resolved.findall(file_raw)
matches_r = pattern_resolved.findall(file_raw)
# matches_n = pattern_not_resolved.findall(dummy)
# matches_r = pattern_resolved.findall(dummy)

not_resolved = {}
for match in matches_n:
    not_resolved[match[0]] = {
        'operands': [match[1], match[3]],
        'operator': match[2],
        'resolved': False
    }

resolved = {}
for match in matches_r:
    if match[0] == 'humn':
        continue    # that is me
    resolved[match[0]] = int(match[1])

# print(not_resolved)
# print(resolved)

print('starting loop 1')

root_op_0 = not_resolved['root']['operands'][0]
root_op_1 = not_resolved['root']['operands'][1]

while not isinstance(root_op_0, int) and not isinstance(root_op_1, int):
    for key, content in not_resolved.items():
        operands = set(content['operands'])
        resolved_keys = set(resolved.keys())
        if root_op_0 in resolved:
            root_op_0 = resolved[root_op_0]
        if root_op_1 in resolved:
            root_op_1 = resolved[root_op_1]
        if operands.issubset(resolved_keys):
            if 'humn' in operands:
                continue    # this has to be found
            val = None
            operand_0 = resolved[content['operands'][0]]
            operand_1 = resolved[content['operands'][1]]
            if key != 'root':
                if content['operator'] == '+':
                    val = operand_0 + operand_1
                elif content['operator'] == '-':
                    val = operand_0 - operand_1
                elif content['operator'] == '*':
                    val = operand_0 * operand_1
                elif content['operator'] == '/':
                    val = int(round(operand_0 / operand_1))
                resolved[key] = val
                not_resolved.pop(key)
            break

print(not_resolved['root'], root_op_0, root_op_1)
if isinstance(root_op_0, int):
    resolved[root_op_1] = root_op_0
else:
    resolved[root_op_0] = root_op_1
not_resolved['root']['resolved'] = True


print('starting loop 2')

while 'humn' not in resolved:
    for key, content in not_resolved.items():
        if not content['resolved'] and key in resolved:
            op_0 = content['operands'][0]
            op_1 = content['operands'][1]
            # print(key, content)
            if op_0 in resolved:
                op_0 = resolved[op_0]
                val = resolved[key]
                result = 0
                if content['operator'] == '+':
                    result = val - op_0
                elif content['operator'] == '-':
                    result = op_0 - val
                elif content['operator'] == '*':
                    result = int(round(val / op_0))
                elif content['operator'] == '/':
                    result = int(round(op_0 / val))
                resolved[op_1] = result
                # print('op0', op_0, op_1, result)
                not_resolved[key]['resolved'] = True
            elif op_1 in resolved:
                op_1 = resolved[op_1]
                val = resolved[key]
                result = 0
                if content['operator'] == '+':
                    result = val - op_1
                elif content['operator'] == '-':
                    result = val + op_1
                elif content['operator'] == '*':
                    result = int(round(val / op_1))
                elif content['operator'] == '/':
                    result = val * op_1
                resolved[op_0] = result
                # print('op1', op_1, op_0, result)
                not_resolved[key]['resolved'] = True

print('humn:', resolved['humn'])
