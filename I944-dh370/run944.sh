#!/bin/bash
# #944 on dh370: the order-160 case of --od_weak_first 1 (main c714694a), the 4.8.2 build of the #935 worktree moved to c714694a
# (Python-only changes since 043834d9) with multidouble's Python package reinstalled at 482c6835. Two earlier runs, with the
# package at a93e0896, were stopped on the coordinator's order: on d93f5b1b (k160_weakfirst_d93f5b1b*) and on 8c1857ce
# (k160_weakfirst_old_pkg*). dh610's chain_k160 command (I903-dh610/run903c.sh's flags F, --ks 160 --keep_plan 1
# --D_max 262), with --steps 1 --od_weak_first 1, 12 threads, nice 10, one run at a time. The unit carries RuntimeMaxSec=10800.
#   run944.sh k160    from I903-dh610/chain_k160/anm_pin3_D234.0000.npz, output k160_weakfirst/ (dh610's default run refused a = 1, 0.5)
#   run944.sh a0125   from the same D 234.0 base, --a0 0.125 and the default corrector (no --od_weak_first), output k160_a0125/
#   run944.sh a0125wf the same with --od_weak_first 1 (only if the default at 0.125 fails), output k160_a0125_weakfirst/
#   run944.sh d225    from I903-dh610/chain_k160/anm_pin3_D225.0000.npz, output k160_d225/ (the default converged: stored next state D226)
WT=/home/nathan/Source/choptuik-large-d-935
R=/home/nathan/Source/choptuik-large-d-raw-wt613
OUT=$R/I944-dh370
PY=$WT/.venv/bin/python
L=$OUT/exits_944.txt
F="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --threads 12 --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred"
case $1 in
  k160) S=I903-dh610/chain_k160/anm_pin3_D234.0000.npz; O=k160_weakfirst; X="--od_weak_first 1" ;;
  d225) S=I903-dh610/chain_k160/anm_pin3_D225.0000.npz; O=k160_d225; X="--od_weak_first 1" ;;
  a0125) S=I903-dh610/chain_k160/anm_pin3_D234.0000.npz; O=k160_a0125; X="--a0 0.125" ;;
  a0125wf) S=I903-dh610/chain_k160/anm_pin3_D234.0000.npz; O=k160_a0125_weakfirst; X="--a0 0.125 --od_weak_first 1" ;;
  *) echo "usage: run944.sh k160|d225|a0125|a0125wf"; exit 2 ;;
esac
cd "$WT/hp" || exit 1
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
mkdir -p "$OUT/$O"
echo "944 $O start $(date -u '+%F %T') hp $(git -C "$WT" rev-parse --short HEAD), package $(grep -o '"commit_id": "[0-9a-f]\{8\}' "$WT"/.venv/lib/python3.14/site-packages/multidouble-*.dist-info/direct_url.json | grep -o '[0-9a-f]\{8\}$'), state $S, flags $X, load $(cut -d' ' -f1-3 /proc/loadavg)" >> "$L"
( while true; do echo "$(date -u +%T) $(free -m | awk '/Mem:/{print $3, $7}')" >> "$OUT/mem_$O.log"; sleep 60; done ) &
SAMP=$!
trap 'echo "944 $O killed by SIGTERM (the unit limit) wall $(( $(date +%s) - t )) s $(date -u "+%F %T")" >> "$L"; kill $SAMP; exit 143' TERM
t=$(date +%s)
nice -n 10 /usr/bin/time -f "time %e s, max rss %M kB" "$PY" -u anm_run.py "$R" "$OUT/$O" --state "$R/$S" $F --ks 160 --keep_plan 1 \
  --steps 1 --D_max 262 $X > "$OUT/$O.log" 2>&1
rc=$?
kill $SAMP
echo "944 $O anm_run exit $rc wall $(( $(date +%s) - t )) s $(date -u '+%F %T')" >> "$L"
exit $rc
