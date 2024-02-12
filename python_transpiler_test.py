#!/usr/bin/python3

import python_transpiler
import unittest

class TestPythonTranspile(unittest.TestCase):
    def setUp(self):
        self.pt = python_transpiler.PythonTranspiler()

    def test_print_float(self):
        ret = self.pt.instrs([
            {
                'type': 'print',
                'value': {
                    'type': 'float',
                    'value': 5.2,
                },
            },
        ])

        self.assertEqual('print(5.2)\n', ret)

    def test_print_int(self):
        ret = self.pt.instrs([
            {
                'type': 'print',
                'value': {
                    'type': 'int',
                    'value': 5,
                },
            },
        ])

        self.assertEqual('print(5)\n', ret)

    def test_print_string(self):
        ret = self.pt.instrs([
            {
                'type': 'print',
                'value': {
                    'type': 'string',
                    'value': 'foo',
                },
            },
        ])

        self.assertEqual("print('foo')\n", ret)


if __name__ == '__main__':
    unittest.main()
