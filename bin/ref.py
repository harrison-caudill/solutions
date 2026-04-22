#!/usr/bin/env python

import argparse
import importlib.util
import os
import pprint
import re
import sys


class BibIt(object):

    def __init__(self, base, root):
        self.base = base
        self.root = root

    def go(self):
        print(f"Processing figures recursively starting in: {self.base}")

        rxp = '^/([^/\\\]+)/chapters/([1-9][0-9]*)/problems/([1-9][0-9]*)$'
        rcm = re.compile(rxp)

        entries = []

        for cur, dirs, files in os.walk(self.base):
            rel = cur[len(self.base):]
            mat = rcm.match(rel)
            if mat:
                book = mat.group(1)
                chapter = int(mat.group(2))
                problem = int(mat.group(3))
                if 'ref.bib' not in files: continue
                entries += self._process_problem(book, chapter, problem, cur)

        tgt = os.path.join(base, 'BUILD', 'ref.bib')
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
                if '@' in line and line.split()[0].startswith('@'):
                    new = self._annotate_declaration(line, chapter, problem)
                    entry.append(new)
                else:
                    entry.append(line)

        return entry


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

    # Find our walking start location
    root = base
    if args.book:
        root = os.path.join(base, args.book)
        if not os.path.isdir(root):
            print(f"Hey Dumbass, {root} isn't a real place!")
            sys.exit(-1)
        if args.chapter:
            root = os.path.join(root, 'chapters', str(args.chapter))
            if not os.path.isdir(root):
                print(f"Hey Dumbass, {root} isn't a real place!")
                sys.exit(-1)
            if args.prob:
                root = os.path.join(root, 'problems', str(args.prob))
                if not os.path.isdir(root):
                    print(f"Hey Dumbass, {root} isn't a real place!")
                    sys.exit(-1)

    bib = BibIt(base, root)
    bib.go()
