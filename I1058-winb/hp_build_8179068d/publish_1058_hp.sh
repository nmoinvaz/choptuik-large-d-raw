#!/bin/bash
# copy the staged #1058 hp-build folder (files only) into the push worktree's I1058-winb/hp_build_8179068d, then commit and push linearly with push_1058_1025.sh
# usage: bash publish_1058_hp.sh "commit message"; stops at the first failing step; read-only on the staging folder
set -euo pipefail
S=/c/Users/nathan/Source/hp1058_winb
W=/c/Users/nathan/Source/choptuik-large-d-raw-754
[ "$(basename "$(git -C "$W" rev-parse --show-toplevel)")" = "choptuik-large-d-raw-754" ]
D=$W/I1058-winb/hp_build_8179068d
mkdir -p "$D/checks"
cp "$S/I1058-winb/hp_build_8179068d/README.md" "$D/"
cp "$S/checks/"*.log "$D/checks/"
for f in hp1058_build.log hp1058b_build.log hp1058b_build_output.log hp1058_build_output.log checks_1058.json mem_1058.csv mem_stats_1058.txt mem_stats_1058.py \
         alerts_1058.log prio_hp_1058.log vcvars.log prep_raw_1058.sh prep_raw_1058.log driver_hp_1058.py driver_hp_1058b.py \
         build_hp_1058.cmd build_hp_1058b.cmd start_hp_1058.cmd start_hp_1058b.cmd start_watchers_1058.cmd start_watchers_1058b.cmd \
         watch_mem_1058.ps1 watch_mem_1058b.ps1 prio_hp_1058.ps1 prio_hp_1058b.ps1 publish_1058_hp.sh; do
  [ -f "$S/$f" ] && cp "$S/$f" "$D/"
done
bash /c/Users/nathan/Source/md510-1025/push_1058_1025.sh "$1"
