#!/usr/bin/env python

import argparse
import importlib.util
import os
import pprint
import re
import sys


class ItFigures(object):

    def __init__(self, base, root):
        self.base = base
        self.root = root

    def go(self):
        print(f"Processing figures recursively starting in: {self.root}")

        rxp = '^/([^/\\\]+)/chapters/([1-9][0-9]*)/problems/([1-9][0-9]*)$'
        rcm = re.compile(rxp)

        for cur, dirs, files in os.walk(self.root):
            rel = cur[len(self.base):]
            mat = rcm.match(rel)
            if mat:
                book = mat.group(1)
                chapter = int(mat.group(2))
                problem = int(mat.group(3))
                if 'figures.py' not in files: continue
                self._process_problem(book, chapter, problem, cur)

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

        fpath = os.path.join(path, 'figures.py')
        assert(os.path.isfile(fpath))

        outpath = os.path.join(self.base,
                               'BUILD',
                               book,
                               'chapters', str(chapter),
                               'problems', str(problem))
        if not os.path.isdir(outpath): os.makedirs(outpath)
        assert(os.path.isdir(outpath))

        modname = f"figures.{book}.{chapter}.{problem}"
        spec = importlib.util.spec_from_file_location(modname, fpath)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        fig = mod.ItFigures()
        fig.go(outpath)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--book', '-b',
                        metavar='BOOK',
                        action='store',
                        dest='book',
                        required=False,
                        type=str,
                        help='Book name',)

    parser.add_argument('--chapter', '-c',
                        metavar='CHAPTER',
                        action='store',
                        dest='chapter',
                        required=False,
                        type=int,
                        help='Problem number',)

    parser.add_argument('--problem', '-p',
                        metavar='PROBLEM',
                        action='store',
                        dest='prob',
                        required=False,
                        type=int,
                        help='Problem number',)
    
    args = parser.parse_args()

    # Find our starting point.  It's the parent of the script location.
    base = os.path.realpath(os.path.join(os.path.dirname(sys.argv[0]), '..'))

    # Find our target location
    tgt = base
    if args.book:
        tgt = os.path.join(base, args.book)
        if not os.path.isdir(tgt):
            print(f"Hey Dumbass, {tgt} isn't a real place!")
            sys.exit(-1)
        if args.chapter:
            tgt = os.path.join(tgt, 'chapters', str(args.chapter))
            if not os.path.isdir(tgt):
                print(f"Hey Dumbass, {tgt} isn't a real place!")
                sys.exit(-1)
            if args.prob:
                tgt = os.path.join(tgt, 'problems', str(args.prob))
                if not os.path.isdir(tgt):
                    print(f"Hey Dumbass, {tgt} isn't a real place!")
                    sys.exit(-1)
    
    fig = ItFigures(base, tgt)
    fig.go()
