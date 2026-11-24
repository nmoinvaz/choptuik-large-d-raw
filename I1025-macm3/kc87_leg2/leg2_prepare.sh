#!/bin/bash
# #1025 macm3 kc87_leg2: pin the leg's inputs from raw commits (git cat-file, exact bytes; each blob checked with git hash-object --no-filters), copy the seeds into the worktree's data/.
# usage: bash leg2_prepare.sh   -> in/, pins.txt, seed files in the worktree (cp only if absent; an existing file must have the pinned blob). Exit 1 on any mismatch.
L2=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg2
RAWG=$HOME/Source/choptuik-large-d-raw-1076p
DATA=$HOME/Source/choptuik-large-d-1025m2/solver/matter/data
cd $L2 || exit 9
git -C $RAWG fetch -q
rc=0
: > pins.txt
pin() {  # path-in-raw blob8 destination commit
  git -C $RAWG cat-file blob $4:$1 > $3 || { echo "cannot read $4:$1" | tee -a pins.txt; rc=1; return; }
  got=$(git hash-object --no-filters $3 | cut -c1-8)
  [ "$got" = "$2" ] && s=ok || { s="MISMATCH (wanted $2)"; rc=1; }
  echo "$got  $(basename $3)  <- $4:$1  $s" | tee -a pins.txt
}
CR=$(git -C $RAWG rev-parse --short=8 origin/main)
pin I1025-dh370/kc87_leg/in/leap_guard.py f1fe7c7c in/leap_guard.py $CR
pin I1025-dh370/kc87_leg/in/mode_tracker.py 807c2d95 in/mode_tracker.py $CR
pin I1025-dh610/kc87_d195/in/kc87_syscheck_1025.py 6df5d960 in/kc87_syscheck_1025.py ec9fb489
pin I1025-win/kc79_d19/kc79_syscheck_1025.py 29dce7ea in/kc79_syscheck_1025.py 8e4797ff
pin I1025-dh370/kc87_leg/sol_l1kc87Ldh370_D21.218750.npy dbc66a07 in/sol_l1kc87Ldh370_D21.218750.npy 21042416
pin I1025-dh370/kc87_leg/sol_l1kc87Ldh370_D21.250000.npy 7e88c368 in/sol_l1kc87Ldh370_D21.250000.npy dd401fe8
pin I1025-dh370/kc87_leg/l1kc87Ldh370.jsonl 07eef60f in/l1kc87Ldh370.jsonl dd401fe8
pin I1025-dh370/kc87_leg/tracker_rows.txt "$(git -C $RAWG rev-parse --short=8 dd401fe8:I1025-dh370/kc87_leg/tracker_rows.txt)" in/dh370_tracker_rows.txt dd401fe8
for f in sol_l1kc87Ldh370_D21.218750.npy sol_l1kc87Ldh370_D21.250000.npy l1kc87Ldh370.jsonl; do
  if [ -e $DATA/$f ]; then
    [ "$(git hash-object --no-filters $DATA/$f | cut -c1-8)" = "$(git hash-object --no-filters in/$f | cut -c1-8)" ] && echo "data/$f present, same blob" | tee -a pins.txt || { echo "data/$f present with another blob" | tee -a pins.txt; rc=1; }
  else cp in/$f $DATA/$f && echo "data/$f copied" | tee -a pins.txt; fi
done
python3 - <<'PY' || rc=1
import json
rows = [json.loads(l) for l in open("in/l1kc87Ldh370.jsonl") if l.strip()]
for D, name in ((21.21875, "leg_seedA.jsonl"), (21.25, "leg_seedB.jsonl")):
    r = [x for x in rows if x["D"] == D][-1]
    open(name, "w").write(json.dumps(r) + "\n")
    print("%s: the row of D %r (|F| %.10g, steps %d, n_null %d)" % (name, D, r["F"], r["steps"], r["n_null"]))
PY
exit $rc
