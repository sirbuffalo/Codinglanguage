class UnknownExpressionType(Exception):
    pass

class UnknownInstructionType(Exception):
    pass

class UnknownListType(Exception):
    pass

class Variable:
    def equal(self, other):
        return Bool(self.val == other.val)

class Bool(Variable):
    def __init__(self, val):
        self.val = bool(val)

    def xnot(self):
        return Bool(not self.val)

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

class Interpreter:
    def __init__(self, ast):
        self._ast = ast

        self._exprTypes = {
            'add': self._add,
            'bool': self._bool,
            'div': self._div,
            'equal': self._equal,
            'float': self._float,
            'get var': self._get_var,
            'int': self._int,
            'mul': self._mul,
            'not': self._not,
            'sub': self._sub,
        }

        self._instrTypes = {
            'if': self._if,
            'loop': self._loop,
            'print': self._print,
            'set var': self._set_var,
        }

        self._listTypes = {
            'range': self._range,
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

    def _if(self, instr, vars):
        expr = self._expr(instr['cond'], vars)

        if expr.val:
            self._instrs(instr['code'], vars)
        elif 'else' in instr:
            self._instrs(instr['else'], vars)

    def _loop(self, instr, vars):
        for iter in self._list(instr['list'], vars):
            vars[instr['var']] = iter
            self._instrs(instr['code'], vars)

    def _print(self, instr, vars):
        print(self._expr(instr['value'], vars).val)

    def _set_var(self, instr, vars):
        vars[instr['name']] = self._expr(instr['value'], vars)

    def _list(self, lst, vars):
        if lst['type'] not in self._listTypes:
            raise UnknownListType(lst['type'])

        return self._listTypes[lst['type']](lst, vars)

    def _range(self, lst, vars):
        start = self._expr(lst['start'], vars)
        end = self._expr(lst['end'], vars)
        for i in range(start.val, end.val):
            yield Int(i)

    def _expr(self, expr, vars):
        if expr['type'] not in self._exprTypes:
            raise UnknownExpressionType(expr['type'])

        return self._exprTypes[expr['type']](expr, vars)

    def _add(self, expr, vars):
        num1 = self._expr(expr['num1'], vars)
        num2 = self._expr(expr['num2'], vars)
        return num1.add(num2)

    def _bool(self, expr, vars):
        return Bool(expr['value'])

    def _div(self, expr, vars):
        num1 = self._expr(expr['num1'], vars)
        num2 = self._expr(expr['num2'], vars)
        return num1.div(num2)

    def _equal(self, expr, vars):
        num1 = self._expr(expr['num1'], vars)
        num2 = self._expr(expr['num2'], vars)
        return num1.equal(num2)

    def _float(self, expr, vars):
        return Float(expr['value'])

    def _get_var(self, expr, vars):
        return vars[expr['name']]

    def _int(self, expr, vars):
        return Int(expr['value'])

    def _mul(self, expr, vars):
        num1 = self._expr(expr['num1'], vars)
        num2 = self._expr(expr['num2'], vars)
        return num1.mul(num2)

    def _not(self, expr, vars):
        num = self._expr(expr['num'], vars)
        return num.xnot()

    def _sub(self, expr, vars):
        num1 = self._expr(expr['num1'], vars)
        num2 = self._expr(expr['num2'], vars)
        return num1.sub(num2)
