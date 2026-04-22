
import argparse
import os
import sys

class PathParser(argparse.ArgumentParser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_argument('--book', '-b',
                          metavar='BOOK',
                          action='store',
                          dest='book',
                          required=False,
                          type=str,
                          help='Book name',)

        self.add_argument('--chapter', '-c',
                          metavar='CHAPTER',
                          action='store',
                          dest='chapter',
                          required=False,
                          type=int,
                          help='Problem number',)

        self.add_argument('--problem', '-p',
                          metavar='PROBLEM',
                          action='store',
                          dest='prob',
                          required=False,
                          type=int,
                          help='Problem number',)

        self.add_argument('--qrf', '-q',
                          action='store_true',
                          dest='qrf',
                          help="Target is the book's QRF",)


class Pathfinder(object):
    def __init__(self, args):
        self.args = args

    def base(self):
        # Find our starting point.  It's the parent of the script location.
        base = os.path.join(os.path.dirname(sys.argv[0]), '..')
        return os.path.realpath(base)

    def _rel(self):
        tgt = ''
        if self.args.book:
            tgt = os.path.join(self.base(), self.args.book)
            if not os.path.isdir(tgt):
                print(f"Hey Dumbass, {tgt} isn't a real place!")
                sys.exit(-1)
            if self.args.qrf:
                return os.path.join(tgt, 'qrf')
            if self.args.chapter:
                tgt = os.path.join(tgt, 'chapters', str(self.args.chapter))
                if not os.path.isdir(tgt):
                    print(f"Hey Dumbass, {tgt} isn't a real place!")
                    sys.exit(-1)
                if self.args.prob:
                    tgt = os.path.join(tgt, 'problems', str(self.args.prob))
                    if not os.path.isdir(tgt):
                        print(f"Hey Dumbass, {tgt} isn't a real place!")
                        sys.exit(-1)

        return tgt

    def tgt(self):
        return os.path.join(self.base(), self._rel())
    
    def bld(self):
        return os.path.join(self.base(), BUILD, self._rel())
