from math import ceil
from glob import glob


class Parser:
    def __init__(self, codetext, indent='    '):
        self.codetext = codetext
        self.indent = indent
        self.parsed = None

    def parse(self):
        self.parsed = []
        for line in self.codetext.split('\n'):
            indention = 0
            for _ in range(ceil(len(line) / len(self.indent)-1)):
                if line[indention * len(self.indent):(indention + 1) * len(self.indent)] != self.indent:
                    break
                indention += 1
            line = line[indention * len(self.indent):]
        return self.parsed


for file in glob('*.🐮🦬'):
    print(Parser(open(file).read()).parse())
