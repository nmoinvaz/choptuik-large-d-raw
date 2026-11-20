#!/usr/bin/env bash
# #1025 memory watch (coordinator's hc: "if free memory falls below 4 GB, stop the D 16.25 solve first and tell me"). Every 60 s it appends "UTC free GiB, tree GiB/procs of D 16.75 and D 16.25" to mem_1025.log. If free physical
# memory is below 4 GiB it stops the D 16.25 solve (its tree, by the exact pid in D16.25.winpid, after checking the command line holds ell_refine.py and l1kc55Fu1025), sends the coordinator one hc and exits. It ends quietly when both trees are gone.
# usage: bash mem1025.sh
X=/d/choptuik-large-d-raw/I1025-win2b
ra=$(cat $X/D16.75.winpid); rb=$(cat $X/D16.25.winpid)
while true; do
  r=$(powershell -NoProfile -File "D:/choptuik-large-d-raw/I1025-win2b/mem1025.ps1" -Root1 $ra -Root2 $rb | tr -d '\r'); set -- $r
  free=$1; wa=$2; na=$3; wb=$4; nb=$5
  echo "$(date -u '+%Y-%m-%d %H:%M:%S') free $free GiB D16.75 $wa GiB/$na D16.25 $wb GiB/$nb" >> $X/mem_1025.log
  [ "${na:-0}" -eq 0 ] && [ "${nb:-0}" -eq 0 ] && break
  if [ "$(awk "BEGIN{print ($free<4)}")" = "1" ]; then
    cl=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"ProcessId=$rb\").CommandLine" | tr -d '\r')
    case "$cl" in
      *ell_refine.py*l1kc55Fu1025*) MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $rb > /dev/null 2>&1; act="stopped the D 16.25 solve (tree of pid $rb, by exact pid)";;
      *) act="D 16.25 solve not running (pid $rb is not its command), nothing stopped";;
    esac
    echo "$(date -u '+%Y-%m-%d %H:%M:%S') FREE UNDER 4 GiB ($free): $act" >> $X/mem_1025.log
    echo "1025 free memory fell to $free GiB (below 4): $act $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/exits_1025.txt
    hc send nathans-macbook-air-m5-3/t5 "win2b to coordinator, #1025 memory: free physical memory on win2 fell to $free GiB (below 4, as you ordered), at $(date -u '+%H:%M') UTC: $act. The D 16.75 solve keeps running. Log: I1025-win2b/mem_1025.log." > /dev/null 2>&1
    break
  fi
  sleep 60
done
