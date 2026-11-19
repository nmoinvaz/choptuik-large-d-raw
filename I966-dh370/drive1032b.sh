#!/usr/bin/env bash
# waits for the old-head step_new (pid 798427, its script bash 769643 is SIGSTOPped so step_old cannot start), ends that script, then runs run1032b.sh.
while :; do s=$(awk '{print $3}' /proc/798427/stat 2>/dev/null); [ -z "$s" ] || [ "$s" = Z ] && break; sleep 5; done
echo "step_new (old head) ended $(date -u '+%F %T')" > /home/nathan/Source/choptuik-large-d-raw-wt613/I1032-dh370/step_new_ended.txt
kill -KILL 769643
bash /home/nathan/Source/choptuik-large-d-raw-wt613/I1032-dh370/run1032b.sh
