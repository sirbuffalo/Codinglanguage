#!/usr/bin/python3

import shutil
from re import *

from math import ceil


def get_indexes(l, function):
    return [i for i, e in enumerate(l) if function(e)]


def error(text):
    spaces = ' ' * (shutil.get_terminal_size().columns - len(text) - len(file) - len(str(line_num)) - 10)
    raise Exception(f'\033[38;5;52m\033[48;5;9m▲ Error: {text}{spaces}{file}\033[38;5;255m:\033[38;5;52m{line_num}\033[0m')


def add_extra_perrs(splitted):
    if type(splitted).__name__ == 'dict':
        return splitted
    if len(splitted) == 3:
        return [add_extra_perrs(splitted[0]), splitted[1], add_extra_perrs(splitted[2])]
    if len(splitted) == 2:
        return [splitted[0], add_extra_perrs(splitted[1])]
    if len(splitted) == 1:
        return add_extra_perrs(splitted[0])
    minus = 0
    for i, x in enumerate(splitted):
        if x['type'] in ['method', 'subscript']:
            splitted[x - 1: x + 1] = [[splitted[x - 1: x + 1]]]
            minus += 1
    for opers in pemdas:
        minus = 0
        for i in get_indexes(splitted, lambda e: 'operation' in e and e['operation'] in opers):
            if splitted[i - minus]['operation'] in SingleOperation.operators:
                splitted[i + 1 - minus] = add_extra_perrs(splitted[i + 1 - minus])
                splitted[i - minus:i + 2 - minus] = [[splitted[i - minus:i + 2 - minus]]]
                minus += 1
            else:
                splitted[i - 1 - minus] = add_extra_perrs(splitted[i - 1 - minus])
                splitted[i + 1 - minus] = add_extra_perrs(splitted[i + 1 - minus])
                splitted[i - 1 - minus:i + 2 - minus] = [splitted[i - 1 - minus:i + 2 - minus]]
                minus += 2
    return splitted

def classify(splitted):
    if type(splitted).__name__ == 'dict':
        return splitted['datatype'](splitted['data'])
    if len(splitted) == 1:
        return classify(splitted[0])
    if len(splitted) == 2:
        if splitted[1]['type'] == 'method':
            return BuiltInMethod(splitted[0], splitted[1])
        elif splitted[1]['type'] == 'subscript':
            return SubScript(classify(splitted[0]), splitted[1]['text'])
        else:
            return SingleOperation(splitted[0]['operation'], classify(splitted[1]))
    if len(splitted) != 3:
        print(splitted)
        raise Exception("len(splitted) != 3")
    return Operation(splitted[1]['operation'], classify(splitted[0]), classify(splitted[2]))

class BuiltInFunction:
    functions = {
        'print': ['value'],
        'input': ['prompt'],
        'int': ['value'],
        'float': ['value']
    }

    def __init__(self, text):
        if not BuiltInFunction.valid(text):
            error('Not a Built in Function')
        self.text = text.strip()
        self.func_name = findall('^[A-Za-z][A-Za-z0-9]*\(', text)[0][:-1]
        self.args = ['']
        perrs = 0
        for char in text[len(self.func_name) + 1:-1]:
            if char in ['(', '[']:
                perrs += 1
            elif char in [')', ']']:
                perrs -= 1
            elif perrs == 0 and char == ',':
                self.args.append('')
            if char != ',' or perrs != 0:
                self.args[-1] += char
        self.args = {BuiltInFunction.functions[self.func_name][i]: Expression(val).to_dict() for i, val in enumerate(self.args)}
    def to_dict(self):
        ans = {
            'type': self.func_name
        }
        ans.update(self.args)
        return ans

    @staticmethod
    def valid(text):
        if search('^[A-Za-z][A-Za-z0-9]*\(.*\)$', text.strip()):
            func_name = findall('^[A-Za-z][A-Za-z0-9]*\(', text.strip())[0][:-1]
            if func_name in BuiltInFunction.functions:
                return True
        return False

class Bool:
    def __init__(self, text):
        if not Bool.valid(text):
            error('Invaild Bool')
        self.value = text.strip() == 'True'

    def to_dict(self):
        return {
            'type': 'bool',
            'value': self.value
        }

    @staticmethod
    def valid(text):
        return text.strip() == 'True' or text.strip() == 'False'

class Var:
    def __init__(self, name):
        if not Var.valid(name):
            error(f'{name} is not a valid variable name')
        self.value = name

    def to_dict(self):
        return {
            'type': 'getvar',
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
        if len(value.strip()) < 7:
            return False
        if value[0] != '[':
            return False
        if value[-1] != ']':
            return False
        if '...' not in value[1:-1]:
            return False
        brackets = 0
        found_dots = False
        for i, char in enumerate(value[1:-1]):
            if char == '[':
                brackets += 1
            elif char == ']':
                brackets -= 1
            if brackets < 0:
                return False
            elif brackets == 0 and value[i:i + 3] == '...':
                found_dots = True
        return found_dots

class List:
    def __init__(self, value):
        if not List.valid(value):
            error('Invalid List')
        self.values = ['']
        perrs = 0
        for char in value.strip()[1:-1]:
            if char in ['[', '(']:
                perrs += 1
            elif char in [']', ')']:
                perrs -= 1
            elif perrs == 0 and char == ',':
                self.values.append('')
            if char != ',' or perrs != 0:
                self.values[-1] += char
        self.values = [Expression(exp).to_dict() for exp in self.values]

    def to_dict(self):
        return {
            'type': 'list',
            'values': self.values
        }

    @staticmethod
    def valid(value):
        if not (value.strip()[0] == '[' and value.strip()[-1] == ']'):
            return False
        bracs = 0
        for char in value.strip()[1:-1]:
            if char == '[':
                bracs += 1
            elif char == ']':
                bracs -= 1
            if bracs < 0:
                return False
        return True

class SubScript:
    def __init__(self, target, text):
        if not SubScript.valid(text):
            error('Not valid subscript')
        self.text = text.strip()
        self.target = target

    def to_dict(self):
        return {
            'type': 'subscript',
            'target': self.target.to_dict(),
            'index': Expression(self.text[1:-1]).to_dict()
        }

    @staticmethod
    def valid(text):
        text = text.strip()
        if not len(text) > 2:
            return False
        if not (text[0] == '[' and text[-1] == ']'):
            return False
        bracs = 0
        for char in text[1:-1]:
            if char == '[':
                bracs += 1
            if char == ']':
                bracs
            if bracs < 0:
                return False
        if bracs == 0:
            return True
        return False



class BuiltInMethod:
    methods = {
        'append': {
            'inputs': [
                'value'
            ]
        }
    }
    def __init__(self, target, text):
        if not BuiltInMethod.valid(text):
            error('Invalid Method')
        self.target = target
        self.method = findall('^.[a-zA-Z][a-zA-Z0-9]*\(', text)[0][1:-1]
        self.args = ['']
        perrs = 0
        for char in text[len(self.method) + 2:-1]:
            if char in ['(', '[']:
                perrs += 1
            elif char in [')', ']']:
                perrs -= 1
            elif perrs == 0 and char == ',':
                self.args.append('')
            if char != ',' or perrs != 0:
                self.args[-1] += char
        self.args = {BuiltInMethod.methods[self.method]['inputs'][i]: Expression(val).to_dict() for i, val in enumerate(self.args)}

    def to_dict(self):
        ans = {
            'type': self.method,
            'target': classify(self.target).to_dict()
        }
        ans.update(self.args)
        return ans

    @staticmethod
    def valid(text):
        if search('^.[a-zA-Z][a-zA-Z0-9]*\(.*\)$', text):
            method = findall('^.[a-zA-Z][a-zA-Z0-9]*\(', text)[0][1:-1]
            if method in BuiltInMethod.methods:
                perrs = 0
                for char in text[len(method) + 1:]:
                    if char == '(':
                        perrs += 1
                    elif char == ')':
                        perrs -= 1
                if perrs == 0:
                    return True
        return False


class Expression:
    data_types = [
        Int,
        Float,
        Range,
        List,
        Bool,
        BuiltInFunction,
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
            for end in range(len(self.expression), 0, -1):
                if self.expression[start:end].strip() in SingleOperation.operators:
                    splitted.append({
                        'type': 'single operation',
                        'operation': self.expression[start:end].strip()
                    })
                    start = end
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
            else:
                if start == len(self.expression.strip()):
                    break
                for end in range(len(self.expression), 0, -1):
                    if self.expression[start:end].strip() in SingleOperation.operators:
                        splitted.append({
                            'type': 'single operation',
                            'operation': self.expression[start:end].strip()
                        })
                        start = end
                for end in range(len(self.expression), 0, -1):
                    for data_type in Expression.data_types:
                        if data_type.valid(self.expression[start:end].strip()):
                            splitted.append({
                                'type': 'datatype',
                                'data': self.expression[start:end].strip(),
                                'datatype': data_type
                            })
                            start = end
                            break
                    else:
                        continue
                    break
                else:
                    error('Could not find valid data type')
                while True:
                    for end in range(len(self.expression), 0, -1):
                        if BuiltInMethod.valid(self.expression[start:end].strip()):
                            splitted.append({
                                'type': 'method',
                                'text': self.expression[start:end].strip()
                            })
                            start = end
                            break
                        elif SubScript.valid(self.expression[start:end]):
                            splitted.append({
                                'type': 'subscript',
                                'text': self.expression[start:end].strip()
                            })
                            start = end
                            break
                    else:
                        break
            if start == len(self.expression.strip()):
                break
            for end in range(len(self.expression), 0, -1):
                if self.expression[start:end].strip() in Operation.operators.keys():
                    splitted.append({
                        'type': 'operation',
                        'operation': self.expression[start:end].strip()
                    })
                    start = end
                    break
            else:
                print(splitted, self.expression)
                error('Could not find valid operation')
        return splitted

    def to_dict(self):
        splitted = self.to_list()
        splitted = add_extra_perrs(splitted)
        return classify(splitted).to_dict()

pemdas = [
    ['^'],
    ['*', '/'],
    ['+', '-'],
    ['%'],
    ['==', '!='],
    ['not'],
    ['and', 'or'],
    ['=']
]

class SingleOperation:
    operators = {
        'not': {
            'name': 'not',
            'types': [
                Bool,
                BuiltInFunction,
                Var
            ]
        }
    }


    def __init__(self, text, value):
        self.operation = text
        self.value = value

    def to_dict(self):
        return {
            'type': SingleOperation.operators[self.operation]['name'],
            'value': self.value.to_dict()
        }

    @staticmethod
    def valid(text, value):
        types = [Operation, SingleOperation]
        if 'type' in SingleOperation.operators[text.strip()]:
            types.append(SingleOperation.operators[text.strip()]['type'])
        if 'types' in SingleOperation.operators[text.strip()]:
            types.extend(SingleOperation.operators[text.strip()]['types'])
        return isinstance(value, tuple(types))


class Operation:
    operators = {
        '*': {
                'name': 'mul',
                'types': [Int, Float, BuiltInFunction, Var]
            },
        '/': {
                'name': 'div',
                'types': [Int, Float, BuiltInFunction, Var]
            },
        '+': {
                'name': 'add',
                'types': [Int, Float, BuiltInFunction, Var]
            },
        '-': {
                'name': 'sub',
                'types': [Int, Float, BuiltInFunction, Var]
            },
        '^': {
            'name': 'pow',
            'types': [Int, Float, BuiltInFunction, Var]
        },
        '%': {
            'name': 'mod',
            'types': [Int, Float, BuiltInFunction, Var]
        },
        '=': {
            'name': 'setvar',
            'type1': Var,
            'types2': [Int, Float, Bool, Range, List, BuiltInFunction, Var],
            'name1': 'name',
            'name2': 'value',
            'prop1': ['name']
        },
        '*=': {
            'name': 'mulset',
            'type1': Var,
            'types2': [Int, Float, Bool, Range, List, BuiltInFunction, Var],
            'name1': 'target',
            'name2': 'value'
        },
        '/=': {
            'name': 'divset',
            'type1': Var,
            'types2': [Int, Float, Bool, Range, List, BuiltInFunction, Var],
            'name1': 'target',
            'name2': 'value'
        },
        '+=': {
            'name': 'addset',
            'type1': Var,
            'types2': [Int, Float, Bool, Range, List, BuiltInFunction, Var],
            'name1': 'target',
            'name2': 'value'
        },
        '-=': {
            'name': 'subset',
            'type1': Var,
            'types2': [Int, Float, Bool, Range, List, BuiltInFunction, Var],
            'name1': 'target',
            'name2': 'value'
        },
        '^=': {
            'name': 'powset',
            'type1': Var,
            'types2': [Int, Float, Bool, Range, List, BuiltInFunction, Var],
            'name1': 'target',
            'name2': 'value'
        },
        'and': {
            'name': 'and',
            'types': [
                Bool, BuiltInFunction, Var
            ]
        },
        'or': {
            'name': 'or',
            'types': [
                Bool, BuiltInFunction, Var
            ]
        },
        '==': {
            'name': 'equal',
            'types': [
                Int,
                Float,
                Range,
                List,
                Bool,
                BuiltInFunction,
                Var
            ]
        },
        '!=': {
            'name': 'notequal',
            'types': [
                Int,
                Float,
                Range,
                List,
                Bool,
                BuiltInFunction,
                Var
            ]
        }
    }

    def __init__(self, operation, value1, value2):
        if not Operation.valid(operation, value1, value2):
            print(Operation.valid(operation, value1, value2), operation, value1, value2, line_num)
            raise Exception('test')
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
        valids1 = [Operation, SingleOperation]
        valids2 = [Operation, SingleOperation]
        if 'type' in data:
            valids1.append(data['type'])
            valids2.append(data['type'])
        if 'types' in data:
            for data_type in data['types']:
                valids1.append(data_type)
                valids2.append(data_type)
        if 'type1' in data:
            valids1.append(data['type1'])
        if 'types1' in data:
            for data_type in data['types1']:
                valids1.append(data_type)
        if 'type2' in data:
            valids2.append(data['type2'])
        if 'types2' in data:
            for data_type in data['types2']:
                valids2.append(data_type)
        return isinstance(value1, tuple(valids1)) and isinstance(value2, tuple(valids2))

class ForLoop:
    def __init__(self, text, parser):
        if not self.valid(text):
            error('For Loop Not Valid')
        self.parser = parser
        self.var_name = findall('(?<=for) +[A-Za-z][A-Za-z0-9]* ', text)[0].strip()
        self.list = text[len(findall('^for +[A-Za-z][A-Za-z0-9]* +of +[^ ]', text)[0]) - 1:].strip()

    def do(self):
        code = []
        self.parser.spot[-1].append({
            'type': 'loop',
            'var': self.var_name,
            'list': Expression(self.list).to_dict(),
            'code': code
        })
        self.parser.spot.append(code)

    @staticmethod
    def valid(text):
        return bool(search('^for +[A-Za-z][A-Za-z0-9]* +of +.*', text))

class IfStatement:
    def __init__(self, text, parser):
        if not IfStatement.valid(text):
            error('invalid if statement')
        self.parser = parser
        self.text = text
        self.expression = text[2:].strip()

    def do(self):
        code = []
        self.parser.spot[-1].append({
            'type': 'switch',
            'cases': [
                {
                    'cond': Expression(self.expression).to_dict(),
                    'code': code
                }
            ]
        })
        self.parser.spot.append(code)

    @staticmethod
    def valid(text):
        return bool(search('^if +.*$', text))


class ElseIfStatement:
    def __init__(self, text, parser):
        if not ElseIfStatement.valid(text):
            error('invalid elif statement')
        self.parser = parser
        self.expression = text[4:].strip()

    def do(self):
        code = []
        self.parser.spot[-1][-1]['cases'].append({
            'cond': Expression(self.expression).to_dict(),
            'code': code
        })
        self.parser.spot.append(code)

    @staticmethod
    def valid(text):
        return bool(search('^elif +.*$', text))


class ElseStatement:
    def __init__(self, text, parser):
        if not ElseStatement.valid(text):
            error('invalid else statement')
        self.parser = parser

    def do(self):
        code = []
        self.parser.spot[-1][-1]['default'] = code
        self.parser.spot.append(code)

    @staticmethod
    def valid(text):
        return text.strip() == 'else'


class Parser:
    commands = [
        ForLoop,
        IfStatement,
        ElseIfStatement,
        ElseStatement
    ]

    def __init__(self, file, indent='    '):
        self.file = file
        self.codetext = open(file).read()
        self.indent = indent
        self.parsed = None
        self.spot = None

    def parse(self):
        global line_num
        global file
        file = self.file
        self.parsed = []
        self.spot = [self.parsed]
        line_num = 1
        for line in self.codetext.split('\n'):
            indention = 0
            for _ in range(ceil(len(line) / len(self.indent)-1)):
                if line[indention * len(self.indent):(indention + 1) * len(self.indent)] != self.indent:
                    break
                indention += 1
            del self.spot[indention+1:]
            line = line[indention * len(self.indent):]
            if '#' in line:
                line = line[:line.index('#')]
            if line == '':
                continue
            for command in Parser.commands:
                if command.valid(line):
                    command(line, self).do()
                    break
            else:
                self.spot[-1].append(Expression(line).to_dict())

            line_num += 1
        return self.parsed