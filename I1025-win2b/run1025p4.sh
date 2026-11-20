#!/usr/bin/env bash
# #1025 P4 amendment 7 (the coordinator's GO, hc ~21:45 UTC 20 Nov): xfkappa's p4_driver_rows.sh (blob e004c9ec) on win2b's k_c 71 recheck row, after its built-in cross-check row (Fb, D 16, k_c 55 -> 2.244042809616683 to 1e-5).
#   PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe THREADS=4 bash p4_driver_rows.sh WT RAW OUT ROWLIST e0c173234c69941b16135ea529145c391599d80a
# WT = D:/choptuik-1025p4 (505d8399), RAW = the fresh extraction directory (git show of origin/main 8def2687, blobs checked by p4_extract1025.sh), OUT = I1025-win2b/p4 (live raw folder), BelowNormal (set by the launching PowerShell).
# usage: bash run1025p4.sh
X=/d/choptuik-large-d-raw/I1025-win2b
WT=D:/choptuik-1025p4
RAW=D:/choptuik-p4in-1025-20261120
OUT=D:/choptuik-large-d-raw/I1025-win2b/p4
BLOB=e0c173234c69941b16135ea529145c391599d80a
log() { echo "1025 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/exits_1025.txt; }
[ "$(git -C $WT rev-parse HEAD)" = 505d839940456a3d04321d75cf66cc3b5bc831c4 ] || { log "P4 not started: $WT is not at 505d8399"; exit 9; }
[ "$(git hash-object --no-filters $RAW/I1025-mac/p4_driver_rows.sh)" = e004c9ec5c722578b460a1354adc337626e75129 ] || { log "P4 not started: driver is not blob e004c9ec"; exit 9; }
[ -f $OUT/README.md ] || { log "P4 not started: $OUT/README.md missing"; exit 9; }
export PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe THREADS=4
log "P4 driver starting (WT $WT, RAW $RAW, OUT $OUT, row list blob $BLOB, THREADS 4)"
bash $RAW/I1025-mac/p4_driver_rows.sh $WT $RAW $OUT $RAW/I1025-mac/p4_rows_win2b.txt $BLOB < /dev/null >> $X/p4_launcher.out 2>&1
rc=$?
log "P4 driver exit $rc"
