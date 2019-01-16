#!/bin/bash
#USAGE: ./workflow.sh CANDIDATE COUNTY SCTYPE
echo $2
echo "Building Simplicial Complexes"
if [ "$3" == 'adjacency' ]; then
  ./process_neighbors.sh $2
  python build_adjacency.py $2 $1
elif [ "$3" == 'vr' ]; then
  ./process_centroids.sh $2
  python gen_alph.py $2 $1
else
  echo "Invalid SCTYPE: "$3
  exit 1
fi
echo "Computing PH"
./../phat/simple_example $2 $1 $3


echo "Building Keys"
./build_precinct_key.sh $1 $2 $3
echo "Finding Loops"
./findloops.sh $1 $2 $3
echo "Converting Loops to Centroids"
./get_loop_coords.sh $1 $2 $3
