#!/bin/bash
# #1025 macm3b kc87_d195: copy the pinned inputs from raw commits (git cat-file, exact bytes) into in/ and check each blob (git hash-object --no-filters).
# The ref_dh610_* files are dh610's k_c 87 D 19.5 regrid and scan, for comparison only (the run does not use them). Writes pins.txt. Exit 1 on any mismatch.
RAWG=$HOME/Source/choptuik-large-d-raw-749p
OUT=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_d195
C=8e4797ff    # the scripts (as kc79_d19375, kc87_d19375, kc87_d1975)
C2=f40a4556   # dh370's accepted k_c 79 D 19.5 state and record (raw I1025-dh370/kc79_d195/)
C3=ec9fb489   # dh610's k_c 87 check and its diff
C4=94e9ebc6   # dh610's k_c 87 D 19.5 regrid result and scan (comparison only)
rc=0
: > $OUT/pins.txt
pin() {  # path-in-raw blob8 name-in-in/ [commit]
  CC=${4:-$C}
  git -C $RAWG cat-file blob $CC:$1 > $OUT/in/$3 || { echo "cannot read $CC:$1"; rc=1; return; }
  got=$(git hash-object --no-filters $OUT/in/$3 | cut -c1-8)
  [ "$got" = "$2" ] && s=ok || { s="MISMATCH (wanted $2)"; rc=1; }
  echo "$got  $3  <- $CC:$1  $s" | tee -a $OUT/pins.txt
}
pin I1025-dh370/kc79_d195/sol_l1kc79dh370d195_D19.5000.npy 9528b355 sol_l1kc79dh370d195_D19.5000.npy $C2
pin I1025-dh370/kc79_d195/l1kc79dh370d195.jsonl 5777d2a2 l1kc79dh370d195.jsonl $C2
pin I1025-dh610/kc87_d195/in/kc87_syscheck_1025.py 6df5d960 kc87_syscheck_1025.py $C3
pin I1025-dh610/kc87_d195/kc87_syscheck_1025.diff dfb42ff7 kc87_syscheck_1025.diff.dh610 $C3
pin I1025-win/kc79_d19/kc79_syscheck_1025.py 29dce7ea kc79_syscheck_1025.py
pin I1025-dh170/kc_break/d18_hybsign.py e089207a d18_hybsign.py
pin I1025-dh170/lower_root/read_lower.py 89309d3c read_lower.py
pin I1025-mac/d18/d185_scan_read.py 7c9d400f d185_scan_read.py
pin I1025-dh610/kc87_d195/sol_l1kc87dh610d195_D19.5000.npy 57f8e2d3 ref_dh610_sol_l1kc87dh610d195_D19.5000.npy $C4
pin I1025-dh610/kc87_d195/l1kc87dh610d195.jsonl 64b8db7c ref_dh610_l1kc87dh610d195.jsonl $C4
pin I1025-dh610/kc87_d195/scan/scan_D19.5_1025.jsonl 8c37aa4d ref_dh610_scan_D19.5_1025.jsonl $C4
pin I1025-dh610/kc87_d195/read_lower.txt 0669efe7 ref_dh610_read_lower.txt $C4
exit $rc
