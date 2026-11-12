#!/usr/bin/env bash
# #525 part 3: twelve steps of a = -0.5 from crawlG D 216.1312 in one anm_run chain (main 14dc386, 16 threads), near_null_eq.py --plant=7 (0cce81e, 2 threads, nice) on each new state as it
# appears, then the rows_only control (must exit nonzero) at D 213.1312. Steps of negative a are untested: a refused step ends the chain ("stopped: no convergence after three halvings" in down.log).
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
R=$RAW/I525-win2
S=I461-win2/crawlG/anm_pin3_D216.1312.npz
[ -f $RAW/$S ] || { echo "missing $S" >&2; exit 9; }
export PYTHONFAULTHANDLER=1
cd /d/choptuik-i446g/hp || exit 9
[ "$(git rev-parse --short=7 HEAD)" = "14dc386" ] || { echo "worktree D:/choptuik-i446g is not at 14dc386" >&2; exit 9; }
echo "run_i525 start $(date -u '+%Y-%m-%d %H:%M:%S UTC') at 14dc386 from $S, 12 steps of a = -0.5" >> $R/exits.txt
"$PY" -u anm_run.py $RAW $R/down --state $S --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 \
   --h_max -0.5 --steps 12 --D_max 400 --threads 16 --corrector od --tol_od 1e-60 --qd_it 12 --a_grow 1.0 --a_hold 1 --lam_stall 0.04 --od_junk 0 --save_dz0 1 --jet_o 1 --reseed 2 --reseed_q 1 \
   --held_o 1 --reseed_o 3 --save_pred 1 > $R/down.log 2>&1 &
APID=$!
echo "anm_run pid $APID" >> $R/exits.txt
done_list=" "
eq_one() {
  local f=$1 Dn
  Dn=$(basename $f .npz); Dn=${Dn#anm_pin3_}
  cd /d/choptuik-i505/hp || return 9
  echo "eq_$Dn start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
  nice -n 10 "$PY" -u near_null_eq.py $RAW I525-win2/down/anm_pin3_$Dn.npz --threads=2 --plant=7 --json=$R/eq_$Dn.json > $R/eq_$Dn.log 2>&1
  echo "eq_$Dn exit $? $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
}
while true; do
  alive=1; kill -0 $APID 2>/dev/null || alive=0
  for f in $R/down/anm_pin3_D*.npz; do
    [ -f "$f" ] || continue
    case "$done_list" in *" $f "*) continue;; esac
    age=$(( $(date +%s) - $(stat -c %Y "$f") ))
    if [ $alive -eq 1 ] && [ $age -lt 30 ]; then continue; fi
    eq_one "$f"; done_list="$done_list$f "
  done
  if [ $alive -eq 0 ]; then
    n=0; for f in $R/down/anm_pin3_D*.npz; do [ -f "$f" ] && case "$done_list" in *" $f "*) ;; *) n=1;; esac; done
    [ $n -eq 0 ] && break
  fi
  sleep 20
done
wait $APID; echo "anm_run exit $? $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
C=$R/down/anm_pin3_D213.1312.npz
if [ -f $C ]; then
  cd /d/choptuik-i505/hp || exit 9
  echo "control eq_D213.1312 --mutate=rows_only start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
  nice -n 10 "$PY" -u near_null_eq.py $RAW I525-win2/down/anm_pin3_D213.1312.npz --threads=2 --plant=7 --mutate=rows_only > $R/eq_D213.1312_ctl_rows_only.log 2>&1
  echo "control eq_D213.1312 --mutate=rows_only exit $? (must be nonzero) $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
else
  echo "control not run: no state at D 213.1312" >> $R/exits.txt
fi
echo "run_i525 done $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
