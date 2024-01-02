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

    def test_instr_loop(self):
        vars = {
            'test1': self._interp._expr({
                'type': 'int',
                'value': 0,
            }, {})
        }

        self._interp._instr({
            'type': 'loop',
            'var': '_',
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
                            'type': 'int',
                            'value': 2,
                        },
                    },
                },
            ],
        }, vars)

        self.assertEqual(20, vars['test1'].val)


if __name__ == '__main__':
    unittest.main()
