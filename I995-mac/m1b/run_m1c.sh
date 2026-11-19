#!/bin/bash
# I995-mac m1b ladder: recount the M = 1 count's unresolved cells at xi1 0.2, then 0.25, then 0.3; code 42d2d58e
cd /Users/nathan/Source/choptuik-large-d-995/solver/inner_stokes
PY=/Users/nathan/venv-314/bin/python
OUT=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/c1624759-29b0-41ee-b1ba-c50f07eff81b/scratchpad/raw983/I995-mac/m1b
n=0; until grep -q "== plant exit" /private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/c1624759-29b0-41ee-b1ba-c50f07eff81b/scratchpad/raw983/I995-mac/logs/m1b.log || [ $n -ge 1440 ]; do sleep 15; n=$((n+1)); done
echo "== ladder start $(date -u '+%F %T')"
prev=$OUT/leaves_M1_full.jsonl
for rung in "0.2 0.25" "0.25 0.3" "0.3 0.25"; do
  set -- $rung
  gtimeout 3h nice -n 10 $PY -u argcount.py --M=1 --recount=$prev --r1=$1 --r1b=$2 --procs=2 --out=$OUT --tag=M1_full_r$1 2>&1 | grep -v -i "userwarning\|super().__init"
  echo "== rung $1 exit ${PIPESTATUS[0]} $(date -u '+%F %T')"
  prev=$OUT/leaves_M1_full_r$1.jsonl
done
echo "== ladder end $(date -u '+%F %T')"
