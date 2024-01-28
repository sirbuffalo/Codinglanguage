import sys
from glob import glob
from parser import Parser
from interpreter import Interpreter
import subprocess


if len(sys.argv) >= 2:
    if sys.argv[1].endswith('.🐮🦬') or sys.argv[1].endswith('.🦬🐮') or sys.argv[1].endswith('.🔥🦬') or sys.argv[1].endswith('.cb') or sys.argv[1].endswith('.fb'):
        parsed_dict = Parser(sys.argv[1]).parse()
        print(f'{sys.argv[1]}:    {parsed_dict}\n')
        interp = Interpreter(parsed_dict)
        interp.run()
    elif sys.argv[1].endswith('.py'):
        subprocess.run(['python', sys.argv[1]])
else:
    files = []
    files.extend(glob('*.🐮🦬'))
    files.extend(glob('*.🦬🐮'))
    files.extend(glob('*.🔥🦬'))
    files.extend(glob('*.cb'))
    files.extend(glob('*.fb'))
    for file in files:
        parsed_dict = Parser(file).parse()
        print(f'{file}:    {parsed_dict}\n')
        interp = Interpreter(parsed_dict)
        interp.run()
