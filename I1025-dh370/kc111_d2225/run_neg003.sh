#!/bin/bash
# #1025 kc111_d2225, t5's ruling (hc 25 Nov): lambda -0.03 as its own job after the scan, on the accepted k_c 111 state, only if 0.01 and 0.02 leave P and "S below 0.01" undecided.
# d18_hybsign.py (e089207a, unmodified), 1 process of 1 thread at nice 10, the scan's output directory (file scan_D22.25_pneg003.jsonl, which read_lower.py's glob scan_*_p*.jsonl picks up).
# Then read_lower.py on the window -0.03 to 0.50. A systemd user unit (i1025k111n); no hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1025-dh370/kc111_d2225
WT=/home/nathan/Source/choptuik-large-d-1025; WTM=$WT/solver/matter
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
. $OUT/stage.conf
IN=$OUT/in; SCAN=$OUT/scan
STATE=$OUT/sol_${TAG}_${DT}.npy; STUB=$OUT/$TAG.jsonl
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
grep -q '^ACCEPTED' $OUT/VERDICT.txt || { step "NEG003 STOP: no ACCEPTED verdict"; exit 1; }
[ "$(blob $STATE)" = 7fc75ef8 ] && [ "$(blob $STUB)" = 06dc9d92 ] && [ "$(blob $IN/d18_hybsign.py)" = e089207a ] && [ "$(blob $IN/read_lower.py)" = 89309d3c ] || { step "NEG003 STOP: the state, record, scanner or reader is not the pinned blob"; exit 1; }
[ -e $SCAN/scan_D22.25_pneg003.jsonl ] && { step "NEG003 STOP: the output exists"; exit 1; }
step "lambda -0.03 starts: 1 process x 1 thread, nice 10; state sol_${TAG}_${DT}.npy 7fc75ef8, record 06dc9d92"
t0=$(date +%s)
( cd $WTM && nice -n 10 env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$WTM \
    /usr/bin/time -v $PY -u $IN/d18_hybsign.py $STUB $STATE $D "-0.03" $SCAN/scan_D22.25_pneg003.jsonl > $SCAN/scan_pneg003.raw 2>&1 ); rc=$?
step "lambda -0.03: exit $rc, $(( $(date +%s) - t0 )) s; $(grep -h 'the record system\|NOT the record system' $SCAN/scan_pneg003.raw | cut -c1-160)"
grep -hE 'Elapsed|Maximum resident' $SCAN/scan_pneg003.raw >> $OUT/steps.txt
cd $IN
{ echo "== window: read_lower.py scan -0.03 0.50"; $PY -I read_lower.py $SCAN -0.03 0.50; echo "(exit $?)"; } > $OUT/read_lower_neg003.txt 2>&1
step "read_lower.py read the window -0.03 to 0.50 (reading in read_lower_neg003.txt)"
echo "NEG003 DONE $(stamp) UTC" > $OUT/NEG003_DONE.txt
exit 0
}
