#!/bin/bash

echo "\\documentclass{article}"
echo "\\usepackage{hyperref}"
echo "\\input{packages}"
echo "\\input{preamble}"
echo "\\input{commands}"
echo "\\begin{document}"

for ((i=1;i<37;i++)) ; do
    echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
    echo "%% Problem ${i}"
    echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"    
    f="sakurai/chapters/1/problems/${i}/problem.tex"
    start=$(grep -n \\\\begin\{purpose\} $f | awk -F: '{print $1}')
    echo "\\section{Problem ${i}}"
    if [ -z ${start} ] ; then
        echo "Problem ${i} Lacks Purpose!"
    else
        end=$(grep -n \\\\end\{purpose\} $f | awk -F: '{print $1}')
        sed -n "$((${start}+1)),$((${end}-1))p" $f
    fi
    echo
    echo
done
         
echo "\\end{document}"
