#!/usr/bin/env python

import argparse
from dataclasses import dataclass
import os
import pprint
import shutil
import subprocess
import sys
import tempfile


class Converter(object):

    def __init__(self, src, dst, dpi, qcad,
                 overwrite=False,
                 linewidth=7.5,
                 inc_src_base=True):
        self.src = self._canonicalize(src)
        self.dst = self._canonicalize(dst)
        self.dpi = dpi
        self.qcad = self._canonicalize(qcad)
        self.overwrite = overwrite
        self.linewidth = linewidth
        self.inc_src_base = inc_src_base

    def convert(self, parent, fname):
        srcpath = os.path.join(parent, fname)
        assert(srcpath.startswith(self.src))

        relpath = srcpath[len(self.src)+1:]
        if self.inc_src_base:
            relpath = os.path.join(os.path.basename(self.src), relpath)

        dstpath = relpath[:-4] + '.png'
        dstpath = os.path.join(self.dst, dstpath)
        dstpath = os.path.realpath(dstpath)

        extant = os.path.isfile(dstpath)
        if extant and self.overwrite:
            print(f'  Overwriting: {relpath}')
        elif extant and not self.overwrite:
            print(f'  Skipping: {relpath}')
            return
        else:
            print(f'  Converting: {relpath}')

        dstdir = os.path.dirname(dstpath)
        if not os.path.isdir(dstdir): os.makedirs(dstdir)

        tmpfile = tempfile.NamedTemporaryFile(suffix='.png')
        tmppath = tmpfile.name

        binpath = os.path.join(self.qcad, 'dwg2bmp')
        cmd = [binpath,
               '-b', 'white',
               '-o', tmppath,
               '-r', str(self.dpi),
               '-no-gui',
               '-c',
               '-force',
               srcpath]
        subprocess.call(cmd)

        cmd = ['identify',
               '-format', '%w',
               tmppath]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        width = int(res.stdout.strip())

        max_width = int(self.dpi * self.linewidth)

        if width > max_width:
            print("Resizing")
            cmd = ['magick', 'convert',
                   '-resize', f'{max_width}x',
                   tmppath, dstpath]
            subprocess.call(cmd)
        else:
            print("Copying")
            shutil.copy(tmppath, dstpath)

    def walk(self):
        print(f"Walking {self.src} => {self.dst}")
        for parent, dirs, files in os.walk(top=self.src):
            for f in files:
                if f.endswith('.dxf'): self.convert(parent, f)

    def _canonicalize(self, path):
        if path.startswith('/'):
            return os.path.realpath(path)
        else:
            base = os.path.dirname(sys.argv[0])
            base = os.getcwd()
            return os.path.realpath(os.path.join(base, path))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--source-dir', '-s',
                        metavar='SRC_DIR',
                        action='store',
                        dest='src_dir',
                        required=False,
                        default='.',
                        type=str,
                        help='Source directory',)

    parser.add_argument('--dst-dir', '-d',
                        metavar='DST_DIR',
                        action='store',
                        dest='dst_dir',
                        required=False,
                        default='BUILD',
                        type=str,
                        help='Destination directory',)

    parser.add_argument('--dpi', '-D',
                        metavar='DPI',
                        action='store',
                        dest='dpi',
                        required=False,
                        default=300,
                        type=int,
                        help='DPI for the export',)
    
    parser.add_argument('--qcad-bin-dir', '-Q',
                        metavar='QCAD_BINS',
                        action='store',
                        dest='qcad_bins',
                        required=False,
                        default='/Applications/QCAD-Pro.app/Contents/Resources',
                        type=str,
                        help='File with the episode names',)

    parser.add_argument('--linewidth', '-L',
                        metavar='LINEWIDTH',
                        action='store',
                        dest='linewidth',
                        required=False,
                        default=7.5,
                        type=float,
                        help='Width (in inches to match dpi) of the content',)

    parser.add_argument('--overwrite', '-o',
                        action='store_true',
                        dest='overwrite',
                        help='Overwrite any files already generated',)

    parser.add_argument('--exclude-src-base', '-E',
                        action='store_true',
                        dest='exc_src_base',
                        help='Exclude the basename of the src directory in relative path in output',)


    args = parser.parse_args()

    c = Converter(src=args.src_dir,
                  dst=args.dst_dir,
                  dpi=args.dpi,
                  qcad=args.qcad_bins,
                  overwrite=args.overwrite,
                  linewidth=args.linewidth,
                  inc_src_base=(not args.exc_src_base))
    c.walk()
