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
        'operator': match[2]
    }

resolved = {}
for match in matches_r:
    resolved[match[0]] = int(match[1])

print(not_resolved)
print(resolved)

while 'root' not in resolved:
    for key, content in not_resolved.items():
        operands = set(content['operands'])
        resolved_keys = set(resolved.keys())
        if operands.issubset(resolved_keys):
            val = None
            operand_0 = resolved[content['operands'][0]]
            operand_1 = resolved[content['operands'][1]]
            if content['operator'] == '+':
                val = operand_0 + operand_1
            elif content['operator'] == '-':
                val = operand_0 - operand_1
            elif content['operator'] == '*':
                val = int(operand_0 * operand_1)
            elif content['operator'] == '/':
                val = int(round(operand_0 / operand_1))
            resolved[key] = val
            break
    not_resolved.pop(key)

print(resolved['root'])
