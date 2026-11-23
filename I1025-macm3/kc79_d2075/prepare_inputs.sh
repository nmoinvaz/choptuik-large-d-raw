#!/bin/bash
# #1025 macm3b kc79_d2075: copy the pinned inputs from raw commits (git cat-file, exact bytes) into in/ and check each blob (git hash-object --no-filters). Writes pins.txt. Exit 1 on any mismatch.
RAWG=$HOME/Source/choptuik-large-d-raw-1076p
OUT=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc79_d2075
C=8e4797ff    # the scripts (as kc79_d19375, kc87_d1975)
C2=60d75f9f   # win2's accepted k_c 79 D 20.75 state and record (raw I1025-win2/kc79_leap/)
mkdir -p $OUT/in
rc=0
: > $OUT/pins.txt
pin() {  # path-in-raw blob8 name-in-in/ [commit]
  CC=${4:-$C}
  git -C $RAWG cat-file blob $CC:$1 > $OUT/in/$3 || { echo "cannot read $CC:$1"; rc=1; return; }
  got=$(git hash-object --no-filters $OUT/in/$3 | cut -c1-8)
  [ "$got" = "$2" ] && s=ok || { s="MISMATCH (wanted $2)"; rc=1; }
  echo "$got  $3  <- $CC:$1  $s" | tee -a $OUT/pins.txt
}
pin I1025-win2/kc79_leap/sol_l1kc79win2d2075_D20.7500.npy 1368e4ac sol_l1kc79win2d2075_D20.7500.npy $C2
pin I1025-win2/kc79_leap/l1kc79win2d2075.jsonl c83fa5b2 l1kc79win2d2075.jsonl $C2
pin I1025-win/kc79_d19/kc79_syscheck_1025.py 29dce7ea kc79_syscheck_1025.py
pin I1025-dh170/kc_break/d18_hybsign.py e089207a d18_hybsign.py
pin I1025-dh170/lower_root/read_lower.py 89309d3c read_lower.py
pin I1025-mac/d18/d185_scan_read.py 7c9d400f d185_scan_read.py
exit $rc
