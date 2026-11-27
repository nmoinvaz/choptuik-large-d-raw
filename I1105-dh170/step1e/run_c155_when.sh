#!/bin/bash
# #1105 step 1e: root the D 15.5 continuation state (c155) once one of the two re-solves (r165b, r155) has ended, so the busy threads stay within t5's order.
# usage: run_c155_when.sh        (waits for a "re-solve exit" line of r165b or r155 in steps_1e.txt, or a DONE_/STOP_ file of either)
{
OUT=/home/nathan/Source/choptuik-large-d-raw-p4/I1105-dh170/step1e
WT2=/home/nathan/Source/choptuik-large-d-1102/solver/matter
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
cd $OUT || exit 9
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC [c155] $*" >> $OUT/steps_1e.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
stop() { step "STOP: $*"; echo "STOP $(stamp) UTC: $*" > $OUT/STOP_c155.txt; exit 1; }
[ "$(blob in/sol_l1kc55Fb1025_D15.5000.npy)" = 990ccde2 ] && [ "$(blob in/l1kc55Fb1025.jsonl)" = 5be40af4 ] || stop "in/ D 15.5 state or record is not 990ccde2 / 5be40af4"
step "waiting for one re-solve (r165b or r155) to end"
until grep -qE '\[(r165b|r155)\] re-solve exit' steps_1e.txt || [ -f DONE_r165b.txt ] || [ -f DONE_r155.txt ] || [ -f STOP_r165b.txt ] || [ -f STOP_r155.txt ]; do sleep 20; done
step "a re-solve ended: c155's root starts"
( cd $WT2 && nice -n 10 $PY -I d18_secant.py selftest > $OUT/selftest_secant_c155.txt 2>&1 ); e0=$?
step "d18_secant.py selftest exit $e0 (0 wanted)"; [ $e0 = 0 ] || stop "d18_secant.py selftest failed"
exec $OUT/run_root1e.sh c155 15.5 in/sol_l1kc55Fb1025_D15.5000.npy in/l1kc55Fb1025.jsonl 2.3282 2.3522
}
