def name(line):
    line = line.upper().split()
    st = ''
    for word in line:
        if len(word) > 2:
            st += word[0]
    return st

txt = input('Введите текст: ')
print(name(txt))