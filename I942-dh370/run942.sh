#!/bin/bash
# #942 on dh370: hpkernel's pinned quad-double solve (hp/qd_window.py --mode pinned on T84-mac/pin5_D71.0000.npz), the
# 4.8.2 build of the #935 worktree. One run is one jsonl, one log and one saved state, all in the arm's folder.
#   run942.sh a   30 runs one after another at --threads 2 on an idle machine, then the control run (start perturbed)
#   run942.sh b   30 runs at --threads 2, 24 at once, then the other 6
#   run942.sh c   30 runs at --threads 1, 24 at once, then the other 6
#   run942.sh p   one run, the pilot: its time and memory size the concurrent arms
WT=/home/nathan/Source/choptuik-large-d-935
RAW=/home/nathan/Source/choptuik-large-d-raw-wt613
OUT=$RAW/I942-dh370
ST=$RAW/T84-mac/pin5_D71.0000.npz
PY=$WT/.venv/bin/python
arm=$1
d=$OUT/$arm
mkdir -p "$d"
# one NAME THREADS [WRAPPER ARGS...]: the run's files are $d/NAME.{jsonl,log,npz}
one() {
  local n=$1 th=$2; shift 2
  mkdir -p "$d/st_$n"
  echo "start $(date -u '+%F %T') load $(cut -d' ' -f1-3 /proc/loadavg) threads $th" > "$d/$n.log"
  ( cd "$WT/hp" && nice -n 10 /usr/bin/time -f "time %e s, max rss %M kB" "$PY" -u "$@" "$d/$n.jsonl" "$ST" --mode pinned \
      --threads "$th" --states "$d/st_$n" ) >> "$d/$n.log" 2>&1
  echo "exit $? $(date -u '+%T')" >> "$d/$n.log"
  mv "$d/st_$n/pin5_D71.0000_pinned.npz" "$d/$n.npz" 2>/dev/null
  rmdir "$d/st_$n" 2>/dev/null
}
batch() { # first last threads: runs first..last at once
  local i
  for i in $(seq "$1" "$2"); do one "$(printf r%02d "$i")" "$3" qd_window.py & done
  wait
}
echo "arm $arm start $(date -u '+%F %T') $(git -C "$WT" rev-parse --short HEAD)" >> "$OUT/exits_942.txt"
case $arm in
  p) one r00 2 qd_window.py ;;
  a) for i in $(seq 1 30); do one "$(printf r%02d "$i")" 2 qd_window.py; done
     one ctl 2 "$OUT/qd_window_perturb.py" 1 "$d/ctl_perturb.json" ;;
  b) batch 1 24 2; batch 25 30 2 ;;
  c) batch 1 24 1; batch 25 30 1 ;;
esac
echo "arm $arm done $(date -u '+%F %T')" >> "$OUT/exits_942.txt"
