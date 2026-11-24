#!/bin/bash
# #1025 macm3 kc87_leg_lambda: copy the pinned inputs from raw commits (git cat-file, exact bytes) and check each blob (git hash-object --no-filters).
# usage: bash prepare87.sh DNAME   (DNAME/point.env: D TAG RAWC STATEFILE STATEBLOB RECBLOB). Writes common/in/ (once), DNAME/in/ and DNAME/pins.txt. Exit 1 on any mismatch.
L=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda
RAWG=$HOME/Source/choptuik-large-d-raw-1076p
DN=$1; OUT=$L/$DN
. $OUT/point.env
mkdir -p $OUT/in $L/common/in
rc=0
: > $OUT/pins.txt
pin() {  # path-in-raw blob8 destination commit
  git -C $RAWG cat-file blob $4:$1 > $3 || { echo "cannot read $4:$1" | tee -a $OUT/pins.txt; rc=1; return; }
  got=$(git hash-object --no-filters $3 | cut -c1-8)
  [ "$got" = "$2" ] && s=ok || { s="MISMATCH (wanted $2)"; rc=1; }
  echo "$got  $(basename $3)  <- $4:$1  $s" | tee -a $OUT/pins.txt
}
C=8e4797ff   # the scripts of the earlier #1025 tasks (raw)
C3=ec9fb489  # dh610's k_c 87 check
CR=$(git -C $RAWG rev-parse --short=8 origin/main)   # repeat_check.py (dh610's), unchanged since its commit
pin I1025-dh610/kc87_d195/in/kc87_syscheck_1025.py 6df5d960 $L/common/in/kc87_syscheck_1025.py $C3
pin I1025-win/kc79_d19/kc79_syscheck_1025.py 29dce7ea $L/common/in/kc79_syscheck_1025.py $C
pin I1025-dh170/kc_break/d18_hybsign.py e089207a $L/common/in/d18_hybsign.py $C
pin I1025-dh170/lower_root/read_lower.py 89309d3c $L/common/in/read_lower.py $C
pin I1025-mac/d18/d185_scan_read.py 7c9d400f $L/common/in/d185_scan_read.py $C
pin I1025-dh610/kc71_d19125/in/repeat_check.py aaf598a9 $L/common/in/repeat_check.py $CR
pin I1025-dh370/kc87_leg/$STATEFILE $STATEBLOB $OUT/in/$STATEFILE $RAWC
pin I1025-dh370/kc87_leg/$TAG.jsonl $RECBLOB $OUT/in/$TAG.jsonl $RAWC
exit $rc
