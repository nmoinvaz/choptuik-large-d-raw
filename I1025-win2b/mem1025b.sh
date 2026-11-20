#!/usr/bin/env bash
# #1025 memory watch, second version (coordinator's hc ~06:46 UTC: D 16.25 stopped; "if commit passes 97 GiB, stop D 16.75 too and tell me"). Every 30 s it appends "UTC free, commit/limit, tree of the running solves, largest rustc" to mem_1025.log.
# Commit over 97 GiB: stops one solve (the D 16.25 solve if it is running, else the D 16.75 solve; its tree, by the exact root pid found by rootpid1025.ps1, after checking its command line), sends the coordinator an hc, and goes on
# (so a second solve is stopped at the next check if commit is still over 97 GiB). Free physical memory under 4 GiB: one hc, no kill. Ends quietly when no solve of the two is running. usage: bash mem1025b.sh
X=/d/choptuik-large-d-raw/I1025-win2b
P=D:/choptuik-large-d-raw/I1025-win2b
sent=0
while true; do
  ra=$(powershell -NoProfile -File "$P/rootpid1025.ps1" -Pat l1kc55Fv1025 | tr -d '\r')
  rb=$(powershell -NoProfile -File "$P/rootpid1025.ps1" -Pat l1kc55Fu1025 | tr -d '\r')
  r=$(powershell -NoProfile -File "$P/mem1025b.ps1" -Root ${ra:-0} | tr -d '\r'); set -- $r
  free=$1; com=$2; lim=$3; wa=$4; rs=$6
  wb=$(powershell -NoProfile -File "$P/mem1025b.ps1" -Root ${rb:-0} | tr -d '\r' | awk '{print $4"/"$5}')
  echo "$(date -u '+%Y-%m-%d %H:%M:%S') free $free GiB commit $com/$lim GiB D16.75 $wa GiB(pid ${ra:--}) D16.25 $wb GiB(pid ${rb:--}) rustc $rs GiB" >> $X/mem_1025.log
  [ -z "$ra" ] && [ -z "$rb" ] && break
  if [ "$(awk "BEGIN{print ($com>97)}")" = "1" ]; then
    if [ -n "$rb" ]; then v=$rb; tag=l1kc55Fu1025; nm="D 16.25"; else v=$ra; tag=l1kc55Fv1025; nm="D 16.75"; fi
    cl=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"ProcessId=$v\").CommandLine" | tr -d '\r')
    case "$cl" in
      *ell_refine.py*$tag*) MSYS2_ARG_CONV_EXCL='*' taskkill /T /F /PID $v > /dev/null 2>&1; act="stopped the $nm solve (tree of pid $v, by exact pid)";;
      *) act="$nm pid $v is not its command, nothing stopped";;
    esac
    echo "$(date -u '+%Y-%m-%d %H:%M:%S') COMMIT OVER 97 GiB ($com of $lim): $act" >> $X/mem_1025.log
    echo "1025 commit passed 97 GiB ($com of $lim): $act $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $X/exits_1025.txt
    hc send nathans-macbook-air-m5-3/t5 "win2b to coordinator, #1025: commit on win2 passed 97 GiB ($com of $lim GiB, free $free GiB, rustc $rs GiB) at $(date -u '+%H:%M') UTC: $act. Log: I1025-win2b/mem_1025.log." > /dev/null 2>&1
  elif [ "$sent" = 0 ] && [ "$(awk "BEGIN{print ($free<4)}")" = "1" ]; then
    sent=1
    hc send nathans-macbook-air-m5-3/t5 "win2b to coordinator, #1025: free physical memory on win2 is $free GiB (below 4) at $(date -u '+%H:%M') UTC, commit $com of $lim GiB, rustc $rs GiB. No solve stopped by this (the commit rule governs). Log: I1025-win2b/mem_1025.log." > /dev/null 2>&1
    echo "$(date -u '+%Y-%m-%d %H:%M:%S') free under 4 GiB ($free), hc sent, nothing killed" >> $X/mem_1025.log
  fi
  sleep 30
done
