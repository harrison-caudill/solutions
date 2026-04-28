#!/usr/bin/env python

import argparse
import importlib.util
import os
import pprint
import re
import sys
import utils


class BibIt(object):

    def __init__(self, base, root):
        self.base = base
        self.root = root

    def go(self):
        print(f"Processing figures recursively starting in: {self.base}")

        rxp = '^/([^/\\\]+)/chapters/([1-9][0-9]*)/problems/([1-9][0-9]*)$'
        rcm = re.compile(rxp)

        entries = []

        # initialize with the qrf since we always have the option of
        # referencing those sources (e.g. the integral table)
        qrf = os.path.join(self.root, 'qrf', 'ref.bib')
        if os.path.isfile(qrf):
            with open(qrf, 'r') as fd:
                entries = list(fd.read().split('\n'))

        for cur, dirs, files in os.walk(self.base):
            rel = cur[len(self.base):]
            mat = rcm.match(rel)
            if mat:
                book = mat.group(1)
                chapter = int(mat.group(2))
                problem = int(mat.group(3))
                if 'ref.bib' not in files: continue
                entries += self._process_problem(book, chapter, problem, cur)

        tgt = os.path.join(self.base, 'BUILD', 'ref.bib')
        with open(tgt, 'w') as fd:
            fd.write('\n'.join(entries))

    def _annotate_declaration(self, line, chapter, problem):
        rxp = '^[^@]*@[^\{]*\{\s*(\S+).*$'
        rcm = re.compile(rxp)
        mat = rcm.match(line)
        name = mat.group(1)
        new = f"{chapter}.{problem}:{name}"
        return line.replace(name, new)

    def _process_problem(self, book, chapter, problem, path):
        blen = len(book)
        plen = (0
                + len(self.base) + blen + 1 # book path with /
                + len('chapter') + 3 + 2    # chapter with /'s
                + len('problems') + 3 + 2   # problem with /'s
                )
        print(f"  %*.*s => %*.*s %2d.%-2d" % (
            plen, plen, path,
            blen, blen, book,
            chapter, problem))

        fpath = os.path.join(path, 'ref.bib')
        assert(os.path.isfile(fpath))

        entry = []
        with open(fpath, 'r') as fd:
            raw = fd.read()
            for line in raw.split('\n'):
                if not len(line): continue
                if '@' in line and line.split()[0].startswith('@'):
                    new = self._annotate_declaration(line, chapter, problem)
                    entry.append(new)
                else:
                    entry.append(line)

        return entry


if __name__ == '__main__':
    parser = utils.PathParser()
    args = parser.parse_args()
    path = utils.Pathfinder(args)
    
    args = parser.parse_args()

    bib = BibIt(path.base(), path.tgt())
    bib.go()
