#!/usr/bin/python3

import glob
from parser import Parser
from interpreter import Interpreter

for filename in glob.glob('tests/*.🔥🦬'):
    print(f'--- {filename} ---')
    parsed = Parser(filename).parse()
    interp = Interpreter(parsed)
    interp.run()
