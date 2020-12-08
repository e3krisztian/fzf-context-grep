#!/usr/bin/env python
from __future__ import print_function
"""
hgrep.py regexp file-name

(poor man's breadcrumb context)

Output matching lines with paths to root in outline hierarcy.
Displaying one line for each immediate parent (less indent than current)

The lines are displayed in the format
right-indented-line-number:line-including the indent

Example output (made up for python code):

   10:class A:
  125:    def f(self, a):
  140:        while 1:
  152:            if ...:
  156:                # line to be find context for
"""

TABSIZE = 4

import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('re', type=re.compile)
parser.add_argument('sourcefile', type=argparse.FileType(mode='r'))
args = parser.parse_args()


class Line:
    def __init__(self, linenumber, linetext):
        self.text = linetext.expandtabs(TABSIZE)
        self.number = linenumber
        self.indent = len(self.text) - len(self.text.lstrip())

    def __str__(self):
        return 'indent({0.indent}):#{0.number}:{0.text}'.format(self)


assert Line(0,'   qwe').indent == 3


outline = []  # type: List[Line]


def print_match():
    for line in outline[:-1]:
        print('  {line.number:5}: {line.text}'.format(line=line))
    print('X {line.number:5}: {line.text}'.format(line=outline[-1]))
    del outline[:]
    # print()


for linenumber, linetext in enumerate(args.sourcefile):
    line = Line(linenumber + 1, linetext.rstrip())

    # delete empty lines, and those that are indented more than the current line
    while outline and not outline[-1].text:
        del outline[-1]
    if line.text:
        while outline and outline[-1].indent >= line.indent:
            del outline[-1]
    outline.append(line)

    if args.re.search(line.text):
        print_match()
