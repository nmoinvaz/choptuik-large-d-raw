#!/bin/bash
# job.sh K NAME : one circle of the box at cut K, one thread (#708's job.sh)
. /Users/nathan/Source/choptuik-large-d-raw-749/I749-macm3/common.sh
K=$1; N=$2
case $N in
  control) C=2.043532530673195,0,0.2 ;;
  c_2.85_p0.25) C=2.85,0.25,0.36 ;;
  c_3.35_p0.25) C=3.35,0.25,0.36 ;;
  c_2.85_m0.25) C=2.85,-0.25,0.36 ;;
  c_3.35_m0.25) C=3.35,-0.25,0.36 ;;
  *) echo "job.sh: unknown circle $N" >&2; exit 9 ;;
esac
[ $N = control ] || wait_state $K
go $K $N $C 1
