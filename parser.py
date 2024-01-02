from math import ceil
from glob import glob
from re import search, split, findall

class Parser:
    def __init__(self, codetext, indent='    '):
        self.codetext = codetext
        self.indent = indent
        self.parsed = None

    def parse(self):
        self.parsed = []
        for line in self.codetext.split('\n'):
            indention = 0
            for _ in range(ceil(len(line) / len(self.indent)-1)):
                if line[indention * len(self.indent):(indention + 1) * len(self.indent)] != self.indent:
                    break
                indention += 1
            line = line[indention * len(self.indent):]
            if search("^[a-zA-Z][a-zA-Z0-9]* *=", line):
                self.parsed.append({
                    'type': 'set var',
                    'name':  findall("^[a-zA-Z][a-zA-Z0-9]* *=", line)[0][:-2].strip(),
                    'value': Parser.parse_expression(split("^[a-zA-Z][a-zA-Z0-9]* *=", line, 1)[1].strip())
                })
        return self.parsed

    @classmethod
    def parse_expression(cls, expression):
        current = ""
        num_par = 0
        new_expression = ""
        replaces = []
        for char in expression:
            if char == '(':
                num_par += 1
                continue
            if char == ')':
                num_par -= 1
                if num_par == 0:
                    new_expression += f'|:{len(replaces)}:|'
                    replaces.append(cls.parse_expression(current))
                    current = ""
                continue
            if 0 < num_par:
                current += char
                continue
            new_expression += char
        expression = new_expression
        new_expression = ""
        operator = None
        num1 = ""
        current = ""
        for char in expression:
            if char in ['*', '/', '+', '-']:
                if operator:
                    new_expression += f'|:{len(replaces)}:|'
                    replaces.append({
                        'type': operator,
                        'num1': cls.parse_expression(num1),
                        'num2': cls.parse_expression(current)
                    })
                num1 = current
                current = ''
            if

        return None

files = glob('*.🐮🦬')
files.extend(glob('*.🦬🐮'))
files.extend(glob('*.🔥🦬'))
files.extend(glob('*.cb'))
files.extend(glob('*.fb'))
for file in files:
    print(Parser(open(file).read()).parse())
