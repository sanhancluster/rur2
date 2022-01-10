#!/bin/bash

FILES='io/io_hm.f90'
F2PY=f2py
FORT=gfortran
BASEDIR=$(dirname "$0")

cd $BASEDIR/rur2
for f in $FILES
do
    bn=$(basename "$f" .f90)
    fn=$(basename "$f")
    dir=$(dirname "$f")
    cd $dir
    $FORT -x f95-cpp-input -c $fn
    $F2PY -c --f90exec=$FORT $fn -m $bn --opt='-O3 -x f95-cpp-input'
    cd $BASEDIR
done
rm *.o *.mod