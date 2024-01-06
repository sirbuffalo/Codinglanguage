#!/usr/bin/python3

import interpreter
import unittest

class TestInterpreter(unittest.TestCase):
    def setUp(self):
        self._interp = interpreter.Interpreter([])

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

    def test_expr_get_var(self):
        # test1

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

    def test_expr_join(self):
        vars = {}

        # test1 = ["foo", "bar"]
        # test2 = test1.join("X")

        res = self._interp._instrs([
            {
                'type': 'set var',
                'name': 'test1',
                'value': {
                    'type': 'list',
                },
            },
            {
                'type': 'append',
                'target': {
                    'type': 'get var',
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
                    'type': 'get var',
                    'name': 'test1',
                },
                'value': {
                    'type': 'string',
                    'value': 'bar',
                },
            },
            {
                'type': 'set var',
                'name': 'test2',
                'value': {
                    'type': 'join',
                    'target': {
                        'type': 'get var',
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

    def test_expr_len(self):
        vars = {}

        # test1 = [3,4]
        # test2 = test.len()

        self._interp._instrs([
            {
                'type': 'set var',
                'name': 'test1',
                'value': {
                    'type': 'list',
                },
            },
            {
                'type': 'append',
                'target': {
                    'type': 'get var',
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
                    'type': 'get var',
                    'name': 'test1',
                },
                'value': {
                    'type': 'int',
                    'value': 4,
                },
            },
            {
                'type': 'set var',
                'name': 'test2',
                'value': {
                    'type': 'len',
                    'target': {
                        'type': 'get var',
                        'name': 'test1',
                    },
                },
            },
        ], vars)

        self.assertEqual(2, vars['test2'].val)

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
                'type': 'set var',
                'name': 'test1',
                'value': {
                    'type': 'list',
                },
            },
            {
                'type': 'append',
                'target': {
                    'type': 'get var',
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
                    'type': 'get var',
                    'name': 'test1',
                },
                'value': {
                    'type': 'int',
                    'value': 2,
                },
            },
            {
                'type': 'set var',
                'name': 'test2',
                'value': {
                    'type': 'subscript',
                    'target': {
                        'type': 'get var',
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

    def test_expr_subscript_string(self):
        vars = {}

        # test1 = "bar"
        # test2 = test[1]

        self._interp._instrs([
            {
                'type': 'set var',
                'name': 'test1',
                'value': {
                    'type': 'string',
                    'value': 'bar',
                },
            },
            {
                'type': 'set var',
                'name': 'test2',
                'value': {
                    'type': 'subscript',
                    'target': {
                        'type': 'get var',
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

    def test_instr_append(self):
        vars = {}

        # test1 = []
        # test1.append(1)
        # test1.append(2)

        self._interp._instrs([
            {
                'type': 'set var',
                'name': 'test1',
                'value': {
                    'type': 'list',
                },
            },
            {
                'type': 'append',
                'target': {
                    'type': 'get var',
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
                    'type': 'get var',
                    'name': 'test1',
                },
                'value': {
                    'type': 'int',
                    'value': 2,
                },
            },
        ], vars)

        self.assertEqual([1, 2], [x.val for x in vars['test1'].val])

    def test_instr_if_equal_true(self):
        vars = {}

        # test1 = 5
        # if test1 == 5:
        #   test1 *= 2

        self._interp._instrs([
            {
                'type': 'set var',
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
                        'type': 'get var',
                        'name': 'test1',
                    },
                    'value2': {
                        'type': 'int',
                        'value': 5,
                    },
                },
                'code': [
                    {
                        'type': 'set var',
                        'name': 'test1',
                        'value': {
                            'type': 'mul',
                            'value1': {
                                'type': 'get var',
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
                    'type': 'set var',
                    'name': 'result',
                    'value': {
                        'type': 'int',
                        'value': 5,
                    },
                },
            ],
            'else': [
                {
                    'type': 'set var',
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
                    'type': 'set var',
                    'name': 'result',
                    'value': {
                        'type': 'int',
                        'value': 5,
                    },
                },
            ],
            'else': [
                {
                    'type': 'set var',
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
                'type': 'set var',
                'name': 'test1',
                'value': {
                    'type': 'list',
                },
            },
            {
                'type': 'append',
                'target': {
                    'type': 'get var',
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
                    'type': 'get var',
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
                    'type': 'get var',
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
                    'type': 'get var',
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
                'type': 'set var',
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
                        'type': 'set var',
                        'name': 'test1',
                        'value': {
                            'type': 'add',
                            'value1': {
                                'type': 'get var',
                                'name': 'test1',
                            },
                            'value2': {
                                'type': 'get var',
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
                'type': 'set var',
                'name': 'test1',
                'value': {
                    'type': 'list',
                },
            },
            {
                'type': 'append',
                'target': {
                    'type': 'get var',
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
                    'type': 'get var',
                    'name': 'test1',
                },
                'value': {
                    'type': 'int',
                    'value': 4,
                },
            },
            {
                'type': 'set var',
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
                    'type': 'get var',
                    'name': 'test1',
                },
                'code': [
                    {
                        'type': 'set var',
                        'name': 'test2',
                        'value': {
                            'type': 'add',
                            'value1': {
                                'type': 'get var',
                                'name': 'test2',
                            },
                            'value2': {
                                'type': 'get var',
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
			'type': 'set var',
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

    def test_instr_print_list(self):
        # test1 = []
        # test1.append(1)
        # test1.append(2)
        # print(test1)

        self._interp._instrs([
            {
                'type': 'set var',
                'name': 'test1',
                'value': {
                    'type': 'list',
                },
            },
            {
                'type': 'append',
                'target': {
                    'type': 'get var',
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
                    'type': 'get var',
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
                    'type': 'get var',
                    'name': 'test1',
                },
            },
        ], {})

    def test_instr_print_string(self):
        # test1 = "foo"
        # print(test1)

        self._interp._instrs([
            {
                'type': 'set var',
                'name': 'test1',
                'value': {
                    'type': 'string',
                    'value': 'foo',
                },
            },
            {
                'type': 'print',
                'value': {
                    'type': 'get var',
                    'name': 'test1',
                },
            },
        ], {})


if __name__ == '__main__':
    unittest.main()
