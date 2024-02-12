#!/usr/bin/python3

import interpreter
import io
import sys
import unittest

class TestInterpreter(unittest.TestCase):
    def setUp(self):
        self._interp = interpreter.Interpreter([])
        self._stdoutbuf = io.StringIO()
        self._stdinbuf = io.StringIO()
        self._realstdout = sys.stdout
        self._realstdin = sys.stdin
        sys.stdout = self._stdoutbuf
        sys.stdin = self._stdinbuf

    def tearDown(self):
        sys.stdout = self._realstdout
        sys.stdin = self._realstdin

    def stdout(self):
        val = self._stdoutbuf.getvalue()
        self._stdoutbuf.truncate()
        self._stdoutbuf.seek(0)
        return val

    def stdin(self, val):
        loc = self._stdinbuf.tell()
        self._stdinbuf.write(val)
        self._stdinbuf.seek(loc)

    def test_expr_add(self):
        # 3 + 4

        res = self._interp._expr({
            'type': 'add',
            'value1': {
                'type': 'int',
                'value': 3,
            },
            'value2': {
                'type': 'int',
                'value': 4,
            },
        }, {})

        self.assertEqual(7, res.val)

    def test_expr_add_floatint(self):
        # 3.0 + 4

        res = self._interp._expr({
            'type': 'add',
            'value1': {
                'type': 'float',
                'value': 3.0,
            },
            'value2': {
                'type': 'int',
                'value': 4,
            },
        }, {})

        self.assertEqual(7.0, res.val)

    def test_expr_add_intfloat(self):
        # 3 + 4.0

        res = self._interp._expr({
            'type': 'add',
            'value1': {
                'type': 'int',
                'value': 3,
            },
            'value2': {
                'type': 'float',
                'value': 4.5,
            },
        }, {})

        self.assertEqual(7.5, res.val)

    def test_expr_and_false(self):
        # true and false

        res = self._interp._expr({
            'type': 'and',
            'value1': {
                'type': 'bool',
                'value': True,
            },
            'value2': {
                'type': 'bool',
                'value': False,
            },
        }, {})

        self.assertEqual(False, res.val)

    def test_expr_and_true(self):
        # true and true

        res = self._interp._expr({
            'type': 'and',
            'value1': {
                'type': 'bool',
                'value': True,
            },
            'value2': {
                'type': 'bool',
                'value': True,
            },
        }, {})

        self.assertEqual(True, res.val)

    def test_expr_bool(self):
        # true

        res = self._interp._expr({
            'type': 'bool',
            'value': True,
        }, {})

        self.assertEqual(True, res.val)

    def test_expr_func(self):
        vars = {}

        # test1 = func(test2) { return test2 + 1 }
        # test3 = test1(5)

        self._interp._instrs([
            {
                'type': 'setvar',
                'name': 'test1',
                'value': {
                    'type': 'func',
                    'args': ['test2'],
                    'code': [
                        {
                            'type': 'return',
                            'value': {
                                'type': 'add',
                                'value1': {
                                    'type': 'getvar',
                                    'name': 'test2',
                                },
                                'value2': {
                                    'type': 'int',
                                    'value': 1,
                                },
                            },
                        },
                    ],
                },
            },
            {
                'type': 'setvar',
                'name': 'test3',
                'value': {
                    'type': 'call',
                    'target': {
                        'type': 'getvar',
                        'name': 'test1',
                    },
                    'args': [
                        {
                            'type': 'int',
                            'value': 5,
                        },
                    ],
                },
            },
        ], vars)

        self.assertEqual(6, vars['test3'].val)

    def test_expr_func_conditional(self):
        vars = {}

        # func(test1) { if test1 == 5 { return 10 } return 1 }(5)

        res = self._interp._expr({
            'type': 'call',
            'target': {
                'type': 'func',
                'args': ['test1'],
                'code': [
                    {
                        'type': 'if',
                        'cond': {
                            'type': 'equal',
                            'value1': {
                                'type': 'getvar',
                                'name': 'test1',
                            },
                            'value2': {
                                'type': 'int',
                                'value': 5,
                            },
                        },
                        'code': [
                            {
                                'type': 'return',
                                'value': {
                                    'type': 'int',
                                    'value': 10,
                                },
                            },
                        ],
                    },
                    {
                        'type': 'return',
                        'value': {
                            'type': 'int',
                            'value': 1,
                        },
                    },
                ],
            },
            'args': [
                {
                    'type': 'int',
                    'value': 5,
                },
            ],
        }, {})

        self.assertEqual(10, res.val)

    def test_expr_return_void(self):
        # test1 = func() {
        #   return
        #   print("B")
        # }
        # print("A")
        # test1()
        # print("C")

        self._interp._instrs([
            {
                'type': 'setvar',
                'name': 'test1',
                'value': {
                    'type': 'func',
                    'args': [],
                    'code': [
                        {
                            'type': 'return',
                        },
                        {
                            'type': 'print',
                            'value': {
                                'type': 'string',
                                'value': 'B',
                            },
                        },
                    ],
                },
            },
            {
                'type': 'print',
                'value': {
                    'type': 'string',
                    'value': 'A',
                },
            },
            {
                'type': 'call',
                'target': {
                    'type': 'getvar',
                    'name': 'test1',
                },
            },
            {
                'type': 'print',
                'value': {
                    'type': 'string',
                    'value': 'C',
                },
            },
        ], {})

        self.assertEqual('A\nC\n', self.stdout())

    def test_expr_func_kwargs(self):
        # func(test1, test2) { return test1 - test2 }(test2=3, 5)

        ret = self._interp._expr({
            'type': 'call',
            'target': {
                'type': 'func',
                'args': ['test1', 'test2'],
                'code': [
                    {
                        'type': 'return',
                        'value': {
                            'type': 'sub',
                            'value1': {
                                'type': 'getvar',
                                'name': 'test1',
                            },
                            'value2': {
                                'type': 'getvar',
                                'name': 'test2',
                            }
                        },
                    },
                ],
            },
            'kwargs': {
                'test2': {
                    'type': 'int',
                    'value': 3,
                },
            },
            'args': [
                {
                    'type': 'int',
                    'value': 5,
                },
            ],
        }, {})

        self.assertEqual(2, ret.val)

    def test_expr_div(self):
        # 12 / 3

        res = self._interp._expr({
            'type': 'div',
            'value1': {
                'type': 'int',
                'value': 12,
            },
            'value2': {
                'type': 'int',
                'value': 3,
            },
        }, {})

        self.assertEqual(4, res.val)

    def test_expr_div_floatint(self):
        # 12.0 / 3

        res = self._interp._expr({
            'type': 'div',
            'value1': {
                'type': 'float',
                'value': 12.0,
            },
            'value2': {
                'type': 'int',
                'value': 3,
            },
        }, {})

        self.assertEqual(4.0, res.val)

    def test_expr_div_intfloat(self):
        # 12 / 3.0

        res = self._interp._expr({
            'type': 'div',
            'value1': {
                'type': 'int',
                'value': 12,
            },
            'value2': {
                'type': 'float',
                'value': 4.8,
            },
        }, {})

        self.assertEqual(2.5, res.val)

    def test_expr_div_float_cast(self):
        # float(3) / 12

        res = self._interp._expr({
            'type': 'div',
            'value1': {
                'type': 'float',
                'value': {
                    'type': 'int',
                    'value': 3,
                },
            },
            'value2': {
                'type': 'int',
                'value': 12,
            },
        }, {})

        self.assertEqual(0.25, res.val)

    def test_expr_equal_false(self):
        # 5 == 6

        res = self._interp._expr({
            'type': 'equal',
            'value1': {
                'type': 'int',
                'value': 5,
            },
            'value2': {
                'type': 'int',
                'value': 6,
            },
        }, {})

        self.assertEqual(False, res.val)

    def test_expr_equal_true(self):
        # 5 == 5

        res = self._interp._expr({
            'type': 'equal',
            'value1': {
                'type': 'int',
                'value': 5,
            },
            'value2': {
                'type': 'int',
                'value': 5,
            },
        }, {})

        self.assertEqual(True, res.val)

    def test_expr_float(self):
        # 1.5

        res = self._interp._expr({
            'type': 'float',
            'value': 1.5,
        }, {})

        self.assertEqual(1.5, res.val)

    def test_expr_float_from_int(self):
        # float(5)

        res = self._interp._expr({
            'type': 'float',
            'value': {
                'type': 'int',
                'value': 5,
            },
        }, {})

        self.assertEqual(5.0, res.val)

    def test_expr_get_var(self):
        # test1

        res = self._interp._expr({
            'type': 'getvar',
            'name': 'test1',
        }, {
            'test1': self._interp._expr({
                'type': 'int',
                'value': 5,
            }, {}),
        })

        self.assertEqual(5, res.val)

    def test_expr_join(self):
        vars = {}

        # test1 = ["foo", "bar"]
        # test2 = test1.join("X")

        res = self._interp._instrs([
            {
                'type': 'setvar',
                'name': 'test1',
                'value': {
                    'type': 'list',
                },
            },
            {
                'type': 'append',
                'target': {
                    'type': 'getvar',
                    'name': 'test1',
                },
                'value': {
                    'type': 'string',
                    'value': 'foo',
                },
            },
            {
                'type': 'append',
                'target': {
                    'type': 'getvar',
                    'name': 'test1',
                },
                'value': {
                    'type': 'string',
                    'value': 'bar',
                },
            },
            {
                'type': 'setvar',
                'name': 'test2',
                'value': {
                    'type': 'join',
                    'target': {
                        'type': 'getvar',
                        'name': 'test1',
                    },
                    'value': {
                        'type': 'string',
                        'value': 'X',
                    },
                },
            },
        ], vars)

        self.assertEqual("fooXbar", vars['test2'].val)

    def test_expr_int(self):
        # 5

        res = self._interp._expr({
            'type': 'int',
            'value': 5,
        }, {})

        self.assertEqual(5, res.val)

    def test_expr_int_from_float(self):
        # int(5.2)

        res = self._interp._expr({
            'type': 'int',
            'value': {
                'type': 'float',
                'value': '5.2',
            },
        }, {})

        self.assertEqual(5, res.val)

    def test_expr_int_from_string(self):
        # int("5")

        res = self._interp._expr({
            'type': 'int',
            'value': {
                'type': 'string',
                'value': '5',
            },
        }, {})

        self.assertEqual(5, res.val)

    def test_expr_input(self):
        # input("foo")

        self.stdin('bar\n')

        res = self._interp._expr({
            'type': 'input',
            'prompt': {
                'type': 'string',
                'value': 'foo',
            }
        }, {})

        self.assertEqual('bar', res.val)

    def test_expr_len(self):
        vars = {}

        # test1 = [3,4]
        # test2 = test.len()

        self._interp._instrs([
            {
                'type': 'setvar',
                'name': 'test1',
                'value': {
                    'type': 'list',
                },
            },
            {
                'type': 'append',
                'target': {
                    'type': 'getvar',
                    'name': 'test1',
                },
                'value': {
                    'type': 'int',
                    'value': 3,
                },
            },
            {
                'type': 'append',
                'target': {
                    'type': 'getvar',
                    'name': 'test1',
                },
                'value': {
                    'type': 'int',
                    'value': 4,
                },
            },
            {
                'type': 'setvar',
                'name': 'test2',
                'value': {
                    'type': 'len',
                    'target': {
                        'type': 'getvar',
                        'name': 'test1',
                    },
                },
            },
        ], vars)

        self.assertEqual(2, vars['test2'].val)

    def test_expr_len_string(self):
        vars = {}

        # test1 = "foo".len()

        self._interp._instrs([
            {
                'type': 'setvar',
                'name': 'test1',
                'value': {
                    'type': 'len',
                    'target': {
                        'type': 'string',
                        'value': 'foo',
                    },
                },
            },
        ], vars)

        self.assertEqual(3, vars['test1'].val)

    def test_expr_list_values(self):
        # [3,4]

        val = self._interp._expr({
            'type': 'list',
            'values': [
                {
                    'type': 'int',
                    'value': 3,
                },
                {
                    'type': 'int',
                    'value': 4,
                },
            ],
        }, {})

        self.assertEqual([3, 4], [x.val for x in val.iterate()])

    def test_expr_mod(self):
        # 20 % 6

        res = self._interp._expr({
            'type': 'mod',
            'value1': {
                'type': 'int',
                'value': 20,
            },
            'value2': {
                'type': 'int',
                'value': 6,
            },
        }, {})

        self.assertEqual(2, res.val)

    def test_expr_mul(self):
        # 20 % 6

        res = self._interp._expr({
            'type': 'mod',
            'value1': {
                'type': 'int',
                'value': 20,
            },
            'value2': {
                'type': 'int',
                'value': 6,
            },
        }, {})

        self.assertEqual(4, res.val)

    def test_expr_mul(self):
        # 3 * 4

        res = self._interp._expr({
            'type': 'mul',
            'value1': {
                'type': 'int',
                'value': 3,
            },
            'value2': {
                'type': 'int',
                'value': 4,
            },
        }, {})

        self.assertEqual(12, res.val)

    def test_expr_not(self):
        # !false

        res = self._interp._expr({
            'type': 'not',
            'value': {
                'type': 'bool',
                'value': False,
            },
        }, {})

        self.assertEqual(True, res.val)

    def test_expr_notequal_false(self):
        # 6 != 6

        res = self._interp._expr({
            'type': 'notequal',
            'value1': {
                'type': 'int',
                'value': 6,
            },
            'value2': {
                'type': 'int',
                'value': 6,
            },
        }, {})

        self.assertEqual(False, res.val)

    def test_expr_notequal_true(self):
        # 5 != 6

        res = self._interp._expr({
            'type': 'notequal',
            'value1': {
                'type': 'int',
                'value': 5,
            },
            'value2': {
                'type': 'int',
                'value': 6,
            },
        }, {})

        self.assertEqual(True, res.val)

    def test_expr_or_false(self):
        # false or false

        res = self._interp._expr({
            'type': 'or',
            'value1': {
                'type': 'bool',
                'value': False,
            },
            'value2': {
                'type': 'bool',
                'value': False,
            },
        }, {})

        self.assertEqual(False, res.val)

    def test_expr_or_true(self):
        # true or false

        res = self._interp._expr({
            'type': 'or',
            'value1': {
                'type': 'bool',
                'value': True,
            },
            'value2': {
                'type': 'bool',
                'value': False,
            },
        }, {})

        self.assertEqual(True, res.val)

    def test_expr_pow_int(self):
        # pow(2,4)

        res = self._interp._expr({
            'type': 'pow',
            'value1': {
                'type': 'int',
                'value': 2,
            },
            'value2': {
                'type': 'int',
                'value': 4,
            },
        }, {})

        self.assertEqual(16, res.val)

    def test_expr_pow_float(self):
        # pow(1.5,2)

        res = self._interp._expr({
            'type': 'pow',
            'value1': {
                'type': 'float',
                'value': 1.5,
            },
            'value2': {
                'type': 'int',
                'value': 2,
            },
        }, {})

        self.assertEqual(2.25, res.val)

    def test_expr_string(self):
        # "foo"

        res = self._interp._expr({
            'type': 'string',
            'value': 'foo',
        }, {})

        self.assertEqual('foo', res.val)

    def test_expr_string_from_int(self):
        # string(5)

        res = self._interp._expr({
            'type': 'string',
            'value': {
                'type': 'int',
                'value': 5,
            },
        }, {})

        self.assertEqual('5', res.val)

    def test_expr_sub(self):
        # 10 - 4

        res = self._interp._expr({
            'type': 'sub',
            'value1': {
                'type': 'int',
                'value': 10,
            },
            'value2': {
                'type': 'int',
                'value': 4,
            },
        }, {})

        self.assertEqual(6, res.val)

    def test_expr_subscript_list(self):
        vars = {}

        # test1 = [1,2]
        # test2 = test[1]

        self._interp._instrs([
            {
                'type': 'setvar',
                'name': 'test1',
                'value': {
                    'type': 'list',
                },
            },
            {
                'type': 'append',
                'target': {
                    'type': 'getvar',
                    'name': 'test1',
                },
                'value': {
                    'type': 'int',
                    'value': 1,
                },
            },
            {
                'type': 'append',
                'target': {
                    'type': 'getvar',
                    'name': 'test1',
                },
                'value': {
                    'type': 'int',
                    'value': 2,
                },
            },
            {
                'type': 'setvar',
                'name': 'test2',
                'value': {
                    'type': 'subscript',
                    'target': {
                        'type': 'getvar',
                        'name': 'test1',
                    },
                    'index': {
                        'type': 'int',
                        'value': 1,
                    },
                },
            },
        ], vars)

        self.assertEqual(2, vars['test2'].val)

    def test_expr_subscript_range(self):
        vars = {}

        # test1 = 2..10
        # test2 = test[4]

        self._interp._instrs([
            {
                'type': 'setvar',
                'name': 'test1',
                'value': {
                    'type': 'range',
                    'start': {
                        'type': 'int',
                        'value': 2,
                    },
                    'end': {
                        'type': 'int',
                        'value': 10,
                    },
                },
            },
            {
                'type': 'setvar',
                'name': 'test2',
                'value': {
                    'type': 'subscript',
                    'target': {
                        'type': 'getvar',
                        'name': 'test1',
                    },
                    'index': {
                        'type': 'int',
                        'value': 4,
                    },
                },
            },
        ], vars)

        self.assertEqual(6, vars['test2'].val)

    def test_expr_subscript_string(self):
        vars = {}

        # test1 = "bar"
        # test2 = test[1]

        self._interp._instrs([
            {
                'type': 'setvar',
                'name': 'test1',
                'value': {
                    'type': 'string',
                    'value': 'bar',
                },
            },
            {
                'type': 'setvar',
                'name': 'test2',
                'value': {
                    'type': 'subscript',
                    'target': {
                        'type': 'getvar',
                        'name': 'test1',
                    },
                    'index': {
                        'type': 'int',
                        'value': 1,
                    },
                },
            },
        ], vars)

        self.assertEqual('a', vars['test2'].val)

    def test_expr_typeof(self):
        # typeof(34.6)

        res = self._interp._expr({
            'type': 'typeof',
            'value': {
                'type': 'float',
                'value': 34.6,
            },
        }, {})

        self.assertEqual('float', res.val)

    def test_expr_xor_false(self):
        # true and true

        res = self._interp._expr({
            'type': 'xor',
            'value1': {
                'type': 'bool',
                'value': True,
            },
            'value2': {
                'type': 'bool',
                'value': True,
            },
        }, {})

        self.assertEqual(False, res.val)

    def test_expr_xor_true(self):
        # true and false

        res = self._interp._expr({
            'type': 'xor',
            'value1': {
                'type': 'bool',
                'value': True,
            },
            'value2': {
                'type': 'bool',
                'value': False,
            },
        }, {})

        self.assertEqual(True, res.val)

    def test_instr_addset(self):
        vars = {}

        # test1 = 1
        # test1 += 2

        self._interp._instrs([
            {
                'type': 'setvar',
                'name': 'test1',
                'value': {
                    'type': 'int',
                    'value': 1,
                },
            },
            {
                'type': 'addset',
                'target': {
                    'type': 'getvar',
                    'name': 'test1',
                },
                'value': {
                    'type': 'int',
                    'value': 2,
                },
            },
        ], vars)

        self.assertEqual(3, vars['test1'].val)

    def test_instr_append(self):
        vars = {}

        # test1 = []
        # test1.append(1)
        # test1.append(2)

        self._interp._instrs([
            {
                'type': 'setvar',
                'name': 'test1',
                'value': {
                    'type': 'list',
                },
            },
            {
                'type': 'append',
                'target': {
                    'type': 'getvar',
                    'name': 'test1',
                },
                'value': {
                    'type': 'int',
                    'value': 1,
                },
            },
            {
                'type': 'append',
                'target': {
                    'type': 'getvar',
                    'name': 'test1',
                },
                'value': {
                    'type': 'int',
                    'value': 2,
                },
            },
        ], vars)

        self.assertEqual([1, 2], [x.val for x in vars['test1'].val])

    def test_instr_divset(self):
        vars = {}

        # test1 = 12
        # test1 /= 3

        self._interp._instrs([
            {
                'type': 'setvar',
                'name': 'test1',
                'value': {
                    'type': 'int',
                    'value': 12,
                },
            },
            {
                'type': 'divset',
                'target': {
                    'type': 'getvar',
                    'name': 'test1',
                },
                'value': {
                    'type': 'int',
                    'value': 3,
                },
            },
        ], vars)

        self.assertEqual(4, vars['test1'].val)

    def test_instr_expr(self):
        # 1 + 2

        self._interp._instrs([
            {
                'type': 'add',
                'value1': {
                    'type': 'int',
                    'value': 1,
                },
                'value2': {
                    'type': 'int',
                    'value': 2,
                },
            },
        ], {})

    def test_instr_if_equal_true(self):
        vars = {}

        # test1 = 5
        # if test1 == 5:
        #   test1 *= 2

        self._interp._instrs([
            {
                'type': 'setvar',
                'name': 'test1',
                'value': {
                    'type': 'int',
                    'value': 5,
                },
            },
            {
                'type': 'if',
                'cond': {
                    'type': 'equal',
                    'value1': {
                        'type': 'getvar',
                        'name': 'test1',
                    },
                    'value2': {
                        'type': 'int',
                        'value': 5,
                    },
                },
                'code': [
                    {
                        'type': 'setvar',
                        'name': 'test1',
                        'value': {
                            'type': 'mul',
                            'value1': {
                                'type': 'getvar',
                                'name': 'test1',
                            },
                            'value2': {
                                'type': 'int',
                                'value': 2,
                            },
                        },
                    },
                ],
            },
        ], vars)

        self.assertEqual(10, vars['test1'].val)

    def test_instr_if_false(self):
        vars = {}

        # if false:
        #   result = 5
        # else:
        #   result = 8

        self._interp._instr({
            'type': 'if',
            'cond': {
                'type': 'bool',
                'value': False,
            },
            'code': [
                {
                    'type': 'setvar',
                    'name': 'result',
                    'value': {
                        'type': 'int',
                        'value': 5,
                    },
                },
            ],
            'else': [
                {
                    'type': 'setvar',
                    'name': 'result',
                    'value': {
                        'type': 'int',
                        'value': 8,
                    },
                },
            ],
        }, vars)

        self.assertEqual(8, vars['result'].val)

    def test_instr_if_true(self):
        vars = {}

        # if true:
        #   result = 5
        # else:
        #   result = 8

        self._interp._instr({
            'type': 'if',
            'cond': {
                'type': 'bool',
                'value': True,
            },
            'code': [
                {
                    'type': 'setvar',
                    'name': 'result',
                    'value': {
                        'type': 'int',
                        'value': 5,
                    },
                },
            ],
            'else': [
                {
                    'type': 'setvar',
                    'name': 'result',
                    'value': {
                        'type': 'int',
                        'value': 8,
                    },
                },
            ],
        }, vars)

        self.assertEqual(5, vars['result'].val)

    def test_instr_insert(self):
        vars = {}

        # test1 = [3,4,5]
        # test1.insert(1, 6)

        self._interp._instrs([
            {
                'type': 'setvar',
                'name': 'test1',
                'value': {
                    'type': 'list',
                },
            },
            {
                'type': 'append',
                'target': {
                    'type': 'getvar',
                    'name': 'test1',
                },
                'value': {
                    'type': 'int',
                    'value': 3,
                },
            },
            {
                'type': 'append',
                'target': {
                    'type': 'getvar',
                    'name': 'test1',
                },
                'value': {
                    'type': 'int',
                    'value': 4,
                },
            },
            {
                'type': 'append',
                'target': {
                    'type': 'getvar',
                    'name': 'test1',
                },
                'value': {
                    'type': 'int',
                    'value': 5,
                },
            },
            {
                'type': 'insert',
                'target': {
                    'type': 'getvar',
                    'name': 'test1',
                },
                'index': {
                    'type': 'int',
                    'value': 1,
                },
                'value': {
                    'type': 'int',
                    'value': 6,
                },
            },
        ], vars)

        self.assertEqual([3,6,4,5], [x.val for x in vars['test1'].iterate()])

    def test_instr_loop(self):
        vars = {}

        # test1 = 0
        # for i in 0..10:
        #   test1 += i

        self._interp._instrs([
            {
                'type': 'setvar',
                'name': 'test1',
                'value': {
                    'type': 'int',
                    'value': 0,
                },
            },
            {
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
                        'type': 'setvar',
                        'name': 'test1',
                        'value': {
                            'type': 'add',
                            'value1': {
                                'type': 'getvar',
                                'name': 'test1',
                            },
                            'value2': {
                                'type': 'getvar',
                                'name': 'i',
                            },
                        },
                    },
                ],
            },
        ], vars)

        self.assertEqual(45, vars['test1'].val)

    def test_instr_loop_list(self):
        vars = {}

        # test1 = [3, 4]
        # test2 = 0
        # for i in test1:
        #   test2 += i

        self._interp._instrs([
            {
                'type': 'setvar',
                'name': 'test1',
                'value': {
                    'type': 'list',
                },
            },
            {
                'type': 'append',
                'target': {
                    'type': 'getvar',
                    'name': 'test1',
                },
                'value': {
                    'type': 'int',
                    'value': 3,
                },
            },
            {
                'type': 'append',
                'target': {
                    'type': 'getvar',
                    'name': 'test1',
                },
                'value': {
                    'type': 'int',
                    'value': 4,
                },
            },
            {
                'type': 'setvar',
                'name': 'test2',
                'value': {
                    'type': 'int',
                    'value': 0,
                },
            },
            {
                'type': 'loop',
                'var': 'i',
                'list': {
                    'type': 'getvar',
                    'name': 'test1',
                },
                'code': [
                    {
                        'type': 'setvar',
                        'name': 'test2',
                        'value': {
                            'type': 'add',
                            'value1': {
                                'type': 'getvar',
                                'name': 'test2',
                            },
                            'value2': {
                                'type': 'getvar',
                                'name': 'i',
                            },
                        },
                    },
                ],
            },
        ], vars)

        self.assertEqual(7, vars['test2'].val)

    def test_instr_equation(self):
        vars = {}

        # times = (((1+1)*6)/3)

        self._interp._instr({
			'type': 'setvar',
            'name': 'times',
            'value': {
                'type': 'div',
                'value1': {
                    'type': 'mul',
                    'value1': {
                        'type': 'add',
                        'value1': {
                            'type': 'int',
                            'value': 1,
                         },
                        'value2': {
                            'type': 'int',
                            'value': 1,
                        },
                    },
                    'value2': {
                        'type': 'int',
                        'value': 6,
                    },
                },
                'value2': {
                    'type': 'int',
                    'value': 3,
                },
            },
        }, vars)

        self.assertEqual(4, vars['times'].val)

    def test_instr_modset(self):
        vars = {}

        # test1 = 20
        # test1 %= 6

        self._interp._instrs([
            {
                'type': 'setvar',
                'name': 'test1',
                'value': {
                    'type': 'int',
                    'value': 20,
                },
            },
            {
                'type': 'modset',
                'target': {
                    'type': 'getvar',
                    'name': 'test1',
                },
                'value': {
                    'type': 'int',
                    'value': 6,
                },
            },
        ], vars)

        self.assertEqual(2, vars['test1'].val)

    def test_instr_mulset(self):
        vars = {}

        # test1 = 3
        # test1 *= 4

        self._interp._instrs([
            {
                'type': 'setvar',
                'name': 'test1',
                'value': {
                    'type': 'int',
                    'value': 3,
                },
            },
            {
                'type': 'mulset',
                'target': {
                    'type': 'getvar',
                    'name': 'test1',
                },
                'value': {
                    'type': 'int',
                    'value': 4,
                },
            },
        ], vars)

        self.assertEqual(12, vars['test1'].val)

    def test_instr_powset(self):
        vars = {}

        # test1 = 2
        # test1 ^= 3

        self._interp._instrs([
            {
                'type': 'setvar',
                'name': 'test1',
                'value': {
                    'type': 'int',
                    'value': 2,
                },
            },
            {
                'type': 'powset',
                'target': {
                    'type': 'getvar',
                    'name': 'test1',
                },
                'value': {
                    'type': 'int',
                    'value': 3,
                },
            },
        ], vars)

        self.assertEqual(8, vars['test1'].val)

    def test_instr_print_list(self):
        # test1 = []
        # test1.append(1)
        # test1.append(2)
        # print(test1)

        self._interp._instrs([
            {
                'type': 'setvar',
                'name': 'test1',
                'value': {
                    'type': 'list',
                },
            },
            {
                'type': 'append',
                'target': {
                    'type': 'getvar',
                    'name': 'test1',
                },
                'value': {
                    'type': 'int',
                    'value': 1,
                },
            },
            {
                'type': 'append',
                'target': {
                    'type': 'getvar',
                    'name': 'test1',
                },
                'value': {
                    'type': 'int',
                    'value': 2,
                },
            },
            {
                'type': 'print',
                'value': {
                    'type': 'getvar',
                    'name': 'test1',
                },
            },
        ], {})

        self.assertEqual('[1,2]\n', self.stdout())

    def test_instr_print_string(self):
        # test1 = "foo"
        # print(test1)

        self._interp._instrs([
            {
                'type': 'setvar',
                'name': 'test1',
                'value': {
                    'type': 'string',
                    'value': 'foo',
                },
            },
            {
                'type': 'print',
                'value': {
                    'type': 'getvar',
                    'name': 'test1',
                },
            },
        ], {})

        self.assertEqual('foo\n', self.stdout())

    def test_instr_remove(self):
        vars = {}

        # a = [3,4,5]
        # a.remove(1)

        val = self._interp._instrs([
            {
                'type': 'setvar',
                'name': 'a',
                'value': {
                    'type': 'list',
                    'values': [
                        {
                            'type': 'int',
                            'value': 3,
                        },
                        {
                            'type': 'int',
                            'value': 4,
                        },
                        {
                            'type': 'int',
                            'value': 5,
                        },
                    ],
                },
            },
            {
                'type': 'remove',
                'target': {
                    'type': 'getvar',
                    'name': 'a',
                },
                'index': {
                    'type': 'int',
                    'value': 1,
                },
            }
        ], vars)

        self.assertEqual([3, 5], [x.val for x in vars['a'].iterate()])

    def test_instr_subset(self):
        vars = {}

        # test1 = 5
        # test1 -= 2

        self._interp._instrs([
            {
                'type': 'setvar',
                'name': 'test1',
                'value': {
                    'type': 'int',
                    'value': 5,
                },
            },
            {
                'type': 'subset',
                'target': {
                    'type': 'getvar',
                    'name': 'test1',
                },
                'value': {
                    'type': 'int',
                    'value': 2,
                },
            },
        ], vars)

        self.assertEqual(3, vars['test1'].val)

    def test_instr_switch(self):
        vars = {}

        # test1 = 5
        # switch:
        # case test1 == 6:
        #   test1 *= 2
        # case test1 == 5:
        #   test1 *= 3

        self._interp._instrs([
            {
                'type': 'setvar',
                'name': 'test1',
                'value': {
                    'type': 'int',
                    'value': 5,
                },
            },
            {
                'type': 'switch',
                'cases': [
                    {
                        'cond': {
                            'type': 'equal',
                            'value1': {
                                'type': 'getvar',
                                'name': 'test1',
                            },
                            'value2': {
                                'type': 'int',
                                'value': 6,
                            },
                        },
                        'code': [
                            {
                                'type': 'setvar',
                                'name': 'test1',
                                'value': {
                                    'type': 'mul',
                                    'value1': {
                                        'type': 'getvar',
                                        'name': 'test1',
                                    },
                                    'value2': {
                                        'type': 'int',
                                        'value': 2,
                                    },
                                },
                            },
                        ],
                    },
                    {
                        'cond': {
                            'type': 'equal',
                            'value1': {
                                'type': 'getvar',
                                'name': 'test1',
                            },
                            'value2': {
                                'type': 'int',
                                'value': 5,
                            },
                        },
                        'code': [
                            {
                                'type': 'setvar',
                                'name': 'test1',
                                'value': {
                                    'type': 'mul',
                                    'value1': {
                                        'type': 'getvar',
                                        'name': 'test1',
                                    },
                                    'value2': {
                                        'type': 'int',
                                        'value': 3,
                                    },
                                },
                            },
                        ],
                    },
                ],
            },
        ], vars)

        self.assertEqual(15, vars['test1'].val)

    def test_instr_switch_default(self):
        vars = {}

        # test1 = 7
        # switch:
        # case test1 == 6:
        #   test1 *= 2
        # case test1 == 5:
        #   test1 *= 3
        # default:
        #   test1 *= 4


        self._interp._instrs([
            {
                'type': 'setvar',
                'name': 'test1',
                'value': {
                    'type': 'int',
                    'value': 7,
                },
            },
            {
                'type': 'switch',
                'cases': [
                    {
                        'cond': {
                            'type': 'equal',
                            'value1': {
                                'type': 'getvar',
                                'name': 'test1',
                            },
                            'value2': {
                                'type': 'int',
                                'value': 6,
                            },
                        },
                        'code': [
                            {
                                'type': 'setvar',
                                'name': 'test1',
                                'value': {
                                    'type': 'mul',
                                    'value1': {
                                        'type': 'getvar',
                                        'name': 'test1',
                                    },
                                    'value2': {
                                        'type': 'int',
                                        'value': 2,
                                    },
                                },
                            },
                        ],
                    },
                    {
                        'cond': {
                            'type': 'equal',
                            'value1': {
                                'type': 'getvar',
                                'name': 'test1',
                            },
                            'value2': {
                                'type': 'int',
                                'value': 5,
                            },
                        },
                        'code': [
                            {
                                'type': 'setvar',
                                'name': 'test1',
                                'value': {
                                    'type': 'mul',
                                    'value1': {
                                        'type': 'getvar',
                                        'name': 'test1',
                                    },
                                    'value2': {
                                        'type': 'int',
                                        'value': 3,
                                    },
                                },
                            },
                        ],
                    },
                ],
                'default': [
                    {
                        'type': 'setvar',
                        'name': 'test1',
                        'value': {
                            'type': 'mul',
                            'value1': {
                                'type': 'getvar',
                                'name': 'test1',
                            },
                            'value2': {
                                'type': 'int',
                                'value': 4,
                            },
                        },
                    },
                ],
            },
        ], vars)

        self.assertEqual(28, vars['test1'].val)


if __name__ == '__main__':
    unittest.main()
