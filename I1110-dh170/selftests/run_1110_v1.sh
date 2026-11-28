#!/bin/bash
# #1110 dh170 (t5's order of 28 Nov 01:15 UTC): a chord state's root against R2's LM root at k_c 127, D 23.0. Each step is its own `systemd-run --user --wait` unit (i1110-jac, -svd,
# -chord, -ctl, -coords, -root[, -rootwide]) under systemd-inhibit, nice -n 10, 2 threads (OPENBLAS/OMP/MKL/RAYON/VECLIB), under timeout; output into this folder; steps in steps.txt [1110].
#   jac   R0's J (exit 3: not the record system: STOP)        svd  its SVD          chord kappa=0.35 -> bar 1 (8351 steps, |F| <= 5e-10: else STOP)
#   ctl   chord kappa=0.34 -> bar 2 (a count other than 8351: else STOP)             coords  |z_chord - z_R2| by R0's bands
#   root  d18_secant's Brent on the chord state's own map at (0.10, 0.13), tol 1e-6, --b12=fast; widened once to (0.05, 0.16) if refused (no bracket); cap 14400 s (timeout)
# R3 (#1101, I1101-dh170) keeps priority: the root does not start until R3's scan group has finished (R3 has started its secant, or is done or stopped, or its unit is not running): a stopped
# process keeps its memory, so the memory rule would hold R3's fourth scan back behind #1104's secant and the root. The root counts as a scanner process of the memory rule (scan_admit.sh, via
# the marker argument --note="d18_secant.py scan root1110"). Then results_1110.py reads the maps and the root records (results_1110_maps.md, results_1110.md) and DONE_1110.txt is written.
# usage: run_1110.sh          Stops at the first failure (STOP_1110.txt). Environment overrides (OUT WT WTM PY R3 UP DRY YTICK CAP) are only for the dry-run test (selftests/dryrun_1110.sh).
{
: "${OUT:=/home/nathan/Source/choptuik-large-d-raw-p4/I1110-dh170}"
: "${WT:=/home/nathan/Source/choptuik-1110}"
: "${WTM:=$WT/solver/matter}"
: "${PY:=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python}"
: "${R3:=/home/nathan/Source/choptuik-large-d-raw-p4/I1101-dh170}"
: "${UP:=i1110}"
: "${DRY:=}"
: "${YTICK:=20}"
: "${CAP:=14400}"
TAG=1110
REC=$OUT/in/l1kc127k070w2.jsonl; STATE=$OUT/in/sol_l1kc127k070w2_D23.0000.npy; R2S=$OUT/in/R2_sol_l1kc127k035w2_D23.0000.npy
RESB=138334a9          # results_1110.py blob (set when the driver is pinned)
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC [$TAG] $*" >> $OUT/steps.txt; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
stop() { step "STOP: $*"; echo "STOP $(stamp) UTC: $*" > $OUT/STOP_$TAG.txt; exit 1; }
cd $OUT || exit 9
if [ -z "$DRY" ]; then
  [ "$(git -C $WT rev-parse --short=8 HEAD)" = db7f9c60 ] && [ -z "$(git -C $WT status --short solver | head -1)" ] || stop "the worktree is not db7f9c60 or not clean"
  [ "$(blob $WTM/i1101_weakdir.py)" = 8709abbd ] && [ "$(blob $WTM/d18_secant.py)" = eb1396ad ] || stop "i1101_weakdir.py is not 8709abbd or d18_secant.py not eb1396ad"
  [ "$(blob $STATE)" = 90d3e655 ] && [ "$(blob $REC)" = d1a3a641 ] && [ "$(blob $R2S)" = 25ba3a91 ] || stop "an input is not the pinned blob (90d3e655, d1a3a641, 25ba3a91)"
  [ "$(blob results_1110.py)" = "$RESB" ] || stop "results_1110.py is not $RESB"
  [ "$(blob $R3/scan_admit.sh)" = e61f8891 ] || stop "scan_admit.sh is not e61f8891"
fi
for f in jac_r0.npz svd_r0.npz sol_chord035_D23.0000.npy sol_chord034_D23.0000.npy root_chord035.jsonl; do [ -e $f ] && stop "$f exists: not overwriting"; done
. $R3/scan_admit.sh
step "pins ok (worktree db7f9c60, i1101_weakdir.py 8709abbd, d18_secant.py eb1396ad, inputs 90d3e655 d1a3a641 25ba3a91, results_1110.py $RESB, scan_admit.sh e61f8891)"
e=""; for m in "" bar7 bar2 ref count sign; do
  if [ -z "$m" ]; then $PY -I results_1110.py selftest > selftests/selftest_results_1110.txt 2>&1; else $PY -I results_1110.py selftest --mutate=$m > selftests/selftest_results_1110_$m.txt 2>&1; fi; e="$e $?"
done
step "results_1110.py selftest exits (plain, bar7, bar2, ref, count, sign):$e (0 1 1 1 1 1 wanted)"
[ "$e" = " 0 1 1 1 1 1" ] || stop "a results_1110.py selftest or mutation did not read as written"
unit() {   # unit NAME TIMEOUT LOG CMD...: one systemd-run unit; waits; returns the command's exit status
  local name=$1 to=$2 log=$3 v fe=(); shift 3
  for v in ${!FAKE_@}; do fe+=(-E "$v=${!v}"); done      # the dry-run test's fake-scanner switches (none in a real run)
  systemd-run --user --wait --collect --unit=$name --working-directory=$WTM \
    -p StandardOutput=append:$OUT/$log -p StandardError=append:$OUT/$log "${fe[@]}" \
    -E OPENBLAS_NUM_THREADS=2 -E OMP_NUM_THREADS=2 -E MKL_NUM_THREADS=2 -E RAYON_NUM_THREADS=2 -E VECLIB_MAXIMUM_THREADS=2 -E D18_DIR=$WTM \
    /usr/bin/systemd-inhibit --what=sleep "--why=#1110 $name" --mode=block nice -n 10 /usr/bin/time -v timeout $to "$@" > $OUT/unit_$name.out 2>&1
}
run_step() {   # run_step NAME TIMEOUT LOG CMD...
  local name=$1 t0=$(date +%s) rc
  step "$name starts (timeout $2 s): ${*:4}"
  unit "$@"; rc=$?
  step "$name exit $rc, $(( $(date +%s) - t0 )) s; $(grep -E 'Maximum resident|Elapsed' $OUT/$3 | tail -2 | tr -s '\t' ' ' | tr '\n' ';')"
  return $rc
}
# ---- 1. J
run_step $UP-jac 7200 jac_r0.log $PY -u i1101_weakdir.py jac $REC $STATE 23.0 $OUT/jac_r0.npz --pin=90d3e655,d1a3a641; rc=$?
[ $rc = 3 ] && stop "jac exit 3: not the record system (or a pin differs): stop and report"
[ $rc = 0 ] && [ -s jac_r0.npz ] || stop "jac exit $rc"
step "jac: $(grep -h '^{"out"' jac_r0.log | tail -1)"
# ---- 2. SVD
run_step $UP-svd 3600 svd_r0.log $PY -u i1101_weakdir.py svd $OUT/jac_r0.npz $OUT/svd_r0.npz; rc=$?
[ $rc = 0 ] && [ -s svd_r0.npz ] || stop "svd exit $rc"
step "svd: $(grep -h '^svd ' svd_r0.log | tail -1)"
# ---- 3. chord at kappa 0.35: bar 1
run_step $UP-chord 3600 chord035.log $PY -u i1101_weakdir.py chord $OUT/svd_r0.npz $REC $STATE 23.0 kappa=0.35 $OUT/sol_chord035_D23.0000.npy; rc=$?
[ $rc = 0 ] && [ -s sol_chord035_D23.0000.map.json ] || stop "chord kappa=0.35 exit $rc"
step "chord 0.35: $(grep -h 'kappa=0.35: steps' chord035.log | tail -1 | cut -c1-330)"
jq -e '(.steps == 8351) and (.F <= 5e-10)' sol_chord035_D23.0000.map.json > /dev/null || stop "bar 1 fails: $(jq -c '{steps,F}' sol_chord035_D23.0000.map.json) (wanted steps 8351, |F| <= 5e-10): stop and report before the root"
step "bar 1 passes: $(jq -c '{steps,F,Delta}' sol_chord035_D23.0000.map.json)"
# ---- 4. the control: kappa 0.34 must give another count
run_step $UP-ctl 3600 chord034.log $PY -u i1101_weakdir.py chord $OUT/svd_r0.npz $REC $STATE 23.0 kappa=0.34 $OUT/sol_chord034_D23.0000.npy; rc=$?
[ $rc = 0 ] && [ -s sol_chord034_D23.0000.map.json ] || stop "chord kappa=0.34 (control) exit $rc"
step "chord 0.34 (control): $(grep -h 'kappa=0.34: steps' chord034.log | tail -1 | cut -c1-330)"
jq -e '.steps != 8351' sol_chord034_D23.0000.map.json > /dev/null || stop "bar 2 fails: the kappa=0.34 control gives $(jq .steps sol_chord034_D23.0000.map.json) steps = 8351: the count cannot tell maps apart; stop and report"
step "bar 2 passes: the control gives $(jq .steps sol_chord034_D23.0000.map.json) steps"
$PY -I results_1110.py maps sol_chord035_D23.0000.map.json sol_chord034_D23.0000.map.json > results_1110_maps.md 2>&1; step "results_1110.py maps exit $? (0 both bars pass)"
# ---- 5. the state difference by R0's bands
run_step $UP-coords 3600 coords.log $PY -u i1101_weakdir.py coords $OUT/svd_r0.npz $R2S chord035=$OUT/sol_chord035_D23.0000.npy; rc=$?
[ $rc = 0 ] || stop "coords exit $rc"
grep -hE '^(weak vectors|chord035)' coords.log > coords_chord035.txt; step "coords: $(grep -h '^chord035' coords.log | cut -c1-300)"
# ---- 6. the root: R3's scan first (it starts only after R3's scan group has finished, see the header); memory rule; t5's cap of 14400 s
r3_pending() {   # R3's scan group has not finished: R3 not landed, or landed and scanning (a 'secant starts' or 'done' line of R3, or its DONE/STOP file, ends it)
  [ -f $R3/DONE_r3.txt ] && return 1; [ -f $R3/STOP_r3.txt ] && return 1
  grep -q '\[r3\] \(secant starts\|done\)' $R3/steps.txt 2>/dev/null && return 1
  [ -n "$DRY" ] || systemctl --user is-active --quiet i1101r3 || return 1     # no R3 unit: nothing will land
  return 0
}
root_run() {   # root_run LO HI JSONL LOG UNIT
  local rpid
  if r3_pending; then step "root $5 waits: R3's scan (#1101, unit i1101r3) has not finished (not landed, or its four scans run); t5: R3 keeps priority"; fi
  while r3_pending; do sleep ${YTICK}; done
  step "root $5 ($1, $2) starts: R3's scan group is over; memory rule (at most $(maxp) scanner processes, $(nscan) running)"
  bg_admit run_step $5 $CAP $4 $PY -u i1101_weakdir.py root $OUT/sol_chord035_D23.0000.npy $1 $2 $3 --tol=1e-6 --b12=fast "--note=d18_secant.py scan root1110"
  rpid=$ADMIT_PID
  wait $rpid; rc=$?
  return $rc
}
root_run 0.10 0.13 $OUT/root_chord035.jsonl root_chord035.log $UP-root; rc=$?
fs=$(jq -r 'select(.kind=="root") | .status' root_chord035.jsonl 2>/dev/null | tail -1)
step "root (0.10, 0.13) exit $rc, final status '${fs:-none}' (exit 0 tol, 2 refused: no bracket, 4 maxev or non-robust, 3 not the saved system, 124/143 the cap); $(grep -c '"kind": "eval"' root_chord035.jsonl 2>/dev/null) evaluations"
WIDE=""
if [ "$fs" = refused ]; then
  step "(0.10, 0.13) does not bracket (refused): widening once to (0.05, 0.16) (t5)"
  root_run 0.05 0.16 $OUT/root_chord035_wide.jsonl root_chord035_wide.log $UP-rootwide; rc=$?
  fs=$(jq -r 'select(.kind=="root") | .status' root_chord035_wide.jsonl 2>/dev/null | tail -1)
  step "root (0.05, 0.16) exit $rc, final status '${fs:-none}'; $(grep -c '"kind": "eval"' root_chord035_wide.jsonl 2>/dev/null) evaluations"
  WIDE=root_chord035_wide.jsonl
fi
$PY -I results_1110.py read root_chord035.jsonl $WIDE > results_1110.md 2> results_1110.err; rr=$?
step "results_1110.py read exit $rr (0 a root formed, 4 no root but a robust bracket, 2 no bracket), results_1110.md"
echo "$TAG DONE $(stamp) UTC, reading exit $rr, root final status '${fs:-none}'" > DONE_$TAG.txt
step "done"
exit 0
}
