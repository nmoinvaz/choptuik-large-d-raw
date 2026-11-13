#!/usr/bin/env bash
# The standing instruction (coordinator, message 1794578121158-0): if #674's arm A converges at 247.043 to #603's state at the same D_str within 1e-40, restart #603 at once, between attempts, from chain_nat's newest
# converged state with --od_strong 4 added (run_603_ns.sh, into chain_ns/). If arm A is refused at 247.043, change nothing. This waits for the arm's exit, checks compare_674.py's output, then waits for the next saved
# state of chain_nat, stops chain_nat there and starts chain_ns from that state with a0 = twice the last accepted a. Decisions and times go to restart_ns.txt.
RAW=/d/choptuik-large-d-raw
R=$RAW/I603-win2
PYT=/c/Users/nathan/Source/venv-t177/Scripts/python.exe
OUT=$R/restart_ns.txt
until grep -q "247.043 armA exit" $RAW/I674-win2/exits_674.txt; do sleep 20; done
echo "arm A at 247.043 exited $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $OUT
cd $RAW/I674-win2 && "$PYT" -I compare_674.py 247.043 A anm_pin3_D248.0194.npz > compare_247.043_armA.txt 2>&1
if grep -q "arm A CONVERGED" compare_247.043_armA.txt && grep -q "equal: True" compare_247.043_armA.txt && grep -q "within 1e-40: True" compare_247.043_armA.txt; then
  echo "arm A converged and its Delta matches #603's within 1e-40: restart between attempts" >> $OUT
else
  echo "arm A at 247.043 did NOT converge or its Delta/D_str does not match: nothing changed" >> $OUT
  exit 0
fi
n0=$(grep -c "Delta of the saved state" $R/chain_nat.log)
until [ "$(grep -c 'Delta of the saved state' $R/chain_nat.log)" -gt "$n0" ]; do sleep 3; done
echo "chain_nat saved a state $(date -u '+%Y-%m-%d %H:%M:%S UTC'): stopping it" >> $OUT
# the launcher python of chain_nat and its children
pid=$(powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object { \$_.CommandLine -match 'anm_run' -and \$_.CommandLine -match 'chain_nat' } | Sort-Object ProcessId | Select-Object -First 1 -ExpandProperty ParentProcessId" | tr -d '\r')
pid2=$(powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object { \$_.CommandLine -match 'anm_run' -and \$_.CommandLine -match 'chain_nat' } | ForEach-Object { \$_.ProcessId } | Sort-Object | Select-Object -First 2" | tr -d '\r' | tr '\n' ' ')
echo "chain_nat python pids: $pid2 (a parent of the first: $pid)" >> $OUT
for p in $pid2; do taskkill //T //F //PID $p >> $OUT 2>&1; done
newest=$(ls $R/chain_nat/anm_pin3_D*.npz | sort -V | tail -n 1)
prev=$(ls $R/chain_nat/anm_pin3_D*.npz | sort -V | tail -n 2 | head -n 1)
[ "$prev" = "$newest" ] && prev=$R/chain/anm_pin3_D253.7313.npz
nw=$(echo "$newest" | sed 's#^/d/#D:/#'); pw=$(echo "$prev" | sed 's#^/d/#D:/#')
A0=$("$PYT" -I -c "
import json, numpy as np
D=lambda p: json.loads(str(np.load(p)['meta']))['D']
a=D('$nw')-D('$pw')
print(repr(2*a))
")
echo "newest $newest previous $prev twice the last accepted a = $A0" >> $OUT
S=${newest#$RAW/}
echo "S=$S" > $R/restart_ns_start.env; echo "A0=$A0" >> $R/restart_ns_start.env
echo "READY: chain_nat stopped; start chain_ns with S=$S A0=$A0 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $OUT
