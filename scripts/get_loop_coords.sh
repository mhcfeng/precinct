#!/bin/bash
#USAGE: ./get_loop_coords.sh CANDIDATE COUNTY SCTYPE

if [ "$3" == 'adjacency' ]
then
  LOOPSDIR="../results/adjacency/"
  CENTROIDDIR="../data/extractcentroids/"
  OUTDIR="../results/adjacency/"
elif [ "$3" == 'vr' ]; then
  LOOPSDIR="../results/vr/"
  CENTROIDDIR="../data/extractcentroids/"
  OUTDIR="../results/vr/"
fi
I=$((1))
echo "oid;Line" > $OUTDIR$1'/'$2'-loops.txt'

while read LOOP
do
  echo $LOOP | sed 's/\([^ ]*\) \([^ ]*\) /\1 \2\'$'\n/g' > junk.lines
  while read LINE
  do
    BEGIN=$(echo $LINE | cut -d' ' -f1)
    BEGINCOORD=$(grep $BEGIN $CENTROIDDIR$2'.csv' | cut -d',' -f1,2 | tr ',' ' ')
    END=$(echo $LINE | cut -d' ' -f2)
    ENDCOORD=$(grep $END $CENTROIDDIR$2'.csv' | cut -d',' -f1,2 | tr ',' ' ')
    echo $I";LINESTRING("$BEGINCOORD", "$ENDCOORD")" >> $OUTDIR$1'/'$2'-loops.txt'
  done < junk.lines
  I=$((I+1))
done < $LOOPSDIR$1'/'$2'-loops'
