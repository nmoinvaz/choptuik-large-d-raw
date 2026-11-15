#!/usr/bin/env bash
# #813 on win2 (the coordinator): kf 41's control circle (R 0.2 at lambda_phys) evaluated on macm3's saved state, with
# #749's command, worktree and build (D:/choptuik-i749 at bd7df22f, #551's modecount_cx, venv-t126), 6 threads beside
# #343. win2's own saved state is moved aside for the run and put back after it. Then compare813.py.
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
HP=/d/choptuik-i749/hp
R=/d/choptuik-large-d-raw/I813-win2
ST=modecount_state_D61.0264_M48_kf41.npz
OWN=modecount_state_D61.0264_M48_kf41_win2own.npz
PYD=modecount_cx/build/modecount_cx.cp312-win_amd64.pyd
log() { echo "813 $1 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_813.txt; }
cd "$HP" || exit 9
[ "$(git rev-parse --short=8 HEAD)" = "bd7df22f" ] || { log "worktree D:/choptuik-i749 is not at bd7df22f"; exit 9; }
cmp -s $PYD /d/choptuik-i551/hp/$PYD || { log "modecount_cx differs from #551's build"; exit 9; }
[ "$(md5sum $R/macm3_state/$ST | cut -c1-32)" = "106886f37685b762bb4e948c26dc7474" ] || { log "macm3's state has another md5"; exit 9; }
[ -f data/$OWN ] && { log "data/$OWN exists already: a run did not finish; put it back by hand first"; exit 9; }
export PYTHONFAULTHANDLER=1
[ -f data/$ST ] && mv data/$ST data/$OWN
cp $R/macm3_state/$ST data/$ST
mkdir -p $R/control/data
log "control start on macm3's state"
t=$(date +%s)
"$PY" -u modecount_circle.py data/seeds/local/up23_D61.0264.npz 2.043532530673195,0,0.2 --M=48 --kf=41 --n0=20 \
   --fmax=1e-15 --tag=D61.0264_M48_kf41 --ball=320 --threads=6 --data=$R/control/data > $R/control/run.log 2>&1
log "control exit $? wall $(( $(date +%s) - t ))s"
[ -f data/$OWN ] && mv data/$OWN data/$ST
log "win2's own state put back: $(md5sum data/$ST | cut -c1-32)"
"$PY" -I $R/compare813.py /d/choptuik-large-d-raw > $R/compare813.txt 2>&1
log "compare exit $?"
