#!/bin/bash
# #1025 kc79_far (dh610) lane_compare.sh D: the coordinator's order of 24 Nov (hc): at a D that the tag g leap also reaches, no lambda_1 scan; the two states' Delta, |F|, steps and constraint side by side (two continuation
# paths to one D and k_c: the state reproducibility). Steps (a failing one stops the lane): pins (in/ readers, worktrees, g/in_blobs.txt and i/in_blobs.txt); selftests (kc79_syscheck 0; compare_states 0 and --mutate 1);
# FARDIR (env) is for the tests. kc79_syscheck_1025.py on each state and record (exit 0; --mutate=F and --mutate=steps exit 1; the same check the leg lane runs); compare_states.py -> compare.txt; push.
{
set -u
D=$1
RAW=/home/nathan/Source/choptuik-large-d-raw; FAR=$RAW/I1025-dh610/kc79_far; F=${FARDIR:-$FAR/D$D}; IN=$FAR/in
WT=/home/nathan/Source/choptuik-large-d-1025g; WTM=$WT/solver/matter; PY=/home/nathan/Source/venv-i1058/bin/python
L=$F/exits_far.txt; PUSH=/tmp/claude-1000/-home-nathan-Source-choptuik-large-d/4ef2cfd3-77e8-4b1b-9eda-6fb9da54dcb9/scratchpad/push_folder.sh
export PYTHONDONTWRITEBYTECODE=1
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC kc79_far D $D: $*" | tee -a $L; }
blob() { git hash-object --no-filters "$1"; }
stop() { say "STOP: $*"; exit 1; }
mkdir -p $F/src
bad=0
while read bb f; do [ -f $IN/$f ] && [ "$(blob $IN/$f)" = "$bb" ] || { say "refuse: $IN/$f missing or not blob $bb"; bad=1; }; done < $FAR/in_blobs.txt
for t in g i; do while read bb f; do [ -f $F/$t/in/$f ] && [ "$(blob $F/$t/in/$f)" = "$bb" ] || { say "refuse: $F/$t/in/$f missing or not blob $bb"; bad=1; }; done < $F/$t/in_blobs.txt; done
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 48c36355 ] || { say "refuse: $WT is not at 48c36355"; bad=1; }
for f in dss_ell ell_ddm ell_dd ddnp; do git -C $WT diff --quiet 505d8399 HEAD -- solver/matter/$f.py || { say "refuse: $f.py differs from 505d8399"; bad=1; }; done
[ $bad = 0 ] || exit 2
say "pins checked (in/ readers, g/ and i/ in_blobs.txt, worktree 1025g 48c36355, compare_states.py blob $(blob $FAR/compare_states.py | cut -c1-8), load $(cut -d' ' -f1-3 /proc/loadavg), $($PY -V 2>&1))"
( cd $IN; $PY -I kc79_syscheck_1025.py --selftest > $F/selftest_kc79_syscheck.log 2>&1; a0=$?
  cd $FAR; $PY -I compare_states.py selftest > $F/selftest_compare.log 2>&1; c0=$?
  $PY -I compare_states.py selftest --mutate > $F/selftest_compare_mutate.log 2>&1; c1=$?
  echo "$a0 $c0 $c1" > $F/selftest_exits.txt )
read -r a0 c0 c1 < $F/selftest_exits.txt
[ "$a0 $c0 $c1" = "0 0 1" ] || stop "the selftests did not behave (kc79_syscheck $a0, compare_states $c0 $c1; wanted 0 0 1)"
say "selftests as wanted (kc79_syscheck, compare_states, its mutate: 0 0 1; the mutate printed: $(grep -c 'control FIRED' $F/selftest_compare_mutate.log) FIRED line)"
for t in g i; do
  TAG=l1kc79Lw1025$t; REC=$F/$t/in/$TAG.jsonl; STATE=$F/$t/in/sol_${TAG}_D$(printf '%.6f' $D).npy
  $PY -I $IN/kc79_syscheck_1025.py $REC $STATE $D $WTM > $F/src/syscheck_$t.txt 2>&1; s=$?
  for m in F steps; do $PY -I $IN/kc79_syscheck_1025.py $REC $STATE $D $WTM --mutate=$m > $F/src/syscheck_${t}_mutate_$m.txt 2>&1; eval "c$m=$?"; done
  say "source check, tag $t: kc79_syscheck_1025.py exit $s; controls --mutate=F exit $cF, --mutate=steps exit $csteps (1 wanted each): $(tail -n 3 $F/src/syscheck_$t.txt | cut -c1-300 | tr '\n' ' ')"
  [ $s = 0 ] && [ $cF = 1 ] && [ $csteps = 1 ] || stop "the tag $t state is not accepted by the k_c 79 check on this build, or a control did not exit 1"
done
( cd $FAR && $PY -I compare_states.py $D $F > $F/compare.txt 2>&1 ); cr=$?
say "compare_states.py exit $cr; compare.txt: $(sed -n '3,12p' $F/compare.txt | cut -c1-200 | tr '\n' ' ' | cut -c1-900)"
[ $cr = 0 ] || stop "compare_states.py exit $cr"
[ -n "${FARDIR:-}" ] || bash $PUSH I1025-dh610/kc79_far/D$D "I1025-dh610/kc79_far/D$D: g and i states side by side" > $F/push_scan.txt 2>&1
say "states compared, no scan (the coordinator's order); far point done"
exit 0
}
