class UnknownExpressionType(Exception):
    pass

class UnknownInstructionType(Exception):
    pass

class Variable:
    def equal(self, other):
        return Bool(self.val == other.val)

    def string(self):
        return f'{self.val}'

class Bool(Variable):
    def __init__(self, val):
        self.val = bool(val)

    def and_(self, other):
        return Bool(self.val and other.val)

    def not_(self):
        return Bool(not self.val)

    def or_(self, other):
        return Bool(self.val or other.val)

class Iterable(Variable):
    def string(self):
        joined = ','.join(x.string() for x in self.iterate())
        return f'[{joined}]'

class List(Iterable):
    def __init__(self):
        self.val = []

    def iterate(self):
        return self.val

    def append(self, value):
        self.val.append(value)

    def insert(self, index, value):
        self.val.insert(index.val, value)

    def len(self):
        return Int(len(self.val))

    def subscript(self, index):
        return self.val[index.val]

class Range(Iterable):
    def __init__(self, start, end):
        self._start = start
        self._end = end

    def iterate(self):
        for i in range(self._start.val, self._end.val):
            yield Int(i)

class Number(Variable):
    def add(self, other):
        return type(self)(self.val + other.val)

    def div(self, other):
        return type(self)(self.val / other.val)

    def mul(self, other):
        return type(self)(self.val * other.val)

    def sub(self, other):
        return type(self)(self.val - other.val)

class Int(Number):
    def __init__(self, val):
        self.val = int(val)

class Float(Number):
    def __init__(self, val):
        self.val = float(val)

class String(Variable):
    def __init__(self, val):
        self.val = str(val)

    def subscript(self, index):
        return String(self.val[index.val])

class Interpreter:
    def __init__(self, ast):
        self._ast = ast

        self._exprTypes = {
            'add': self._add,
            'and': self._and,
            'bool': self._bool,
            'div': self._div,
            'equal': self._equal,
            'float': self._float,
            'get var': self._get_var,
            'int': self._int,
            'len': self._len,
            'list': self._list,
            'mul': self._mul,
            'not': self._not,
            'or': self._or,
            'range': self._range,
            'string': self._string,
            'sub': self._sub,
            'subscript': self._subscript,
        }

        self._instrTypes = {
            'append': self._append,
            'if': self._if,
            'insert': self._insert,
            'loop': self._loop,
            'print': self._print,
            'set var': self._set_var,
        }

    def run(self):
        self._instrs(self._ast, {})

    def _instrs(self, instrs, vars):
        for instr in instrs:
            self._instr(instr, vars)

    def _instr(self, instr, vars):
        if instr['type'] not in self._instrTypes:
            raise UnknownInstructionType(instr['type'])

        self._instrTypes[instr['type']](instr, vars)

    def _append(self, instr, vars):
        target = self._expr(instr['target'], vars)
        value = self._expr(instr['value'], vars)
        target.append(value)

    def _if(self, instr, vars):
        expr = self._expr(instr['cond'], vars)

        if expr.val:
            self._instrs(instr['code'], vars)
        elif 'else' in instr:
            self._instrs(instr['else'], vars)

    def _insert(self, instr, vars):
        target = self._expr(instr['target'], vars)
        index = self._expr(instr['index'], vars)
        value = self._expr(instr['value'], vars)
        target.insert(index, value)

    def _loop(self, instr, vars):
        for iter in self._expr(instr['list'], vars).iterate():
            vars[instr['var']] = iter
            self._instrs(instr['code'], vars)

    def _print(self, instr, vars):
        print(self._expr(instr['value'], vars).string())

    def _set_var(self, instr, vars):
        vars[instr['name']] = self._expr(instr['value'], vars)

    def _expr(self, expr, vars):
        if type(expr) is int:
            return Int(expr)
        elif type(expr) is float:
            return Float(expr)
        elif type(expr) is bool:
            return Bool(expr)
        elif type(expr) is str:
            return String(expr)

        if expr['type'] not in self._exprTypes:
            raise UnknownExpressionType(expr['type'])

        return self._exprTypes[expr['type']](expr, vars)

    def _add(self, expr, vars):
        v1 = self._expr(expr['value1'], vars)
        v2 = self._expr(expr['value2'], vars)
        return v1.add(v2)

    def _and(self, expr, vars):
        v1 = self._expr(expr['value1'], vars)
        v2 = self._expr(expr['value2'], vars)
        return v1.and_(v2)

    def _bool(self, expr, vars):
        return Bool(bool(self._expr(expr['value'], vars).val))

    def _div(self, expr, vars):
        v1 = self._expr(expr['value1'], vars)
        v2 = self._expr(expr['value2'], vars)
        return v1.div(v2)

    def _equal(self, expr, vars):
        v1 = self._expr(expr['value1'], vars)
        v2 = self._expr(expr['value2'], vars)
        return v1.equal(v2)

    def _float(self, expr, vars):
        return Float(float(self._expr(expr['value'], vars).val))

    def _get_var(self, expr, vars):
        return vars[expr['name']]

    def _int(self, expr, vars):
        return Int(int(self._expr(expr['value'], vars).val))

    def _len(self, expr, vars):
        target = self._expr(expr['target'], vars)
        return target.len()

    def _list(self, expr, vars):
        return List()

    def _mul(self, expr, vars):
        v1 = self._expr(expr['value1'], vars)
        v2 = self._expr(expr['value2'], vars)
        return v1.mul(v2)

    def _not(self, expr, vars):
        value = self._expr(expr['value'], vars)
        return value.not_()

    def _or(self, expr, vars):
        v1 = self._expr(expr['value1'], vars)
        v2 = self._expr(expr['value2'], vars)
        return v1.or_(v2)

    def _range(self, expr, vars):
        start = self._expr(expr['start'], vars)
        end = self._expr(expr['end'], vars)
        return Range(start, end)

    def _string(self, expr, vars):
        return String(str(self._expr(expr['value'], vars).val))

    def _sub(self, expr, vars):
        v1 = self._expr(expr['value1'], vars)
        v2 = self._expr(expr['value2'], vars)
        return v1.sub(v2)

    def _subscript(self, expr, vars):
        target = self._expr(expr['target'], vars)
        index = self._expr(expr['index'], vars)
        return target.subscript(index)
