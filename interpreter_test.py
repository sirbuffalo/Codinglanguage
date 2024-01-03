#!/usr/bin/python3

import interpreter
import unittest

class TestInterpreter(unittest.TestCase):
    def setUp(self):
        self._interp = interpreter.Interpreter([])

    def test_expr_add(self):
        res = self._interp._expr({
            'type': 'add',
            'num1': {
                'type': 'int',
                'value': 3,
            },
            'num2': {
                'type': 'int',
                'value': 4,
            },
        }, {})

        self.assertEqual(7, res.val)

    def test_expr_bool(self):
        res = self._interp._expr({
            'type': 'bool',
            'value': True,
        }, {})

        self.assertEqual(True, res.val)

    def test_expr_div(self):
        res = self._interp._expr({
            'type': 'div',
            'num1': {
                'type': 'int',
                'value': 12,
            },
            'num2': {
                'type': 'int',
                'value': 3,
            },
        }, {})

        self.assertEqual(4, res.val)

    def test_expr_equal_false(self):
        res = self._interp._expr({
            'type': 'equal',
            'num1': {
                'type': 'int',
                'value': 5,
            },
            'num2': {
                'type': 'int',
                'value': 6,
            },
        }, {})

        self.assertEqual(False, res.val)

    def test_expr_equal_true(self):
        res = self._interp._expr({
            'type': 'equal',
            'num1': {
                'type': 'int',
                'value': 5,
            },
            'num2': {
                'type': 'int',
                'value': 5,
            },
        }, {})

        self.assertEqual(True, res.val)

    def test_expr_float(self):
        res = self._interp._expr({
            'type': 'float',
            'value': 1.5,
        }, {})

        self.assertEqual(1.5, res.val)

    def test_expr_get_var(self):
        res = self._interp._expr({
            'type': 'get var',
            'name': 'test1',
        }, {
            'test1': self._interp._expr({
                'type': 'int',
                'value': 5,
            }, {}),
        })

        self.assertEqual(5, res.val)

    def test_expr_int(self):
        res = self._interp._expr({
            'type': 'int',
            'value': 5,
        }, {})

        self.assertEqual(5, res.val)

    def test_expr_mul(self):
        res = self._interp._expr({
            'type': 'mul',
            'num1': {
                'type': 'int',
                'value': 3,
            },
            'num2': {
                'type': 'int',
                'value': 4,
            },
        }, {})

        self.assertEqual(12, res.val)

    def test_expr_not(self):
        res = self._interp._expr({
            'type': 'not',
            'num': {
                'type': 'bool',
                'value': False,
            },
        }, {})

        self.assertEqual(True, res.val)

    def test_expr_sub(self):
        res = self._interp._expr({
            'type': 'sub',
            'num1': {
                'type': 'int',
                'value': 10,
            },
            'num2': {
                'type': 'int',
                'value': 4,
            },
        }, {})

        self.assertEqual(6, res.val)

    def test_instr_loop(self):
        vars = {
            'test1': self._interp._expr({
                'type': 'int',
                'value': 0,
            }, {})
        }

        self._interp._instr({
            'type': 'loop',
            'var': 'i',
            'list': {
                'type': 'range',
                'start': {
                    'type': 'int',
                    'value': 0,
                },
                'end': {
                    'type': 'int',
                    'value': 10,
                },
            },
            'code': [
                {
                    'type': 'set var',
                    'name': 'test1',
                    'value': {
                        'type': 'add',
                        'num1': {
                            'type': 'get var',
                            'name': 'test1',
                        },
                        'num2': {
                            'type': 'get var',
                            'name': 'i',
                        },
                    },
                },
            ],
        }, vars)

        self.assertEqual(45, vars['test1'].val)

    def test_instr_equation(self):
        vars = {}

        self._interp._instr({
			'type': 'set var',
            'name': 'times',
            'value': {
                'type': 'div',
                'num1': {
                    'type': 'mul',
                    'num1': {
                        'type': 'add',
                        'num1': {
                            'type': 'int',
                            'value': 1,
                         },
                        'num2': {
                            'type': 'int',
                            'value': 1,
                        },
                    },
                    'num2': {
                        'type': 'int',
                        'value': 6,
                    },
                },
                'num2': {
                    'type': 'int',
                    'value': 3,
                },
            },
        }, vars)

        self.assertEqual(4, vars['times'].val)


if __name__ == '__main__':
    unittest.main()
