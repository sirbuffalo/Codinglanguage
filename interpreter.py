class UnknownExpressionType(Exception):
    pass

class UnknownInstructionType(Exception):
    pass

class UnknownListType(Exception):
    pass

class Variable:
    def add(self, other):
        return type(self)(self.val + other.val)

    def div(self, other):
        return type(self)(self.val / other.val)

    def mul(self, other):
        return type(self)(self.val * other.val)

    def sub(self, other):
        return type(self)(self.val - other.val)

class Int(Variable):
    def __init__(self, val):
        self.val = int(val)

class Float(Variable):
    def __init__(self, val):
        self.val = float(val)

class Interpreter:
    def __init__(self, ast):
        self._ast = ast

        self._exprTypes = {
            'add': self._add,
            'div': self._div,
            'float': self._float,
            'get var': self._get_var,
            'int': self._int,
            'mul': self._mul,
            'sub': self._sub,
        }

        self._instrTypes = {
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

    def _loop(self, instr, vars):
        for iter in self._list(instr['list'], vars):
            vars[instr['var']] = iter
            self._instrs(instr['code'], vars)

    def _print(self, instr, vars):
        print(self._expr(instr['value'], vars))

    def _set_var(self, instr, vars):
        vars[instr['name']] = self._expr(instr['value'], vars)

    def _list(self, lst, vars):
        if lst['type'] not in self._listTypes:
            raise UnknownListType(lst['type'])

        return self._listTypes[lst['type']](lst, vars)

    def _range(self, lst, vars):
        start = self._expr(lst['start'], vars)
        end = self._expr(lst['end'], vars)
        return range(start.val, end.val)

    def _expr(self, expr, vars):
        if expr['type'] not in self._exprTypes:
            raise UnknownExpressionType(expr['type'])

        return self._exprTypes[expr['type']](expr, vars)

    def _add(self, expr, vars):
        num1 = self._expr(expr['num1'], vars)
        num2 = self._expr(expr['num2'], vars)
        return num1.add(num2)

    def _div(self, expr, vars):
        num1 = self._expr(expr['num1'], vars)
        num2 = self._expr(expr['num2'], vars)
        return num1.div(num2)

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

    def _sub(self, expr, vars):
        num1 = self._expr(expr['num1'], vars)
        num2 = self._expr(expr['num2'], vars)
        return num1.sub(num2)
