class UnknownExpressionType(Exception):
    pass

class UnknownInstructionType(Exception):
    pass

class UnknownListType(Exception):
    pass

class Variable:
    pass

class Int(Variable):
    def __init__(self, val):
        self.val = int(val)

class Interpreter:
    def __init__(self, ast):
        self._ast = ast

        self._exprTypes = {
            'add': self._add,
            'get var': self._get_var,
            'int': self._int,
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
        return Int(num1.val + num2.val)

    def _int(self, expr, vars):
        return Int(expr['value'])

    def _get_var(self, expr, vars):
        return vars[expr['name']]
