#!/usr/bin/env bash
# #780: complex_imag_dd.py at the double counts' points (dd 0: only the light-cone block and the LU differ from
# complex_imag.py), the windings over those values, and a sample in full double-double (dd all).
# Usage: run.sh RAWDIR I95_IMAG_DIR, from solver/matter/ of wip/i780. One process, nice 10.
set -u
R=$1
E=$2
PY=${PY:-python3}
ST=../../hp/data/states
date -u '+start %Y-%m-%d %H:%M:%S UTC' > "$R/run.log"
git rev-parse HEAD >> "$R/run.log"
for p in up2_D20.0437:D20 up_D10.0000:D10; do
  s=${p%%:*}; d=${p##*:}
  nice -n 10 $PY i780_compare.py $ST/$s.npz $E/evals_$d.jsonl --dd=0 --out="$R/dd0_$d.jsonl" > "$R/dd0_$d.log" 2>&1
  echo "dd0 $d exit $? $(date -u '+%H:%M:%S')" >> "$R/run.log"
done
for p in up2_D20.0437:D20 up_D10.0000:D10; do
  s=${p%%:*}; d=${p##*:}
  nice -n 10 $PY complex_imag_dd.py count $ST/$s.npz B0 U0 FULL --dd=0 --rtol=1e-11 --evlog="$R/dd0_$d.jsonl" \
      --out="$R/counts_dd0.jsonl" > "$R/count_dd0_$d.log" 2>&1
  echo "count dd0 $d exit $? $(date -u '+%H:%M:%S')" >> "$R/run.log"
done
for p in up2_D20.0437:D20 up_D10.0000:D10; do
  s=${p%%:*}; d=${p##*:}
  nice -n 10 $PY i780_compare.py $ST/$s.npz $E/evals_$d.jsonl --dd=all --tol=1e-14 --stride=30 \
      --out="$R/ddall_$d.jsonl" > "$R/ddall_$d.log" 2>&1
  echo "ddall $d exit $? $(date -u '+%H:%M:%S')" >> "$R/run.log"
done
date -u '+end %Y-%m-%d %H:%M:%S UTC' >> "$R/run.log"
