#!/bin/bash
# #1064 (dh170): run_anm_ks315.sh's line through anm_probe1064.py (ElimO.project prints its input and output); stopped by exact pid after the first two PROBE lines or 40 min.
KS=${1:-315}; TAG=${2:-probe315}
D=/home/nathan/Source/choptuik-large-d-raw-p4/I1064-dh170; HP=/home/nathan/Source/choptuik-large-d-1058b/hp
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python; RAW=/home/nathan/scratch949
ST=I966-dh370/ks_chain3b/leg14_D261.1415_ks293/anm_pin3_D262.0099.npz
say() { echo "== $(date -u '+%F %T') UTC $*" >> $D/exits_1064dh170.txt; }
cd $HP || exit 9; export HP_DIR=$HP
ARGS="$RAW $D/anm_$TAG --state $ST --kfreeze 3 --held_fit data/held_fit.json --N 31 --eps 1e-14 --h_max 2 --threads 4 --corrector od --tol_od 2e-34 --qd_it 40 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept own --save_jet 1 --od_strong 4 --reseed_start pred --a_rule reseed --a_scale 0.000715 --jet_tangent_from 1 --series_split 1 --a_rise 1 --proj_start pred --reseed_o_stop 1 --od_floor_delta 1e-30 --proj_o 1 --reseed_qd_bar 1e-13 --steps 0 --ks $KS --keep_plan 0 --save_base 1 --D_max 270.8483 --allow_unraw"
echo "# $(date -u '+%F %T') UTC anm_probe1064.py $ARGS" > $D/anm_$TAG.log
say "start $TAG (anm_run through anm_probe1064.py, ks $KS)"
s0=$(date +%s)
nice -n 10 /usr/bin/time -v $PY -u $D/anm_probe1064.py $ARGS >> $D/anm_$TAG.log 2>&1 &
tp=$!
while kill -0 $tp 2>/dev/null; do
  n=$(grep -c "^PROBE project" $D/anm_$TAG.log)
  if [ "$n" -ge 2 ] || grep -qE "Traceback" $D/anm_$TAG.log || [ $(( $(date +%s) - s0 )) -gt 2400 ]; then
    py=$(ps -o pid= --ppid $tp | head -1 | tr -d ' '); say "stop by exact pid: python $py and time $tp ($n PROBE lines, $(( $(date +%s) - s0 )) s)"; kill -TERM $py $tp 2>/dev/null; break
  fi
  sleep 10
done
wait $tp; say "$TAG ended, $(( $(date +%s) - s0 )) s"
