#!/usr/bin/env python
from __future__ import print_function
"""
indent-context.py file-name line-number [--above N] [--below N] [--context N]

(poor man's breadcrumb context)

Output lines around line-number with paths to root in outline hierarcy.
Displaying one line for each immediate parent (less indent than current)

The lines are displayed in the format
right-indented-line-number:line-including the indent

Example output (made up for python code) for line=156, context=1:

   10:class A:
  125:    def f(self, a):
  140:        while 1:
  152:            if ...:
  155:                # above
  156:                # line to be find context for
  157:            # below
"""

TABSIZE = 4

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('filename', type=argparse.FileType(mode='r'))
parser.add_argument('linenumber', type=int)
parser.add_argument('--above', type=int, default=0)
parser.add_argument('--below', type=int, default=0)
parser.add_argument('--context', type=int, default=0)
args = parser.parse_args()
args.above = max(args.above, args.context)
args.below = max(args.below, args.context)


class Line:
    def __init__(self, linenumber, linetext):
        self.text = linetext.expandtabs(TABSIZE)
        self.number = linenumber
        self.indent = len(self.text) - len(self.text.lstrip())

    def __str__(self):
        return 'indent({0.indent}):#{0.number}:{0.text}'.format(self)


assert Line(0,'   qwe').indent == 3


outline = []  # type: List[Line]

for linenumber, linetext in enumerate(args.filename):
    line = Line(linenumber + 1, linetext.rstrip())

    # delete empty lines, and those that are indented more than the current line
    if line.number <= args.linenumber - args.above:
        while outline and not outline[-1].text:
            del outline[-1]
        if line.text:
            while outline and outline[-1].indent >= line.indent:
                del outline[-1]
    outline.append(line)
    if line.number >= args.linenumber + args.below:
        break

for line in outline:
    if line.number < args.linenumber - args.above:
        prefix = '^^'
    elif line.number == args.linenumber:
        prefix = '=>'
    else:
        prefix = '  '
    print('{} {line.number:5}: {line.text}'.format(prefix, line=line))
