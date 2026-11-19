#!/usr/bin/env bash
# waits for the old-head step_new (pid 798427; its script bash 769643 is SIGSTOPped, so step_old at the old head cannot start), KILLs that script,
# checks that it is gone and that no old-head step_old exists, and only then runs run1032b.sh. On a failed check it stops and writes old_script_check.txt.
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1032-dh370
st() { awk '{print $3}' /proc/$1/stat 2>/dev/null; }
while :; do s=$(st 798427); { [ -z "$s" ] || [ "$s" = Z ]; } && break; sleep 5; done
echo "step_new (old head) ended $(date -u '+%F %T')" > $OUT/step_new_ended.txt
kill -KILL 769643
ok=0
for i in $(seq 1 60); do s=$(st 769643); if [ -z "$s" ] || [ "$s" = Z ]; then ok=1; break; fi; sleep 1; done
{ echo "$(date -u '+%F %T') bash 769643 (old run1032.sh) state after KILL: '${s:-gone}'";
  echo "ps lines for the old script's pid and its parent 769634: $(ps -o pid=,stat= -p 769643,769634 2>&1 | tr '\n' ';')";
  echo "old-head step_old files: $(ls -d $OUT/step_old $OUT/step_old.log 2>/dev/null | tr '\n' ' ')(none = nothing started)"; } > $OUT/old_script_check.txt
if [ $ok = 1 ] && [ -z "$(ls -d $OUT/step_old $OUT/step_old.log 2>/dev/null)" ]; then echo "check passed: old script gone, no step_old" >> $OUT/old_script_check.txt; else echo "CHECK FAILED, round 2 not started" >> $OUT/old_script_check.txt; exit 3; fi
bash $OUT/run1032b.sh
