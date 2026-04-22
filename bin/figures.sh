#!/bin/bash

# Find our build/base path
BASE=$(dirname $(dirname $0))
echo $BASE | grep -q ^/
if [ $? -ne 0 ] ; then
    base=$(dirname ${PWD}/${base})
fi
build=${base}/BUILD

# find our target
tgt=
if [ -d $1 ] ; then
    # We're building a single problem
    if [ -f $1/figures.py ] ; then
        pushd $1
        python figures.py
        popd
    fi
else
    for f in $(find . -type f -name "figures.py") ; do
        pushd $(dirname $f)
        python figures.py
        popd
    done
fi
