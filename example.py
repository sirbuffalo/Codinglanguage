#!/usr/bin/python3

# example parse
parse = [
    # setting times to 10
    {
        'type': 'set var',
        'name': 'times',
        'value': {
            'type': 'int',
            'value': 10
        }
    },
    # looping 1 - 11 times
    {
        'type': 'loop',
        'var':  'index',
        'list': {
            'type': 'range',
            'start': {
                'type': 'int',
                'value': 1
            },
            'end': {
                'type': 'add',
                'value1': {
                    'type': 'int',
                    'value': 1
                },
                'value2': {
                    'type': 'get var',
                    'name': 'times'
                }
            }
        },
        # print index
        'code': [
            {
                'type': 'print',
                'value': {
                    'type': 'get var',
                    'name': 'index'
                }
            }
        ]
    }
]

import interpreter
interp = interpreter.Interpreter(parse)
interp.run()
