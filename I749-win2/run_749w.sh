#!/usr/bin/env bash
# #749 on win2 (win2b): the kf 41 half of #708's box at D 61.0264, M 48, with #551's command (one process: the lambda_phys
# control R 0.2 and the four R 0.36 circles, --ball=320), only the cut changed. From hp/ of the worktree D:/choptuik-i749
# at wip/i749 bd7df22f (b5d69cc2 with 672d01b7's modecount_circle.py, positions up to winding 6), with modecount_cx from
# #551's build (D:/choptuik-i551 at 98ee71bd, the same modecount_cx source as b5d69cc2), venv-t126, 10 threads.
# First the planted check of the positions, which must exit 0.
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
HP=/d/choptuik-i749/hp
R=/d/choptuik-large-d-raw/I749-win2
K=41
PYD=modecount_cx/build/modecount_cx.cp312-win_amd64.pyd
cd "$HP" || exit 9
[ "$(git rev-parse --short=8 HEAD)" = "bd7df22f" ] || { echo "worktree D:/choptuik-i749 is not at bd7df22f" >&2; exit 9; }
cmp -s $PYD /d/choptuik-i551/hp/$PYD || { echo "modecount_cx differs from #551's build" >&2; exit 9; }
export PYTHONFAULTHANDLER=1
log() { echo "$1 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_749.txt; }
"$PY" -u modecount_circle_planted.py --controls > $R/planted.log 2>&1; rc=$?
log "749 planted --controls exit $rc (must be 0)"
[ $rc = 0 ] || exit 1
mkdir -p $R/kf$K/data
log "749 kf$K start"
t=$(date +%s)
"$PY" -u modecount_circle.py data/seeds/local/up23_D61.0264.npz 2.043532530673195,0,0.2 2.85,0.25,0.36 3.35,0.25,0.36 2.85,-0.25,0.36 3.35,-0.25,0.36 \
   --M=48 --kf=$K --n0=20 --fmax=1e-15 --tag=D61.0264_M48_kf$K --ball=320 --threads=10 --data=$R/kf$K/data > $R/kf$K/run.log 2>&1
log "749 kf$K exit $? wall $(( $(date +%s) - t ))s"
