#!/bin/bash
# #1025 kc87_leg: waits for dh610's accepted k_c 87 D 21.0 state on raw origin/main (I1025-dh610/kc87_d21/: VERDICT.txt "ACCEPTED", sol_l1kc87dh610e_D21.0000.npy, l1kc87dh610e.jsonl in one commit), copies it to in/ as seed B,
# records its blobs (in/seedB_state.blob, in/seedB_record.blob, the commit in seedB_commit.txt), checks the record's D (21.0) and Delta against the state's last entry, then starts run_leg.sh (the leg). Polls every 120 s, gives up after 6 h.
# Unit i1025leg87. Log: exits_leg.txt. No hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1025-dh370/kc87_leg
RAWP=/home/nathan/Source/choptuik-large-d-raw-push960
SRC=I1025-dh610/kc87_d21
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
stamp() { date -u '+%F %T'; }
log() { echo "kc87_leg $* $(stamp) UTC" >> $OUT/exits_leg.txt; }
log "waiting for seed B in raw $SRC (poll 120 s, 6 h)"
end=$(( $(date +%s) + 21600 ))
while [ $(date +%s) -lt $end ]; do
  git -C $RAWP pull -q --rebase origin main > /dev/null 2>&1
  if grep -q '^ACCEPTED' $RAWP/$SRC/VERDICT.txt 2>/dev/null && [ -s $RAWP/$SRC/sol_l1kc87dh610e_D21.0000.npy ] && [ -s $RAWP/$SRC/l1kc87dh610e.jsonl ]; then break; fi
  sleep 120
done
grep -q '^ACCEPTED' $RAWP/$SRC/VERDICT.txt 2>/dev/null || { log "STOP: seed B did not appear in 6 h"; exit 1; }
sleep 60; git -C $RAWP pull -q --rebase origin main > /dev/null 2>&1
cp $RAWP/$SRC/sol_l1kc87dh610e_D21.0000.npy $OUT/in/seedB_sol_l1kc87dh610e_D21.0000.npy
cp $RAWP/$SRC/l1kc87dh610e.jsonl $OUT/in/seedB_l1kc87dh610e.jsonl
git hash-object --no-filters $OUT/in/seedB_sol_l1kc87dh610e_D21.0000.npy | cut -c1-8 > $OUT/in/seedB_state.blob
git hash-object --no-filters $OUT/in/seedB_l1kc87dh610e.jsonl | cut -c1-8 > $OUT/in/seedB_record.blob
git -C $RAWP log -1 --format='%h %cI %s' -- $SRC > $OUT/in/seedB_commit.txt
$PY -I - <<PYEOF > $OUT/in/seedB_check.txt 2>&1
import json, numpy as np
r = [json.loads(l) for l in open("$OUT/in/seedB_l1kc87dh610e.jsonl") if l.strip()][-1]
z = np.load("$OUT/in/seedB_sol_l1kc87dh610e_D21.0000.npy")
print("record D", r["D"], "kc", r.get("kc"), "Delta", repr(r["Delta"]), "F", r["F"], "steps", r["steps"], "; state z[-1]", repr(float(z[-1])), "shape", z.shape)
assert r["D"] == 21.0 and r.get("kc") == 87 and abs(float(z[-1]) - r["Delta"]) <= 1e-15
print("seed B: record and state agree")
PYEOF
[ $? = 0 ] || { log "STOP: seed B's record and state disagree: $(cat $OUT/in/seedB_check.txt | tail -1)"; exit 1; }
log "seed B taken: state blob $(cat $OUT/in/seedB_state.blob), record blob $(cat $OUT/in/seedB_record.blob), commit $(cat $OUT/in/seedB_commit.txt | cut -c1-120); $(head -1 $OUT/in/seedB_check.txt | cut -c1-200)"
exec bash $OUT/run_leg.sh
}
