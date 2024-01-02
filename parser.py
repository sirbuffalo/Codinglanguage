#!/usr/bin/python3

from math import ceil
from glob import glob
from re import search, split, findall
import interpreter

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
        expression = expression.strip()
        splited = []
        perrs = [splited]
        current = ''
        lasttype = None
        for char in expression:
            if char == ' ':
                if current != '':
                    perrs[-1].append(current)
                    current = ''
                continue
            if char in ['*', '/', '+', '-'] and lasttype != 'op':
                if current:
                    perrs[-1].append(current)
                perrs[-1].append(char)
                current = ''
                lasttype = 'op'
                continue
            if char == '(':
                if current:
                    perrs[-1].append(current)
                current = ''
                newperr = []
                perrs[-1].append(newperr)
                perrs.append(newperr)
                lasttype = 'openperr'
                continue
            if char == ')':
                if current:
                    perrs[-1].append(current)
                current = ''
                perrs.pop()
                lasttype = 'closeperr'
                continue
            try:
                int(current + char)
            except ValueError:
                try:
                    perrs[-1].append(str(int(current)))
                    current = char
                    lasttype = 'int'
                    continue
                except ValueError:
                    pass
            try:
                float(current + char)
            except ValueError:
                try:
                    perrs[-1].append(str(float(current)))
                    current = ''
                    lasttype = 'float'
                    continue
                except ValueError:
                    pass
            if search('^[a-zA-Z][a-zA-Z0-9]*$', current) and not search('^[a-zA-Z][a-zA-Z0-9]*$', current + char):
                print(current, char)
                perrs[-1].append(current)
                current = ''
                lasttype = 'var'
            current += char
        if current != '':
            perrs[-1].append(current)
        # ops = [i for i in range(len(splited)) if splited[i] in ['*', '/']]
        # for i, index in enumerate(ops):
        #     splited[index - i * 2 - 1:index - i * 2 + 1] = [[index - i * 2 - 1:index - i * 2 + 1]]
        return splited


files = glob('*.🐮🦬')
files.extend(glob('*.🦬🐮'))
files.extend(glob('*.🔥🦬'))
files.extend(glob('*.cb'))
files.extend(glob('*.fb'))
for file in files:
    print(Parser(open(file).read()).parse())
    # interp = interpreter.Interpreter(Parser(open(file).read()).parse())
    # interp.run()
