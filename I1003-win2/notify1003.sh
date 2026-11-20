#!/usr/bin/env bash
# #1003: tells win2-build (hc t1w) and the coordinator the moment K 49 J 1500 ends (coordinator's hc ~07:10 UTC 20 Nov: the #1034 build stays stopped until K 49 ends, then win2-build restarts it; "tell win2-build the moment K 49 ends").
# Read only. Trigger: a new line "K 49 J 1500 exit" or "cap of" in exits_1003.txt (written by run1003k49.sh), or the launcher stub (pid in k49.winpid) gone. Then it waits up to 90 s for the amp_flint_par processes to be gone, reads the exit line,
# whether the final JSON exists, free and commit memory, and sends one hc to t1w and one to the coordinator. It kills nothing. usage: bash notify1003.sh
X=/d/choptuik-large-d-raw-743/I1003-win2
stub=$(cat $X/k49.winpid)
n0=$(wc -l < $X/exits_1003.txt)
while true; do
  if tail -n +$((n0+1)) $X/exits_1003.txt | grep -aqE "K 49 J 1500 exit|cap of"; then break; fi
  alive=$(powershell -NoProfile -Command "if (Get-Process -Id $stub -ErrorAction SilentlyContinue) {'yes'} else {'no'}" | tr -d '\r')
  [ "$alive" = no ] && break
  sleep 30
done
for i in 1 2 3; do
  n=$(powershell -NoProfile -Command "@(Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object { \$_.CommandLine -like '*amp_flint_par.py*' }).Count" | tr -d '\r')
  [ "$n" = 0 ] && break
  sleep 30
done
ex=$(tail -n +$((n0+1)) $X/exits_1003.txt | grep -aE "K 49 J 1500 exit|cap of" | tail -n 2 | cut -c1-200 | tr '\n' ';')
fin=no; [ -s $X/sigF_w1.0000_K49_J1500_p1280.json ] && fin=yes
mem=$(powershell -NoProfile -Command "\$o=Get-CimInstance Win32_OperatingSystem; ('free {0:N1} GiB, commit {1:N1} of {2:N1} GiB' -f (\$o.FreePhysicalMemory/1MB), ((\$o.TotalVirtualMemorySize-\$o.FreeVirtualMemory)/1MB), (\$o.TotalVirtualMemorySize/1MB))" | tr -d '\r')
t=$(date -u '+%H:%M:%S UTC 20 Nov')
echo "$t K 49 ended notice: amp_flint_par processes left $n, exit lines: $ex final json $fin, $mem" >> $X/notify1003.log
hc send t1w "win2b to win2-build: #1003 K 49 J 1500 has ENDED ($t). amp_flint_par processes left: $n (0 means its python tree is gone). Exit lines: $ex Final JSON written: $fin. Memory now: $mem. The coordinator said the #1034 build was stopped by hand until K 49 ends and that you restart it then. My #1025 solves keep running beside you: two ell_refine python (D:/choptuik-i1025b, D 16.75 and D 16.25, 4 BLAS threads each, about 0.5 GiB working set each now, 2-3 GB expected, BelowNormal); leave them alone. I do not touch your build." > /dev/null 2>&1 || hc send desktop-pc/t1w "win2b to win2-build: #1003 K 49 J 1500 has ENDED ($t); amp_flint_par processes left: $n; exit lines: $ex final JSON: $fin; $mem. The coordinator said you restart the #1034 build when K 49 ends. My #1025 solves (two ell_refine python) keep running; leave them." > /dev/null 2>&1
hc send nathans-macbook-air-m5-3/t5 "win2b: #1003 K 49 J 1500 has ENDED ($t); amp_flint_par processes left: $n; exit lines: $ex final JSON: $fin; $mem. win2-build has been told (hc t1w). I now run the closing comparison." > /dev/null 2>&1
echo "$(date -u '+%H:%M:%S') notices sent" >> $X/notify1003.log
