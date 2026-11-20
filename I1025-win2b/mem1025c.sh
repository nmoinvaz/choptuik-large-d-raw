#!/usr/bin/env bash
# #1025 memory watch, third version, ALERT ONLY (coordinator's hc ~06:50 UTC: Nathan's standing rule is that no watcher kills or stops a process for its memory use; "send me an hc when commit passes 95 GiB and again at 97 GiB,
# and when free falls under 4 GiB, and stop nothing"). Every 30 s it appends "UTC free, commit/limit, tree of each solve, largest rustc" to mem_1025.log. One hc per threshold crossing (commit 95, commit 97, free 4), re-armed when
# commit falls 1.5 GiB below its threshold (free: above 6 GiB), at most one per threshold per 15 min. It never kills or stops anything. Ends quietly when no solve of the two is running. usage: bash mem1025c.sh
X=/d/choptuik-large-d-raw/I1025-win2b
P=D:/choptuik-large-d-raw/I1025-win2b
a95=0; a97=0; a4=0; t95=0; t97=0; t4=0
alert() { # key text
  hc send nathans-macbook-air-m5-3/t5 "win2b to coordinator, #1025 memory alert (alert only, nothing stopped): $1 at $(date -u '+%H:%M') UTC. Free $free GiB, commit $com of $lim GiB, D 16.75 $wa GiB, D 16.25 $wb, rustc $rs GiB. Log: I1025-win2b/mem_1025.log." > /dev/null 2>&1
  echo "$(date -u '+%Y-%m-%d %H:%M:%S') ALERT hc sent: $1" >> $X/mem_1025.log
}
while true; do
  ra=$(powershell -NoProfile -File "$P/rootpid1025.ps1" -Pat l1kc55Fv1025 | tr -d '\r')
  rb=$(powershell -NoProfile -File "$P/rootpid1025.ps1" -Pat l1kc55Fu1025 | tr -d '\r')
  r=$(powershell -NoProfile -File "$P/mem1025b.ps1" -Root ${ra:-${rb:-0}} | tr -d '\r'); set -- $r
  free=$1; com=$2; lim=$3; rs=$6
  wa="-"; wb="-"
  [ -n "$ra" ] && wa=$(powershell -NoProfile -File "$P/mem1025b.ps1" -Root $ra | tr -d '\r' | awk '{print $4}')
  [ -n "$rb" ] && wb=$(powershell -NoProfile -File "$P/mem1025b.ps1" -Root $rb | tr -d '\r' | awk '{print $4}')
  echo "$(date -u '+%Y-%m-%d %H:%M:%S') free $free GiB commit $com/$lim GiB D16.75 $wa GiB(pid ${ra:--}) D16.25 $wb GiB(pid ${rb:--}) rustc $rs GiB" >> $X/mem_1025.log
  [ -z "$ra" ] && [ -z "$rb" ] && break
  now=$(date +%s)
  if [ "$(awk "BEGIN{print ($com>95)}")" = "1" ]; then
    [ "$a95" = 0 ] && [ $((now-t95)) -ge 900 ] && { alert "commit passed 95 GiB"; a95=1; t95=$now; }
  elif [ "$(awk "BEGIN{print ($com<93.5)}")" = "1" ]; then a95=0; fi
  if [ "$(awk "BEGIN{print ($com>97)}")" = "1" ]; then
    [ "$a97" = 0 ] && [ $((now-t97)) -ge 900 ] && { alert "commit passed 97 GiB"; a97=1; t97=$now; }
  elif [ "$(awk "BEGIN{print ($com<95.5)}")" = "1" ]; then a97=0; fi
  if [ "$(awk "BEGIN{print ($free<4)}")" = "1" ]; then
    [ "$a4" = 0 ] && [ $((now-t4)) -ge 900 ] && { alert "free physical memory under 4 GiB"; a4=1; t4=$now; }
  elif [ "$(awk "BEGIN{print ($free>6)}")" = "1" ]; then a4=0; fi
  sleep 30
done
