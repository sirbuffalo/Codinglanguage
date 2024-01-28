#!/usr/bin/python3

import argparse
from parser import Parser
from interpreter import Interpreter

endings = {
    '🐮🦬',
    '🐮',
    '🔥🦬',
    'cb',
    'fb',
}

ap = argparse.ArgumentParser()
ap.add_argument('-p', '--parsed', action='store_true', help='Print parse tree')
ap.add_argument('filename', nargs='+')
args = ap.parse_args()

for filename in args.filename:
    parsed = Parser(filename).parse()
    if args.parsed:
        print(f'{filename}: {parsed}')
    interp = Interpreter(parsed)
    interp.run()
