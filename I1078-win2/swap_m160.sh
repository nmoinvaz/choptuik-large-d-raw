#!/bin/bash
# The coordinator's split (2026-11-25, dh370 takes M' 160): when chain1078.py opens its M' 160 step (ends_m160_w0.0002.log),
# stop the chain's tree (root cmd.exe pid 43124, checked by its command line) and start chain2_h0001.py (hmax 0.001 at M' 96).
export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"
O=/d/choptuik-raw-i1078/I1078-win2
st() { echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') $*" >> $O/steps_1078.txt; }
until [ -e $O/ends_m160_w0.0002.log ]; do
  [ -e $O/chain.done ] || ls $O/STOP_* > /dev/null 2>&1 && { st "swap_m160: the chain ended before its M' 160 step; nothing done"; exit 0; }
  sleep 5
done
cl=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter 'ProcessId=43124').CommandLine" | tr -d '\r')
case "$cl" in
  *run_chain.cmd*) MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID 43124 > /dev/null 2>&1; st "swap_m160: chain1078 tree (pid 43124) stopped at the start of its M' 160 step, by the coordinator's split (dh370 takes M' 160)";;
  *) st "swap_m160: pid 43124 is not run_chain.cmd ('${cl:0:60}'); nothing killed, chain2 not started"; exit 1;;
esac
sleep 5
powershell -NoProfile -Command "\$si = New-CimInstance -CimClass (Get-CimClass Win32_ProcessStartup) -ClientOnly -Property @{PriorityClass=[uint32]16384; ShowWindow=[uint16]0}; \$r = Invoke-CimMethod Win32_Process -MethodName Create -Arguments @{CommandLine='cmd.exe /c D:\choptuik-raw-i1078\I1078-win2\run_chain2.cmd'; ProcessStartupInformation=\$si}; 'chain2 pid ' + \$r.ProcessId" | tr -d '\r' | while read l; do st "swap_m160: $l"; done
