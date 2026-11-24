#!/bin/bash
# #1087 T2: one rung. usage: run_rung.sh <K> <tag> <cap_s> [extra anm_run args...]; tag names the OUT folder (ks<K>_<tag>).
# Leg 15's own anm_run line (I966-dh370/leg_args_at_pause966.txt) with only --state, OUT, --steps 0 --keep_plan 0 --save_base 1 --ks K and
# --threads 4 changed (--base_polish as given in the extra args, or as in the line when absent). The rung is ended by TERM to its exact pid
# at the first "on 0: |F|" line of the octo-double Newton, or at the cap, or when it exits; KILL 60 s after TERM. Records seconds in rung.txt.
{
K=$1; TAG=$2; CAP=$3; shift 3
RAWROOT=/home/nathan/Source/choptuik-large-d-raw-wt613
OUT=$RAWROOT/I1087-dh370/ks${K}_$TAG
PY=/home/nathan/Source/choptuik-large-d-961/.venv/bin/python
HP=/home/nathan/Source/choptuik-large-d-966g/hp
STATE=I966-dh370/ks_chain3b/leg15_D263.4862_ks293/anm_pin3_D263.5987.npz
[ "$(git hash-object --no-filters $RAWROOT/$STATE | cut -c1-8)" = 2331c88f ] || { echo "state is not blob 2331c88f"; exit 9; }
[ "$(git -C $HP rev-parse --short=8 HEAD)" = 299728b7 ] || { echo "worktree not at 299728b7"; exit 9; }
mkdir -p $OUT || exit 9
LINE=( --state $STATE --kfreeze 3 --held_fit data/held_fit.json --N 31 --eps 1e-14 --h_max 0.045 --threads 4 --corrector od --tol_od 2e-34
  --qd_it 40 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept own
  --save_jet 1 --od_strong 4 --reseed_start pred --a_rule reseed --a_scale 0.000715 --jet_tangent_from 1 --series_split 1 --a_rise 1
  --proj_start pred --reseed_o_stop 1 --od_floor_delta 1e-30 --proj_o 1 --reseed_o_bar 1e-17 --base_polish 0 --reseed_qd_bar 1e-13
  --steps 0 --ks $K --keep_plan 0 --save_base 1 --D_max 273.4862 )
# extra args after the line: a repeated option takes its last value (argparse)
CMD=( nice -n 10 $PY -u $HP/anm_run.py $RAWROOT $OUT "${LINE[@]}" "$@" )
echo "# $(date -u '+%F %T') UTC K $K tag $TAG cap $CAP s cwd $HP: ${CMD[*]}" > $OUT/cmd.txt
cd $HP || exit 9
export PYTHONFAULTHANDLER=1
t0=$(date +%s)
"${CMD[@]}" > $OUT/stdout.log 2>&1 &
PID=$!
echo "$(date -u '+%F %T') UTC pid $PID" >> $OUT/cmd.txt
why=exited
while kill -0 $PID 2>/dev/null; do
  if grep -qE 'on 0: \|F\| ' $OUT/stdout.log 2>/dev/null; then why="first on 0 line"; break; fi
  if [ $(( $(date +%s) - t0 )) -ge $CAP ]; then why="cap $CAP s"; break; fi
  sleep 2
done
sec=$(( $(date +%s) - t0 ))
if kill -0 $PID 2>/dev/null; then
  kill -TERM $PID; for i in $(seq 30); do sleep 2; kill -0 $PID 2>/dev/null || break; done
  kill -0 $PID 2>/dev/null && { kill -KILL $PID; why="$why (KILL)"; }
fi
wait $PID; rc=$?
echo "$(date -u '+%F %T') UTC K $K tag $TAG: ended by: $why; seconds to that point $sec; exit $rc" | tee $OUT/rung.txt
grep -E '^base|on 0: \|F\| |base polish|octo-double Newton' $OUT/stdout.log | head -8 | tee -a $OUT/rung.txt
exit 0
}
