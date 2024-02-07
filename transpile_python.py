import interpreter

class Transpiler:
    def __init__(self, ast):
        self._ast = ast

        self._exprTypes = {
            'int': self._int,
        }

        self._instrTypes = {
            'print': self._print,
        }

    def _expr(self, expr):
        if type(expr) is int:
            print(expr)

        if expr['type'] not in self._exprTypes:
            raise interpreter.UnknownExpressionType(expr['type'])

        return self._exprTypes[expr['type']](expr)

    def _int(self):
        pass

    def _print(self):
        pass
