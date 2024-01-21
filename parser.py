#!/usr/bin/python3

from math import ceil
from glob import glob
from re import *
import interpreter
import shutil

def get_indexes(l, *args):
    return [i for i, e in enumerate(l) if e in args]

def error(text):
    spaces = ' ' * (shutil.get_terminal_size().columns - len(text) - len(file) - len(str(line_num)) - 10)
    print(f'\033[38;5;52m\033[48;5;9m▲ Error: {text}{spaces}{file}\033[38;5;255m:\033[38;5;52m{line_num}\033[0m')
    exit(1)


def add_extra_perrs(splitted):
    if type(splitted).__name__ == 'str':
        return splitted
    if len(splitted) == 3:
        return splitted
    for i in get_indexes(splitted, '*', '/'):
        add_extra_perrs(splitted[i - 1])
        add_extra_perrs(splitted[i + 1])
        splitted[i - 1:i + 2] = [[splitted[i - 1:i + 2]]]
    for i in get_indexes(splitted, '+', '-'):
        add_extra_perrs(splitted[i - 1])
        add_extra_perrs(splitted[i + 1])
        splitted[i - 1:i + 2] = [[splitted[i - 1:i + 2]]]

def classify(splitted):
    if type(splitted).__name__ == 'str':
        for data_type in Expression.data_types:
            if data_type.valid(splitted):
                return data_type(splitted)
    if len(splitted) == 1:
        return classify(splitted[0])
    if len(splitted) != 3:
        raise Exception("len(splitted) != 3")
    return Operation(splitted[1], classify(splitted[0]), classify(splitted[2]))


class Var:
    def __init__(self, name):
        if not Var.valid(name):
            error(f'{name} is not a valid variable name')
        self.value = name

    def to_dict(self):
        return {
            'type': 'get var',
            'name': self.value
        }

    @staticmethod
    def valid(value):
        return bool(search('^[a-zA-Z][a-zA-Z0-9]*$', value))


class Int:
    def __init__(self, value):
        if not Int.valid(value):
            error(f'{value} is not a valid int')
        self.value = int(value)

    def to_dict(self):
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

    def to_dict(self):
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

class Range:
    def __init__(self, value):
        if not Range.valid(value):
            error(f'{value} is not a valid Range')
        brackets = 0
        for i, char in enumerate(value[1:-1]):
            if char == '[':
                brackets += 1
            elif char == ']':
                brackets -= 1
            elif brackets == 0 and value[i:i + 3] == '...':
                self.start = value[1:i]
                self.end = value[i + 3:-1]

    def to_dict(self):
        return {
            'type': 'range',
            'start': Expression(self.start).to_dict(),
            'end': Expression(self.end).to_dict()
        }

    @staticmethod
    def valid(value):
        if value[0] != '[':
            return False
        if value[-1] != ']':
            return False
        if '...' not in value[1:-1]:
            return False
        brackets = 0
        for i, char in enumerate(value[1:-1]):
            if char == '[':
                brackets += 1
            elif char == ']':
                brackets -= 1
            elif brackets == 0 and value[i:i + 3] == '...':
                return True
        else:
            return False


class Operation:
    pemdas = [
        ['*', '/'],
        ['+', '-']
    ]
    operators = {
        '*': {
                'name': 'mul',
                'types': [Int, Float, Var]
            },
        '/': {
                'name': 'div',
                'types': [Int, Float, Var]
            },
        '+': {
                'name': 'add',
                'types': [Int, Float, Var]
            },
        '-': {
                'name': 'sub',
                'types': [Int, Float, Var]
            },
        '=': {
            'name': 'set var',
            'type1': Var,
            'types2': [Int, Float, Var],
            'name1': 'name',
            'name2': 'value',
            'prop1': ['name']
        }
    }

    def __init__(self, operation, value1, value2):
        self.operation = operation
        self.value1 = value1
        self.value2 = value2

    def to_dict(self):
        name1 = 'value1'
        name2 = 'value2'
        prop1 = []
        prop2 = []
        if 'name1' in Operation.operators[self.operation]:
            name1 = Operation.operators[self.operation]['name1']
        if 'name2' in Operation.operators[self.operation]:
            name2 = Operation.operators[self.operation]['name2']
        ans = {
            'type': Operation.operators[self.operation]['name'],
            name1: self.value1.to_dict(),
            name2: self.value2.to_dict()
        }
        if 'prop1' in Operation.operators[self.operation]:
            prop1 = Operation.operators[self.operation]['prop1']
        if 'prop2' in Operation.operators[self.operation]:
            prop2 = Operation.operators[self.operation]['prop2']
        for prop in prop1:
            ans[name1] = ans[name1][prop]
        for prop in prop2:
            ans[name2] = ans[name2][prop]
        return ans

    @staticmethod
    def valid(operator, value1, value2):
        data = Operation.operators[operator]
        if 'types' in data:
            for data_type in data['types']:
                if isinstance(value1, data_type):
                    break
            else:
                return False
            for data_type in data['types']:
                if isinstance(value2, data_type):
                    break
            else:
                return False
        if 'type' in data:
            return isinstance(value1, data['type']) and isinstance(value2, data['type'])
        if 'type1' in data:
            if not isinstance(value1, data['type1']):
                return False
        if 'type2' in data:
            if not isinstance(value2, data['type2']):
                return False
        if 'types1' in data:
            for data_type in data['types1']:
                if isinstance(value1, data_type):
                    break
            else:
                return False
        if 'types2' in data:
            for data_type in data['types2']:
                if isinstance(value2, data_type):
                    break
            else:
                return False
        return True

class Expression:
    data_types = [
        Int,
        Float,
        Range,
        Var
    ]

    def __init__(self, text):
        self.expression = text.strip()

    def to_list(self):
        splitted = []
        start = 0
        while True:
            if start == len(self.expression.strip()):
                break
            if self.expression[start] == '(':
                perr = 0
                for i in range(start, len(self.expression)):
                    if self.expression[i] == '(':
                        perr += 1
                    elif self.expression[i] == ')':
                        perr -= 1
                    if perr == 0:
                        splitted.append(Expression(self.expression[start + 1:i]).to_list())
                        start = i + 1
                        break
            if start == len(self.expression.strip()):
                break
            for end in range(len(self.expression), 0, -1):
                for data_type in Expression.data_types:
                    if data_type.valid(self.expression[start:end].strip()):
                        splitted.append(self.expression[start:end].strip())
                        start = end
                        break
                else:
                    continue
                break
            else:
                error('Could not find valid data type')
            if start == len(self.expression.strip()):
                break
            for end in range(len(self.expression), 0, -1):
                if self.expression[start:end].strip() in Operation.operators.keys():
                    splitted.append(self.expression[start:end].strip())
                    start = end
                    break
            else:
                error('Could not find valid operation')
        return splitted

    def to_dict(self):
        splitted = self.to_list()
        add_extra_perrs(splitted)
        return classify(splitted).to_dict()

class ForLoop:
    def __init__(self, text):
        if not self.valid(text):
            error('For Loop Not Valid')
        self.var_name = findall('(?<=^for)[^ ]+(?<= )', text)[0]
        self.list = text[len(findall('$for +[A-Ba-b][A-Ba-b0-9]* +of +[^ ]', text)[0]):].strip()

    def to_dict(self):
        return {
            'type': 'loop',
            'var': self.var_name,
            'list': self.list
        }

    @staticmethod
    def valid(text):
        return bool(search('for +[A-Ba-b][A-Ba-b0-9]* +of +.*$', text))


class Parser:
    def __init__(self, codetext, indent='    '):
        self.codetext = codetext
        self.indent = indent
        self.parsed = None

    def parse(self):
        global line_num
        self.parsed = []
        spot = [self.parsed]
        line_num = 1
        for line in self.codetext.split('\n'):
            indention = 0
            for _ in range(ceil(len(line) / len(self.indent)-1)):
                if line[indention * len(self.indent):(indention + 1) * len(self.indent)] != self.indent:
                    break
                indention += 1
            del spot[indention+1:]
            line = line[indention * len(self.indent):]
            spot[-1].append(Expression(line).to_dict())
            line_num += 1
        return self.parsed


files = glob('*.🐮🦬')
files.extend(glob('*.🦬🐮'))
files.extend(glob('*.🔥🦬'))
files.extend(glob('*.cb'))
files.extend(glob('*.fb'))
for file in files:
    print(Parser(open(file).read()).parse())
    interp = interpreter.Interpreter(Parser(open(file).read()).parse())
    interp.run()
