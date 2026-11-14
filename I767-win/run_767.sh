#!/usr/bin/env bash
# #767 on the win laptop: amp_flint_par.py at wf 1.09 and 1.11, K 15, J 1500, 1280 bits, --procs 3, --fit phys --mf 6:12,
# from the worktree C:/Users/nathan/Source/choptuik-i767 at 188853c5 (#82's summation order, before #246), venv-t151
# (python-flint 0.9.0, FLINT 3.6.0). Then compare_767.py against #82's K 45 files of win2, taken from origin/main into
# C:/Users/nathan/scratch767 so the live raw clone is not pulled.
PY=/c/Users/nathan/Source/venv-t151/Scripts/python.exe
RAW=/c/Users/nathan/Source/choptuik-large-d-raw; R=$RAW/I767-win
B=/c/Users/nathan/scratch767
mkdir -p $B
log() { echo "767 $1 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_767.txt; }
git -C $RAW fetch -q origin
for w in 1.09 1.10 1.11; do git -C $RAW show origin/main:I82-win2/sigF_w${w}_K45_J1500_p1280.json > $B/K45_w$w.json; done
cd /c/Users/nathan/Source/choptuik-i767/solver/inner_amp || exit 9
[ "$(git rev-parse --short=8 HEAD)" = "188853c5" ] || { echo "worktree is not at 188853c5" >&2; exit 9; }
log "start, $("$PY" -c 'import flint; print("python-flint", flint.__version__, "FLINT", flint.__FLINT_VERSION__)')"
"$PY" -I $R/compare_767.py --selftest > $R/selftest_767.txt 2>&1; rc=$?
log "selftest exit $rc (must be 0)"
[ $rc = 0 ] || exit 1
for w in 1.09 1.11; do
  log "wf $w start"
  "$PY" -u amp_flint_par.py $w 15 1500 1280 --procs 3 --fit phys --mf 6:12 --out $R/sigF_w${w}_K15_J1500_p1280.json > $R/amp_w$w.log 2>&1
  log "wf $w exit $?"
done
"$PY" -I $R/compare_767.py $R $B > $R/compare_767.txt 2>&1; log "compare exit $? (must be 0)"
log "all done"
