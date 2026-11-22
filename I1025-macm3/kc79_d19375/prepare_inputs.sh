#!/bin/bash
# #1025 macm3b kc79_d19375: copy the pinned inputs from raw commit 8e4797ff (git cat-file, exact bytes; the push worktree's files can drift) into in/ and check each blob
# (git hash-object --no-filters). Writes pins.txt. Exit 1 on any mismatch.
RAWG=$HOME/Source/choptuik-large-d-raw-749p
OUT=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc79_d19375
C=8e4797ff   # the scripts; the state and the record come from C2
C2=1845c479
rc=0
: > $OUT/pins.txt
pin() {  # path-in-raw blob8 name-in-in/ [commit]
  CC=${4:-$C}
  git -C $RAWG cat-file blob $CC:$1 > $OUT/in/$3 || { echo "cannot read $CC:$1"; rc=1; return; }
  got=$(git hash-object --no-filters $OUT/in/$3 | cut -c1-8)
  [ "$got" = "$2" ] && s=ok || { s="MISMATCH (wanted $2)"; rc=1; }
  echo "$got  $3  <- $CC:$1  $s" | tee -a $OUT/pins.txt
}
pin I1025-win2/kc71_leap/states/sol_l1kc71Lw1025b_D19.375000.npy e883864a sol_l1kc71Lw1025b_D19.375000.npy $C2
pin I1025-win2/kc71_leap/states/l1kc71Lw1025b.jsonl 9659eac3 l1kc71Lw1025b.jsonl $C2
pin I1025-win2/kc71_d185/kc71_syscheck.py 4cd86cd4 kc71_syscheck.py
pin I1025-win/kc79_d19/kc79_syscheck_1025.py 29dce7ea kc79_syscheck_1025.py
pin I1025-dh170/kc_break/d18_hybsign.py e089207a d18_hybsign.py
pin I1025-dh170/lower_root/read_lower.py 89309d3c read_lower.py
pin I1025-mac/d18/d185_scan_read.py 7c9d400f d185_scan_read.py
exit $rc
