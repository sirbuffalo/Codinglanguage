#!/usr/bin/python3

import difflib
import glob
import io
import os.path
import sys
from interpreter import Interpreter
from parser import Parser

for filename in glob.glob('tests/*.🔥🦬'):
    stdinbuf = io.StringIO()
    stdoutbuf = io.StringIO()
    sys.stdin = stdinbuf
    sys.stdout = stdoutbuf

    print(f'{filename}: ', end='', file=sys.stderr)

    if os.path.exists(f'{filename}.input'):
        inp = open(f'{filename}.input').read()
        stdinbuf.write(inp)
        stdinbuf.seek(0)

    try:
        parsed = Parser(filename).parse()
        interp = Interpreter(parsed)
        interp.run()
    except Exception as e:
        print(f'ERROR: {e}', file=sys.stderr)
        continue

    actual = stdoutbuf.getvalue()

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
