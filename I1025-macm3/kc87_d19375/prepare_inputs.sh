#!/bin/bash
# #1025 macm3b kc87_d19375: copy the pinned inputs from raw commits (git cat-file, exact bytes; the push worktree's files can drift) into in/ and check each blob
# (git hash-object --no-filters). Writes pins.txt. Exit 1 on any mismatch.
RAWG=$HOME/Source/choptuik-large-d-raw-749p
OUT=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_d19375
C=8e4797ff    # the scripts (as kc79_d19375)
C2=98796643   # my k_c 79 D 19.375 state and record (the scan commit of kc79_d19375)
C3=ec9fb489   # dh610's k_c 87 check and its diff
rc=0
: > $OUT/pins.txt
pin() {  # path-in-raw blob8 name-in-in/ [commit]
  CC=${4:-$C}
  git -C $RAWG cat-file blob $CC:$1 > $OUT/in/$3 || { echo "cannot read $CC:$1"; rc=1; return; }
  got=$(git hash-object --no-filters $OUT/in/$3 | cut -c1-8)
  [ "$got" = "$2" ] && s=ok || { s="MISMATCH (wanted $2)"; rc=1; }
  echo "$got  $3  <- $CC:$1  $s" | tee -a $OUT/pins.txt
}
pin I1025-macm3/kc79_d19375/sol_l1kc79macm3d19375_D19.3750.npy d5ef91f3 sol_l1kc79macm3d19375_D19.3750.npy $C2
pin I1025-macm3/kc79_d19375/l1kc79macm3d19375.jsonl a7c1addb l1kc79macm3d19375.jsonl $C2
pin I1025-dh610/kc87_d195/in/kc87_syscheck_1025.py 6df5d960 kc87_syscheck_1025.py $C3
pin I1025-dh610/kc87_d195/kc87_syscheck_1025.diff dfb42ff7 kc87_syscheck_1025.diff.dh610 $C3
pin I1025-win/kc79_d19/kc79_syscheck_1025.py 29dce7ea kc79_syscheck_1025.py
pin I1025-dh170/kc_break/d18_hybsign.py e089207a d18_hybsign.py
pin I1025-dh170/lower_root/read_lower.py 89309d3c read_lower.py
pin I1025-mac/d18/d185_scan_read.py 7c9d400f d185_scan_read.py
exit $rc
