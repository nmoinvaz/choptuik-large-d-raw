#!/usr/bin/env bash
# #803 on the win laptop: #780's light-cone comparison at D = 4. i780_compare.py at the double count's evaluation
# points (--dd=0: only the light-cone block, in double-double, and the LU differ from complex_imag.py), then
# complex_imag_dd.py count over those values in B0, U0 and FULL, then summary803.py against I95's double counts.
# Worktree C:/Users/nathan/Source/choptuik-i803 at main, venv-t151 (no hp kernel is used). One process.
PY=/c/Users/nathan/Source/venv-t151/Scripts/python.exe
RAW=/c/Users/nathan/Source/choptuik-large-d-raw; R=$RAW/I803-win
B=/c/Users/nathan/scratch803
mkdir -p $B
git -C $RAW fetch -q origin
git -C $RAW show origin/main:I95-mac/imag/evals_D4_M48.jsonl > $B/evals_D4.jsonl
git -C $RAW show origin/main:I95-mac/imag/counts.jsonl > $B/counts_i95.jsonl
cd /c/Users/nathan/Source/choptuik-i803/solver/matter || exit 9
ST=../../hp/data/lowD_states/lowDn_D4.0000_M48.npz
log() { echo "803 $1 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_803.txt; }
log "start, main $(git rev-parse --short=8 HEAD)"
"$PY" -u i780_compare.py $ST $B/evals_D4.jsonl --dd=0 --out=$R/dd0_D4.jsonl > $R/dd0_D4.log 2>&1
log "compare exit $? (0: every phase within 1e-3 rad)"
"$PY" -u complex_imag_dd.py count $ST B0 U0 FULL --dd=0 --rtol=1e-11 --evlog=$R/dd0_D4.jsonl --out=$R/counts_dd0.jsonl > $R/count_dd0_D4.log 2>&1
log "count exit $?"
"$PY" -I $R/summary803.py $R $B/counts_i95.jsonl > $R/summary803.txt 2>&1
log "summary exit $? (0: PASS)"
log "all done"
