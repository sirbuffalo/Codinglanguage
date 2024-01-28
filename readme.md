    times = 10
    for index of [1...times + 1]
        print(index)
Here is a example parse for the code above

    [
        # setting times to 10
        {
            'type': 'setvar',
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
                    'num1': {
                        'type': 'int',
                        'value': 1
                    },
                    'num2': {
                        'type': 'getvar',
                        'name': 'times'
                    }
                }
            },
            # print index
            'code': [
                {
                    'type': 'print',
                    'value': {
                        'type': 'getvar',
                        'name': 'index'
                    }
                }
            ]
        }
    ]
