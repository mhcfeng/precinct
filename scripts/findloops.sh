#!/bin/bash
#USAGE: ./findloops.sh CANDIDATE COUNTY TYPE
if [ "$3" == 'adjacency' ]; then
  INDIR="../results/adjacency/"
  SCDIR="../data/simplicialcomplex/"
elif [ "$3" == 'vr' ]; then
  INDIR="../results/vr/"
  SCDIR="../data/vrcomplex/"
fi

NUMHOLES=$(grep -e '^1,' $INDIR$1'/'$2'.csv' |wc -l |sed 's/^[ ]*//g' | cut -d' ' -f1)

if [ $((NUMHOLES)) -gt 0 ]
then
  grep -e '^1,' $INDIR$1'/'$2'.csv' | cut -d',' -f4 > junk.loops
  while IFS= read line
  do
    cat $SCDIR$1'/'$2'.dat' | awk '{print NR-1,$0}' > junk.0
    LISTSC=$(echo $line | sed 's/ $//g' | tr ' ' '\n')
    for SC in $LISTSC
    do
      grep -e "^$SC " junk.0 | cut -d' ' -f3,4 >> junk.vertices
    done

    cat junk.vertices | tr '\n' ' ' >> junk.1
    echo >> junk.1
    rm -f junk.vertices
  done < junk.loops

  rm -f junk.0

  cat $INDIR$1'/'$2"-key" | sed 's/\([^ ]*\) \([^ ]*\)/s%^\2 %\1 %g/' > sed.script
  cat $INDIR$1'/'$2"-key" | sed 's/\([^ ]*\) \([^ ]*\)/s% \2 % \1 %g/' >> sed.script
  sed -f sed.script junk.1 > junk.replace
  sed -f sed.script junk.replace > $INDIR$1'/'$2'-loops'
  rm -f junk.1
  rm -f sed.script
  rm -f junk.*
fi
