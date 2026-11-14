#!/usr/bin/env bash
# #791: the strip -0.05 < Re lambda < 0.05, |Im lambda| < 9 at settings A and B, then the zeros near 0 and +-i omega.
# Usage: run.sh RAWDIR, from solver/matter/ of wip/i791. One process at a time, nice 10.
set -u
R=$1
PY=${PY:-python3}
B="--box=-0.05,0.05,-9,9"
SA=""
SB="--r0=0.11 --r1=0.25 --alpha=0.3"
{ date -u '+start %Y-%m-%d %H:%M:%S UTC'; git rev-parse HEAD
  $PY css_inf_count.py selftest; echo "selftest exit $?"
  $PY css_inf_count.py selftest --mutate=coarse; echo "selftest control exit $? (must be 1)"; } > "$R/selftest.log" 2>&1
for s in A B; do
  if [ $s = A ]; then SET=$SA; else SET=$SB; fi
  nice -n 10 $PY css_inf_count.py count $B $SET --evlog="$R/evals_$s.jsonl" --out="$R/counts.jsonl" \
      > "$R/count_$s.log" 2>&1; echo "exit $?" >> "$R/count_$s.log"
  nice -n 10 $PY css_inf_count.py count $B $SET --plant=0.02+6j --evlog="$R/evals_$s.jsonl" --out="$R/counts.jsonl" \
      > "$R/count_${s}_plant.log" 2>&1; echo "exit $?" >> "$R/count_${s}_plant.log"
  date -u "+setting $s counted %H:%M:%S UTC" >> "$R/selftest.log"
done
for s in A B; do
  if [ $s = A ]; then SET=$SA; else SET=$SB; fi
  # lambda = 0 with the default absolute tolerance; +-i omega with 1e-16 (the default stalls there, #781)
  nice -n 10 $PY css_inf_count.py locate 0.02+0.01j $SET --target=0 --out="$R/locate.jsonl" > "$R/locate_${s}.log" 2>&1
  echo "exit $?" >> "$R/locate_${s}.log"
  nice -n 10 $PY css_inf_count.py locate 0.02+3.97j 0.02-3.97j $SET --target=iw,-iw --atol=1e-16 \
      --out="$R/locate.jsonl" >> "$R/locate_${s}.log" 2>&1
  echo "exit $?" >> "$R/locate_${s}.log"
done
date -u '+end %Y-%m-%d %H:%M:%S UTC' >> "$R/selftest.log"
