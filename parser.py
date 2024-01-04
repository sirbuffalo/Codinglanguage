#!/usr/bin/python3

from math import ceil
from glob import glob
from re import *
import interpreter

def error(text):
    print('\033[91m' + text)
    exit(1)

class Var:
    def __init__(self, name):
        if not Var.vaild(name):
            error(f'{name} is not a valid variable name')
        self.name = name

    def __dict__(self):
        return {
            'type': 'get var',
            'name': self.name
        }

    @staticmethod
    def valid(value):
        return bool(search('^[a-zA-Z][a-zA-Z0-9]*$', value))


class Int:
    def __init__(self, value):
        if not Int.valid(value):
            error(f'{value} is not a valid int')
        self.value = int(value)

    def __dict__(self):
        return {
            'type': 'int',
            'value': self.value
        }

    @staticmethod
    def valid(value):
        try:
            int(value)
            return True
        except ValueError:
            return False
        except TypeError:
            return False


class Float:
    def __init__(self, value):
        if not Float.valid(value):
            error(f'{value} is not a valid float')
        self.value = float(value)

    def __dict__(self):
        return {
            'type': 'float',
            'value': self.value
        }

    @staticmethod
    def valid(value):
        try:
            float(value)
            return True
        except ValueError:
            return False
        except TypeError:
            return False


class Operation:
    operators = {
        '*':{
                'name': 'mul',
                'types': [Int.valid, Float.valid, Var.valid]
            },
        '/': {
                'name': 'div',
                'types': [Int.valid, Float.valid, Var.valid]
            },
        '+': {
                'name': 'add',
                'types': [Int.valid, Float.valid, Var.valid]
            },
        '-': {
                'name': 'sub',
                'types': [Int.valid, Float.valid, Var.valid]
            },
        '=': {
            'name': 'set var',
            'type1': Var.valid,
            'type2': [Int.valid, Float.valid, Var.valid]
        },
        '==': {
            'name': 'equal',
            'types': [Int.valid, Float.valid, Var.valid]
        }
    }

    def __init__(self, operation, *values):
        self.operation = operation
        self.values = values

    def __dict__(self):
        ans = {
            'type': Operation.operators[self.operation]['name']
        }
        if len(self.values) == 1:
            ans['value'] = self.values[0]
        else:
            for i in range(len(self.values)):
                ans['value'+str(i+1)] = self.values[i]

    @staticmethod
    def valid(operator, value1, value2):
        data = Operation.operators[operator]
        if 'types' in data:
            for value in (value1, value2):
                for validate in data['types']:
                    if validate(value):
                        break
                else:
                    return False
        elif 'type' in data:
            return data['type'](value1) and data['type'](value2)
        elif 'type1' in data:
            if not data['type'](value1):
                return False
            if 'type2' in data:
                return data['type'](value2)
            elif 'types2' in data:
                for validate in data['types2']:
                    if validate(value2):
                        break
                else:
                    return False
        elif 'types1' in data:
            for validate in data['types']:
                if validate(value1):
                    break
            else:
                return False
            if 'type2' in data:
                return data['type'](value2)
            elif 'types2' in data:
                for validate in data['types2']:
                    if validate(value2):
                        break
                else:
                    return False
        return True

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
        if len(equation) == 1 and type(equation[0]).__name__ == 'list':
            return cls.add_extra_parentheses(equation[0])
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
        # print(equation_list, len(equation_list))
        operand = {
            '*': 'mul',
            '/': 'div',
            '+': 'add',
            '-': 'sub'
        }[equation_list[1]]
        return {
            'type': operand,
            'value1': cls.parse_symbol(equation_list[0]),
            'value2': cls.parse_symbol(equation_list[2])
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
