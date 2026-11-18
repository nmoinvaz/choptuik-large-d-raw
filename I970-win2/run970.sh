#!/bin/bash
# #970 on win2: one step from ks_chain2's D 238.1789 state at a 0.4657 with --reseed_qd_bar 1e-21 (venv-i962, worktree D:\choptuik-i962).
# F is run903e.sh's flags (I903-win2/run903e.sh) with --threads 4. Raw in, raw out: both under this raw worktree.
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
PY=C:/Users/nathan/Source/venv-i962/Scripts/python.exe
RAW=D:/choptuik-i935-raw
OUT=/d/choptuik-i935-raw/I970-win2
S=I903-win2/ks_chain2/leg00_D232.0000_ks291/anm_pin3_D238.1789.npz
F="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --threads 4 --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred"
export PYTHONFAULTHANDLER=1 OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4
cd /d/choptuik-i962/hp || exit 9
log() { echo "970 $* $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $OUT/exits_970.txt; }
[ -f /d/choptuik-i935-raw/$S ] || { log "missing $S"; exit 9; }
log "start main $(git rev-parse --short=8 HEAD), state $S, a0 0.4657, --reseed_qd_bar 1e-21, 4 threads"
t=$(date +%s)
"$PY" -u anm_run.py $RAW $RAW/I970-win2/bar21 --state $S $F --ks 291 --keep_plan 0 --D_max 242 --steps 1 --a0 0.4657 --reseed_qd_bar 1e-21 > $OUT/bar21.log 2>&1
rc=$?
log "anm_run exit $rc wall $(( $(date +%s) - t ))s"
touch $OUT/run.done
exit $rc
