#!/bin/bash
# #1025 kc127_d22875 (t5's order, 25 Nov): run_regrid.sh (regrid to k_c 119 -> 127, accepted only by the checks), then, if VERDICT.txt says ACCEPTED, a memory gate and run_scan.sh.
# The gate (dh610's idea): the scan starts when MemAvailable is at least 17000 MiB (3 procs x 4.5 GiB, my k_c 119 scan processes peaked at 3.97 GiB, + 3.5 GiB); it waits at most 6 h,
# polling each 60 s, and then stops with a report. Nothing is stopped or killed for memory. Exit codes go to exits_k127.txt. A systemd user unit under systemd-inhibit.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1025-dh370/kc127_d22875
cd $OUT || exit 9
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps.txt; }
bash $OUT/run_regrid.sh; rc=$?
echo "regrid $rc" >> $OUT/exits_k127.txt
grep -q '^ACCEPTED' $OUT/VERDICT.txt 2>/dev/null || { step "LANE STOP: no ACCEPTED verdict (run_regrid.sh exit $rc): no scan"; exit 1; }
t0=$(date +%s)
while true; do
  av=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo)
  [ "$av" -ge 17000 ] && break
  [ $(( $(date +%s) - t0 )) -ge 21600 ] && { step "LANE STOP: MemAvailable stayed under 17000 MiB for 6 h (now $av): no scan"; exit 1; }
  [ -e $OUT/gate_waiting ] || { step "scan gate: MemAvailable $av MiB is under 17000; waiting (up to 6 h)"; echo $av > $OUT/gate_waiting; }
  sleep 60
done
step "scan gate passed: MemAvailable $av MiB (waited $(( $(date +%s) - t0 )) s)"
bash $OUT/run_scan.sh; rc=$?
echo "scan $rc" >> $OUT/exits_k127.txt
exit 0
}
