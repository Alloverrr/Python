import re

txt = 'He jests at scars. That never felt a wound!   Hello, friend!   Are you OK?'
parts = re.split(r'(?<=[.?!]) +', txt)

def print_sent(items):
    for item in items:
        print(item)

print_sent(parts)
print(f'Предложений в тексте: {len(parts)}')