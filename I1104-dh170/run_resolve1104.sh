#!/bin/bash
# #1104's second run (t5's order, comment 7226665371 and the hc of 19:34 UTC 27 Nov): re-solve macm3's k_c 127 D 23.125 state at kappa 0.5 with ell_refine.py (t5's command, 3 threads,
# nice 10, cap 57600 s on the python pid), then check the bars (|F| <= 5e-10, steps 5855 +- 2%). Writes DONE_resolve.txt (PASS or FAIL of the bars) or STOP_resolve.txt.
# Logs the python pid's RSS and CPU every 30 min (ell_refine.py prints no progress). The scans of the re-solved state start from run_scan1104.sh, launched by hand after PASS.
{
D=23.125; LAM0=2.0992182200
SRC=l1kc127Lmacm3; NEW=l1kc127k050dh170d23125; DT=D23.1250
SSB=e1dccb3c; SRB=58d3b080
OUT=/home/nathan/Source/choptuik-large-d-raw-p4/I1104-dh170
WT=/home/nathan/Source/choptuik-large-d-1025k79; WTM=$WT/solver/matter
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
TAG=resolve
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC [$TAG] $*" >> $OUT/steps.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
stop() { step "STOP: $*"; echo "STOP $(stamp) UTC: $*" > $OUT/STOP_$TAG.txt; exit 1; }
cd $OUT || exit 9
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 48c36355 ] || stop "regrid worktree not at 48c36355"
for f in dss_ell ell_ddm ell_dd ddnp; do git -C $WT diff --quiet 505d8399 HEAD -- solver/matter/$f.py || stop "$f.py differs from 505d8399"; done
[ "$(blob $WTM/ell_refine.py)" = 631e5801 ] && [ "$(blob $WTM/dss_ell.py)" = 5d28c19e ] || stop "ell_refine.py is not 631e5801 or dss_ell.py not 5d28c19e"
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/')" ] || stop "worktree solver/ has changes"
[ "$(blob in/sol_${SRC}_$DT.npy)" = $SSB ] && [ "$(blob in/$SRC.jsonl)" = $SRB ] || stop "in/ start is not the pinned blob ($SSB, $SRB)"
for f in $WTM/data/$NEW.jsonl $WTM/data/sol_${NEW}_$DT.npy; do [ -e $f ] && stop "$f exists"; done
for f in sol_${SRC}_$DT.npy $SRC.jsonl; do
  [ -e $WTM/data/$f ] && { [ "$(blob $WTM/data/$f)" = "$(blob in/$f)" ] || stop "data/$f exists and differs from in/$f"; } || cp in/$f $WTM/data/$f
done
[ "$(blob $WTM/data/sol_${SRC}_$DT.npy)" = $SSB ] && [ "$(blob $WTM/data/$SRC.jsonl)" = $SRB ] || stop "data/ start is not the pinned blob"
step "pins ok: regrid worktree 48c36355 (ell_refine.py 631e5801, dss_ell.py 5d28c19e = equal 505d8399 for ell_ddm, ell_dd, ddnp), start state $SSB, record $SRB (copied into data/)"
export OMP_NUM_THREADS=3 OPENBLAS_NUM_THREADS=3 MKL_NUM_THREADS=3
CMD="nice -n 10 timeout 57600 $PY -u ell_refine.py $SRC 127 $NEW 127 1 $D $LAM0 --kappa 0.5 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma"
echo "# $(stamp) UTC cmd (cwd $WTM, 3 threads, nice 10, cap 57600 s): $CMD" > $OUT/resolve.log
step "re-solve starts: $CMD"
t0=$(date +%s)
( cd $WTM && /usr/bin/time -v $CMD >> $OUT/resolve.log 2>&1 ) &
bp=$!
( while kill -0 $bp 2>/dev/null; do
    sleep 1800
    p=$(pgrep -n -f "ell_refine.py $SRC 127 $NEW")
    [ -n "$p" ] && echo "$(stamp) UTC [$TAG] alive: pid $p RSS $(ps -o rss= -p $p) kB CPU $(ps -o pcpu= -p $p)% elapsed $(( $(date +%s) - t0 )) s" >> $OUT/steps.txt
  done ) &
wait $bp; rc=$?
step "re-solve exit $rc, wall $(( $(date +%s) - t0 )) s (0 wanted; 124 is the cap); $(grep -E 'Maximum resident|Elapsed' $OUT/resolve.log | tr '\n' ' ' | cut -c1-200)"
[ $rc = 0 ] || stop "the re-solve exit $rc"
[ -s $WTM/data/$NEW.jsonl ] && [ -s $WTM/data/sol_${NEW}_$DT.npy ] || stop "the re-solve wrote no state or record"
cp -n $WTM/data/$NEW.jsonl $WTM/data/sol_${NEW}_$DT.npy $OUT/
step "record: $(tail -1 $OUT/$NEW.jsonl | jq -c '{D,kc,kappa,u0,F,F_start,steps,Delta,Delta_src,constraint,seconds}'); state $(blob $OUT/sol_${NEW}_$DT.npy), record $(blob $OUT/$NEW.jsonl)"
v=$(tail -1 $OUT/$NEW.jsonl | jq -r '(.F <= 5e-10) and (.steps >= 5855*0.98) and (.steps <= 5855*1.02) and (.kappa == 0.5)')
if [ "$v" = true ]; then echo "PASS $(stamp) UTC: |F| $(tail -1 $OUT/$NEW.jsonl | jq .F), steps $(tail -1 $OUT/$NEW.jsonl | jq .steps) (bars |F| <= 5e-10, steps 5855 +- 2%)" > $OUT/DONE_resolve.txt
else echo "FAIL $(stamp) UTC: |F| $(tail -1 $OUT/$NEW.jsonl | jq .F), steps $(tail -1 $OUT/$NEW.jsonl | jq .steps) (bars |F| <= 5e-10, steps 5855 +- 2%): the state is not used" > $OUT/DONE_resolve.txt; fi
step "bars: $(cat $OUT/DONE_resolve.txt)"
exit 0
}
