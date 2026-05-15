#!/bin/bash

for f in $(find .  -type f -name "*.tex" | grep -v jackson) ; do printf "%%%% Start of File: %s\n" "$f" ; cat $f ; printf "%%%% End of File: %s\n" "$f" ; done
