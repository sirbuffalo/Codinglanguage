#!/usr/bin/python3

import difflib
import glob
import io
import sys
from interpreter import Interpreter
from parser import Parser

stdoutbuf = io.StringIO()
sys.stdout = stdoutbuf

for filename in glob.glob('tests/*.🔥🦬'):
    print(f'{filename}: ', end='', file=sys.stderr)
    parsed = Parser(filename).parse()
    interp = Interpreter(parsed)
    interp.run()

    actual = stdoutbuf.getvalue()
    stdoutbuf.truncate(0)
    stdoutbuf.seek(0)

    expected = open(f'{filename}.expected').read()

    if actual != expected:
        print(f'DIFF', file=sys.stderr)
        diff = difflib.unified_diff(
            actual.splitlines(keepends=True),
            expected.splitlines(keepends=True),
            fromfile='actual',
            tofile='expected',
        )
        sys.stderr.writelines(diff)
    else:
        print(f'OK', file=sys.stderr)