#!/bin/bash
# #1064 (dh170): leg 13's anm_run line as dh610 and win2 ran it for the order raise (comment 7060065590: --steps 0 --keep_plan 0 --save_base 1 --ks K), at D 262.0099 and ks 315, 4 threads, nice 10, to read anm_run's own
# start |F| and first Newton step beside raise_test1064.py's. Stopped by exact pid at the first "no trial step accepted" / "converged" line or after 50 min. --allow_unraw: OUT is in the raw-p4 input tree (not a git checkout); the output is pushed from there.
D=/home/nathan/Source/choptuik-large-d-raw-p4/I1064-dh170; HP=/home/nathan/Source/choptuik-large-d-1058b/hp
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python; RAW=/home/nathan/scratch949
ST=I966-dh370/ks_chain3b/leg14_D261.1415_ks293/anm_pin3_D262.0099.npz
say() { echo "== $(date -u '+%F %T') UTC $*" >> $D/exits_1064dh170.txt; }
cd $HP || exit 9
CMD="$PY -u anm_run.py $RAW $D/anm_ks315 --state $ST --kfreeze 3 --held_fit data/held_fit.json --N 31 --eps 1e-14 --h_max 2 --threads 4 --corrector od --tol_od 2e-34 --qd_it 40 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept own --save_jet 1 --od_strong 4 --reseed_start pred --a_rule reseed --a_scale 0.000715 --jet_tangent_from 1 --series_split 1 --a_rise 1 --proj_start pred --reseed_o_stop 1 --od_floor_delta 1e-30 --proj_o 1 --reseed_qd_bar 1e-13 --steps 0 --ks 315 --keep_plan 0 --save_base 1 --D_max 270.8483 --allow_unraw"
{ echo "# $(date -u '+%F %T') UTC cmd: $CMD"; } > $D/anm_ks315.log
say "start anm_run ks315 (own start |F|, first Newton step)"
s0=$(date +%s)
nice -n 10 /usr/bin/time -v $CMD >> $D/anm_ks315.log 2>&1 &
tp=$!; echo $tp > $D/time_pid_anm315.txt
while kill -0 $tp 2>/dev/null; do
  if grep -qE "no trial step accepted|converged|^base polish saved|stopping" $D/anm_ks315.log || [ $(( $(date +%s) - s0 )) -gt 3000 ]; then
    py=$(ps -o pid= --ppid $tp | head -1 | tr -d ' '); say "stop by exact pid: python $py and time $tp ($(( $(date +%s) - s0 )) s)"; kill -TERM $py $tp 2>/dev/null; break
  fi
  sleep 10
done
wait $tp; say "anm_run ks315 ended, $(( $(date +%s) - s0 )) s"
