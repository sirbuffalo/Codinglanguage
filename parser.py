#!/usr/bin/python3

from math import ceil
from glob import glob
from re import *
import interpreter

class Parser:
    def __init__(self, codetext, indent='    '):
        self.codetext = codetext
        self.indent = indent
        self.parsed = None

    def parse(self):
        self.parsed = []
        spot = [self.parsed]
        last_indent = 0
        for line in self.codetext.split('\n'):
            indention = 0
            for _ in range(ceil(len(line) / len(self.indent)-1)):
                if line[indention * len(self.indent):(indention + 1) * len(self.indent)] != self.indent:
                    break
                indention += 1
            del spot[indention+1:]
            line = line[indention * len(self.indent):]
            if search("^[a-zA-Z][a-zA-Z0-9]* *=", line):
                spot[-1].append({
                    'type': 'set var',
                    'name':  findall("^[a-zA-Z][a-zA-Z0-9]* *=", line)[0][:-2].strip(),
                    'value': Parser.parse_expression(split("^[a-zA-Z][a-zA-Z0-9]* *=", line, 1)[1].strip())
                })
            elif search('^print\(.*\)$', line):
                spot[-1].append({
                    'type': 'print',
                    'value': Parser.parse_expression(line[6:-1])
                })
            elif search('for +[a-zA-Z][a-zA-Z0-9]* +of +', line):
                new_spot = []
                spot[-1].append({
                    'type': 'loop',
                    'var': sub('(^for +| +of +.+)', '', line),
                    'list': Parser.parse_expression(sub('for +[a-zA-Z][a-zA-Z0-9]* +of +', '', line, 1)),
                    'code': new_spot
                })
                spot.append(new_spot)
        return self.parsed

    @classmethod
    def parse_expression(cls, expression):
        expression = expression.strip()
        if expression[0] == '[' and expression[-1] == ']':
            return {
                'type': 'range',
                'start': cls.parse_expression(expression[1:expression.find('...')]),
                'end': cls.parse_expression(expression[expression.find('...') + 3:-1])
            }
        splited = []
        perrs = [splited]
        current = ''
        last_op = -5
        i = -1
        for i, char in enumerate(expression):
            if char == ' ':
                if current != '':
                    perrs[-1].append(current)
                    current = ''
                continue
            i += 1
            if char in ['*', '/', '+', '-'] and last_op + 1 < i and 1 < i:
                if current:
                    perrs[-1].append(current)
                perrs[-1].append(char)
                current = ''
                last_op = i
                continue
            if char == '(':
                if current:
                    perrs[-1].append(current)
                current = ''
                newperr = []
                perrs[-1].append(newperr)
                perrs.append(newperr)
                continue
            if char == ')':
                if current:
                    perrs[-1].append(current)
                current = ''
                perrs.pop()
                continue
            try:
                int(current + char)
            except ValueError:
                try:
                    perrs[-1].append(str(int(current)))
                    current = char
                    continue
                except ValueError:
                    pass
            except TypeError:
                pass
            try:
                float(current + char)
            except ValueError:
                try:
                    perrs[-1].append(str(float(current)))
                    current = char
                    continue
                except ValueError:
                    pass
            except TypeError:
                pass
            if search('^[a-zA-Z][a-zA-Z0-9]*$', current) and not search('^[a-zA-Z][a-zA-Z0-9]*$', current + char):
                perrs[-1].append(current)
                current = ''
            current += char
        if current != '':
            perrs[-1].append(current)
        return cls.equation_list_to_json(cls.add_extra_parentheses(splited))

    @classmethod
    def add_extra_parentheses(cls, equation_original):
        equation = equation_original.copy()
        ops = [i for i in range(len(equation)) if equation[i] in ['*', '/']]
        for i, index in enumerate(ops):
            if type(equation[index - i * 2 - 1]).__name__ == 'list':
                equation[index - i * 2 - 1] = cls.add_extra_parentheses(equation[index - i * 2 - 1])
            if type(equation[index - i * 2 + 1]).__name__ == 'list':
                equation[index - i * 2 + 1] = cls.add_extra_parentheses(equation[index - i * 2 + 1])
            equation[index - i * 2 - 1:index - i * 2 + 2] = [equation[index - i * 2 - 1:index - i * 2 + 2]]
        ops = [i for i in range(len(equation)) if equation[i] in ['+', '-']]
        for i, index in enumerate(ops):
            if type(equation[index - i * 2 - 1]).__name__ == 'list':
                equation[index - i * 2 - 1] = cls.add_extra_parentheses(equation[index - i * 2 - 1])
            if type(equation[index - i * 2 + 1]).__name__ == 'list':
                equation[index - i * 2 + 1] = cls.add_extra_parentheses(equation[index - i * 2 + 1])
            equation[index - i * 2 - 1:index - i * 2 + 2] = [equation[index - i * 2 - 1:index - i * 2 + 2]]
        return equation[0]

    @classmethod
    def equation_list_to_json(cls, equation_list):
        if type(equation_list).__name__ == 'str':
            return cls.parse_symbol(equation_list)
        operand = {
            '*': 'mul',
            '/': 'div',
            '+': 'add',
            '-': 'sub'
        }[equation_list[1]]
        return {
            'type': operand,
            'num1': cls.parse_symbol(equation_list[0]),
            'num2': cls.parse_symbol(equation_list[2])
        }

    @classmethod
    def parse_symbol(cls, symbol):
        symbol_type = type(symbol).__name__
        if symbol_type == 'list':
            return cls.equation_list_to_json(symbol)
        elif symbol_type == 'str':
            try:
                return {
                    'type': 'int',
                    'value': int(symbol)
                }
            except ValueError:
                try:
                    return {
                        'type': 'float',
                        'value': float(symbol)
                    }
                except ValueError:
                    if search('^[a-zA-Z][a-zA-Z0-9]*$', symbol):
                        return {
                            'type': 'get var',
                            'name': symbol
                        }
                    else:
                        print('?')

files = glob('*.🐮🦬')
files.extend(glob('*.🦬🐮'))
files.extend(glob('*.🔥🦬'))
files.extend(glob('*.cb'))
files.extend(glob('*.fb'))
for file in files:
    print(Parser(open(file).read()).parse())
    interp = interpreter.Interpreter(Parser(open(file).read()).parse())
    interp.run()
