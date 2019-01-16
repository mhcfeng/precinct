#!/bin/bash

Datafile='../full-list'

for COUNTY in $(cat $Datafile); do
  ./workflow.sh hill $COUNTY vr
  ./workflow.sh trump $COUNTY vr
done
