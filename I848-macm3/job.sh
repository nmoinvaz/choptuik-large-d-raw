#!/bin/bash
# job.sh NAME : one circle of #812's kf 47 count on the second layout, one thread
. /Users/nathan/Source/choptuik-large-d-raw-749/I848-macm3/common.sh
case $1 in
  c_2.85_p0.25) C=2.85,0.25,0.36 ;;
  c_3.35_p0.25) C=3.35,0.25,0.36 ;;
  c_2.85_m0.25) C=2.85,-0.25,0.36 ;;
  c_3.35_m0.25) C=3.35,-0.25,0.36 ;;
  triple) C=2.905,0,0.24 ;;
  lens) C=3.16186,0.14008,0.05 ;;
  lensc) C=3.16186,-0.14008,0.05 ;;
  *) echo "job.sh: unknown circle $1" >&2; exit 9 ;;
esac
go $1 $C 1
