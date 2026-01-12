import re


def decode_sequence(encoded):
    result = ""
    i = 0
    while i < len(encoded):
        if encoded[i].isdigit():
            result += encoded[i + 1] * int(encoded[i])
            i += 1
        else:
            result += encoded[i]
        i += 1
    return result


def get_data(filename):
    items = []
    with open(filename, 'r', encoding='utf-8') as file:
        for row in file:
            cols = row.strip().split('\t')
            items.append((
                cols[0].strip(),
                cols[1].strip(),
                decode_sequence(cols[2].strip())
            ))
    return items


def get_tasks(filename):
    tasks = []
    with open(filename, 'r', encoding='utf-8') as file:
        for row in file:
            parts = row.strip().split('\t')
            cmd = parts[0].strip()
            if cmd == 'search' or cmd == 'mode':
                tasks.append((cmd, parts[1].strip()))
            else:
                tasks.append((cmd, parts[1].strip(), parts[2].strip()))
    return tasks


def find_sequence(data, pattern):
    target = decode_sequence(pattern)
    for item in data:
        if target in item[2]:
            return f'{item[1]}\t{item[0]}'
    return 'NOT FOUND'


def calc_difference(data, name1, name2):
    seq1 = seq2 = None
    for item in data:
        if item[0] == name1:
            seq1 = item[2]
        elif item[0] == name2:
            seq2 = item[2]

    if seq1 is None and seq2 is None:
        return f"MISSING: {name1}, {name2}"
    elif seq1 is None:
        return f"MISSING: {name1}"
    elif seq2 is None:
        return f"MISSING: {name2}"

    min_len = min(len(seq1), len(seq2))
    diff_count = 0

    for i in range(min_len):
        if seq1[i] != seq2[i]:
            diff_count += 1

    return str(diff_count + abs(len(seq1) - len(seq2)))


def find_most_common(data, protein_name):
    for item in data:
        if item[0] == protein_name:
            sequence = item[2]
            counts = {}
            for char in sequence:
                counts[char] = counts.get(char, 0) + 1

            max_val = max(counts.values())
            for key in sorted(counts):
                if counts[key] == max_val:
                    return key, max_val
    return 'MISSING'


# Основная часть
data = get_data('sequences.0.txt')
tasks = get_tasks('commands.0.txt')

output_file = open('analysis_result.txt', 'w', encoding='utf-8')
output_file.write('Analysis Report\n')

for idx, task in enumerate(tasks, 1):
    cmd_type = task[0]

    if cmd_type == 'search':
        res = find_sequence(data, task[1])
        output_file.write(f'{idx:03d}   search   {decode_sequence(task[1])}\n{res}\n')

    elif cmd_type == 'diff':
        res = calc_difference(data, task[1], task[2])
        output_file.write(f'{idx:03d}   diff   {task[1]}   {task[2]}\n{res}\n')

    elif cmd_type == 'mode':
        res = find_most_common(data, task[1])
        if res != 'MISSING':
            output_file.write(f'{idx:03d}   mode   {task[1]}\n{res[0]}\t{res[1]}\n')
        else:
            output_file.write(f'{idx:03d}   mode   {task[1]}\n{res}\n')

output_file.close()
print("Программа завершена. Результат сохранен в analysis_result.txt")
