#!/bin/bash
#USAGE: ./build_precinct_key.sh CANDIDATE COUNTY SCTYPE
if [ "$3" == 'adjacency' ]
then
  SCDIR='../data/simplicialcomplex/'
  KEYDIR='../data/adjacency/'
  OUTDIR='../results/adjacency/'
elif [ "$3" == 'vr' ]
then
  SCDIR='../data/vrcomplex/'
  KEYDIR='../data/extractcentroids/'
  OUTDIR='../results/vr/'
else
  echo "INVALID SIMPLICIAL COMPLEX TYPE "$3
  exit 1
fi

cat $SCDIR$1'/'$2'.dat' | awk '{print NR-1,$0}' | grep -e ' 0$' |cut -d' ' -f1> list.junk

cat $KEYDIR$1'/'$2'-key' |cut -d' ' -f2 > key.junk

paste key.junk list.junk|tr '\t' ' ' > $OUTDIR$1'/'$2'-key'

rm -rf *.junk
