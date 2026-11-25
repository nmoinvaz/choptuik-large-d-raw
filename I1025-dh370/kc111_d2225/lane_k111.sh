#!/bin/bash
# #1025 kc111_d2225 (t5's order, 25 Nov): run_regrid.sh (regrid to k_c 103 -> 111, accepted only by the checks), then, if VERDICT.txt says ACCEPTED, a memory gate and run_scan.sh.
# The gate (dh610's idea): the scan starts when MemAvailable is at least 25000 MiB (5 procs x 4.4 GiB + 3 GiB; dh170's k_c 111 scan points peaked at about 4.3 GiB, my k_c 103 ones at 3.72 GiB); it waits at most 6 h,
# polling each 60 s, and then stops with a report. Nothing is stopped or killed for memory. Exit codes go to exits_k111.txt. A systemd user unit under systemd-inhibit.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1025-dh370/kc111_d2225
cd $OUT || exit 9
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps.txt; }
bash $OUT/run_regrid.sh; rc=$?
echo "regrid $rc" >> $OUT/exits_k111.txt
grep -q '^ACCEPTED' $OUT/VERDICT.txt 2>/dev/null || { step "LANE STOP: no ACCEPTED verdict (run_regrid.sh exit $rc): no scan"; exit 1; }
t0=$(date +%s)
while true; do
  av=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo)
  [ "$av" -ge 25000 ] && break
  [ $(( $(date +%s) - t0 )) -ge 21600 ] && { step "LANE STOP: MemAvailable stayed under 25000 MiB for 6 h (now $av): no scan"; exit 1; }
  [ -e $OUT/gate_waiting ] || { step "scan gate: MemAvailable $av MiB is under 25000; waiting (up to 6 h)"; echo $av > $OUT/gate_waiting; }
  sleep 60
done
step "scan gate passed: MemAvailable $av MiB (waited $(( $(date +%s) - t0 )) s)"
bash $OUT/run_scan.sh; rc=$?
echo "scan $rc" >> $OUT/exits_k111.txt
exit 0
}
