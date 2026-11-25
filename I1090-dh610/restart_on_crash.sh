#!/bin/bash
# restart_on_crash.sh M: the coordinator's order (hc of 25 Nov, from t2v): the run of unit i1090-m$M that has already printed a D line continues until it crashes (the float64 pre-solve of 6e231f5a raises LinAlgError at M >= 10);
# then this script starts the unit again on b88bf1eb (run_dd2.sh: worktree ~/Source/c1090b, fresh folder dd_M${M}_cont2, same flags). A crash is a Python Traceback in the unit's journal; any other end (the 20 h cap, the script's own
# stop after 3 failed refinements, the last D done) does not restart anything: it is only reported. Alert-only otherwise; stops nothing.
M=$1; F=/home/nathan/Source/choptuik-large-d-raw/I1090-dh610; T5="nathans-macbook-air-m5-3/t5"; U=i1090-m$M
t0=$(date '+%F %T'); echo "$(date -u '+%F %T') UTC watching unit $U" >> $F/restart_M$M.txt
while [ "$(systemctl --user is-active $U)" = active ]; do sleep 30; done
tb=$(journalctl --user -u $U --since "$t0" --no-pager 2>/dev/null | grep -c "Traceback")
last=$(journalctl --user -u $U --since "$t0" --no-pager 2>/dev/null | grep -E "Error|Traceback" | tail -n 1 | cut -c1-200)
if [ "$tb" -gt 0 ]; then
  echo "$(date -u '+%F %T') UTC unit $U crashed ($last); starting the run on b88bf1eb into dd_M${M}_cont2" >> $F/restart_M$M.txt
  systemd-run --user --unit=$U --collect /usr/bin/systemd-inhibit --what=sleep:idle --who=dh610 --why=$U bash /home/nathan/Source/choptuik-large-d-raw/I967-dh610/withmem967.sh /tmp/claude-1000/-home-nathan-Source-choptuik-large-d/4ef2cfd3-77e8-4b1b-9eda-6fb9da54dcb9/scratchpad/memlog_${U}_3.log $F/run_dd2.sh $M >> $F/restart_M$M.txt 2>&1
  hc send "$T5" "dh610 i1090 (auto): unit $U crashed ($last); restarted on b88bf1eb into dd_M${M}_cont2 (run_dd2.sh), the old folder dd_M${M}_cont is kept" > /dev/null 2>&1
else
  echo "$(date -u '+%F %T') UTC unit $U ended without a traceback (cap, 3 failed refinements or finished): not restarted" >> $F/restart_M$M.txt
  hc send "$T5" "dh610 i1090 (auto): unit $U ended without a Python traceback (20 h cap, stop after 3 failed refinements, or finished); not restarted; see dd_M${M}_cont/solve_dd_cont.log" > /dev/null 2>&1
fi
