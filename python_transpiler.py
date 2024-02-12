import interpreter

class PythonTranspiler:
    def __init__(self):
        self._exprTypes = {
            'float': self._float,
            'int': self._int,
            'string': self._string,
        }

        self._instrTypes = {
            'print': self._print,
        }

    def instrs(self, instrs):
        ret = []

        for instr in instrs:
            ret.append(self._instr(instr))

        return ''.join(ret)

    def _instr(self, instr):
        if instr['type'] not in self._instrTypes:
            raise interpreter.UnknownInstructionType(instr['type'])

        return self._instrTypes[instr['type']](instr)

    def _expr(self, expr):
        if type(expr) is int:
            return expr
        elif type(expr) is float:
            return expr
        elif type(expr) is str:
            return expr

        if expr['type'] not in self._exprTypes:
            raise interpreter.UnknownExpressionType(expr['type'])

        return self._exprTypes[expr['type']](expr)

    def _int(self, expr):
        return str(self._expr(expr['value']))

    def _float(self, expr):
        return str(self._expr(expr['value']))

    def _string(self, expr):
        return f"'{self._expr(expr['value'])}'"

    def _print(self, expr):
        return f'print({self._expr(expr["value"])})\n'
