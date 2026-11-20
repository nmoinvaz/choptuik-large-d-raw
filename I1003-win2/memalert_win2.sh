#!/usr/bin/env bash
# win2 memory alert, ALERT ONLY (coordinator's hc ~07:15 UTC 20 Nov: "bring the alert-only memory watches back with" the #1034 build restart, which win2-build starts at once when K 49 ends; Nathan's standing rule: no watcher kills or stops
# a process for its memory use). Every 30 s it appends "UTC free, commit/limit, largest rustc, top 3 processes" to memalert_win2.log. One hc to the coordinator per threshold crossing (commit 95 GiB, commit 97 GiB, free under 4 GiB),
# re-armed when commit falls 1.5 GiB below its threshold (free: above 6 GiB), at most one per threshold per 15 min. While mem1025c.sh (the #1025 watch, same thresholds) is running it only logs, so there is no double alert.
# It kills and stops nothing. It ends when no ell_refine, amp_flint_par, cargo or rustc process has been running for 30 min. usage: bash memalert_win2.sh
X=/d/choptuik-large-d-raw-743/I1003-win2
a95=0; a97=0; a4=0; t95=0; t97=0; t4=0; idle=0
while true; do
  r=$(powershell -NoProfile -Command "
    \$o=Get-CimInstance Win32_OperatingSystem
    \$ps=Get-Process
    \$rs=(\$ps | Where-Object { \$_.ProcessName -eq 'rustc' } | Measure-Object WorkingSet64 -Maximum).Maximum
    \$top=(\$ps | Sort-Object WorkingSet64 -Descending | Select-Object -First 3 | ForEach-Object { \$_.ProcessName + ' ' + [math]::Round(\$_.WorkingSet64/1GB,1) }) -join ', '
    \$n=@(\$ps | Where-Object { \$_.ProcessName -in 'cargo','rustc' }).Count + @(Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object { \$_.CommandLine -like '*ell_refine.py*' -or \$_.CommandLine -like '*amp_flint_par.py*' }).Count
    \$m=@(Get-CimInstance Win32_Process | Where-Object { \$_.CommandLine -like '*mem1025c.sh*' -and \$_.Name -like 'bash*' -and \$_.CommandLine -notlike '*Get-CimInstance*' }).Count
    '{0:N1}|{1:N1}|{2:N1}|{3:N1}|{4}|{5}|{6}' -f (\$o.FreePhysicalMemory/1MB), ((\$o.TotalVirtualMemorySize-\$o.FreeVirtualMemory)/1MB), (\$o.TotalVirtualMemorySize/1MB), (\$rs/1GB), \$n, \$m, \$top
  " | tr -d '\r')
  IFS='|' read free com lim rs n m top <<< "$r"
  echo "$(date -u '+%Y-%m-%d %H:%M:%S') free $free GiB commit $com/$lim GiB rustc ${rs:-0} GiB procs $n 1025watch $m top: $top" >> $X/memalert_win2.log
  alert() {
    echo "$(date -u '+%Y-%m-%d %H:%M:%S') ALERT: $1" >> $X/memalert_win2.log
    [ "$m" -gt 0 ] && return
    hc send nathans-macbook-air-m5-3/t5 "win2b to coordinator, win2 memory alert (alert only, nothing stopped): $1 at $(date -u '+%H:%M') UTC. Free $free GiB, commit $com of $lim GiB, rustc ${rs:-0} GiB; largest processes: $top. Log: I1003-win2/memalert_win2.log." > /dev/null 2>&1
  }
  now=$(date +%s)
  if [ "$(awk "BEGIN{print ($com>95)}")" = "1" ]; then [ "$a95" = 0 ] && [ $((now-t95)) -ge 900 ] && { alert "commit passed 95 GiB"; a95=1; t95=$now; }
  elif [ "$(awk "BEGIN{print ($com<93.5)}")" = "1" ]; then a95=0; fi
  if [ "$(awk "BEGIN{print ($com>97)}")" = "1" ]; then [ "$a97" = 0 ] && [ $((now-t97)) -ge 900 ] && { alert "commit passed 97 GiB"; a97=1; t97=$now; }
  elif [ "$(awk "BEGIN{print ($com<95.5)}")" = "1" ]; then a97=0; fi
  if [ "$(awk "BEGIN{print ($free<4)}")" = "1" ]; then [ "$a4" = 0 ] && [ $((now-t4)) -ge 900 ] && { alert "free physical memory under 4 GiB"; a4=1; t4=$now; }
  elif [ "$(awk "BEGIN{print ($free>6)}")" = "1" ]; then a4=0; fi
  if [ "${n:-0}" -eq 0 ]; then idle=$((idle+1)); else idle=0; fi
  [ "$idle" -ge 60 ] && break
  sleep 30
done
echo "$(date -u '+%Y-%m-%d %H:%M:%S') no ell_refine, amp_flint_par, cargo or rustc for 30 min: watch ends" >> $X/memalert_win2.log
