#!/bin/bash
# sends the coordinator an hc line at the main events of steps.txt (a Krawczyk verdict, H1, lemma 6a, H2, the inclusion, the cross-load, a STOP, the end); runs from the runner session's shell, where hc works
F=/home/nathan/Source/choptuik-large-d-raw/I1079-dh610; T5="nathans-macbook-air-m5-3/t5"
timeout 86400 tail -n0 -F $F/steps.txt | while read -r line; do
  case "$line" in
    *"point run:"*|*"margins "*|*"PASS: exc"*|*"H1: exit"*|*"lemma 6a: exit"*|*"lemma 6a controls"*|*"H2: probe"*|*"incl done"*|*"theorem_A_sets_M.py"*end*|*"cross-load"*|*"xload done"*|*"chain done"*|*"h2 done"*|*"STOP:"*|*"run_all:"*) hc send "$T5" "dh610 #1079 (auto): ${line:0:900}";;
  esac
  case "$line" in *"run_all: all stages done"*|*"STOP:"*|*"run_all: a STOP"*) break;; esac
done
