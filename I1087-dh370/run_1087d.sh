#!/bin/bash
# #1087 T2, amendment 3 (t5): the starting |F| at order K from the documented "base:" line (--tol 1e40: the double-double gate then passes, the
# line prints the octo-double max|F| of the stored state at order K before any step); each rung ends by TERM to its exact pid at that line.
#   (i)  as is: the chain's own worktree 966g (299728b7), "base: double-double |F| ..., octo-double max|F| X" line.
#   (ii) with --reseed_base 1: worktree 1087 (299728b7 + the --reseed_base change of 276aa1cd, blob 7e34d721), "base re-seeded at ks K ...
#        octo-double max|F| Fr" line; its own "base:" line before the re-seed is a second reading of (i).
# Controls: C1 K 293 (i) with --keep_plan 1 must read 1.0e-38 to 1.1e-38 (the chain stops otherwise); C2 K 293 (ii) with --tol_od 1e-40 (so the
# polish and with it the re-seed run at the state's own order): information. Then K 315 330 360 420 with --keep_plan 0, (i) then (ii) per K.
# 4 threads, nice 10, cap 3600 s each. results.txt gets one row per rung.
{
D=/home/nathan/Source/choptuik-large-d-raw-wt613/I1087-dh370
H966=/home/nathan/Source/choptuik-large-d-966g/hp
H1087=/home/nathan/Source/choptuik-large-d-1087/hp
cd $D || exit 9
note() { echo "$(date -u '+%F %T') UTC $*" >> results.txt; }
# rung K TAG KP HP STOPRE TO CODEBLOB -- extra anm_run args
rung() {
  local K=$1 TAG=$2 KPV=$3 HPV=$4 SRE=$5 TOV=$6 CB=$7; shift 8
  BP=1 KP=$KPV HP=$HPV STOPRE=$SRE TO=$TOV CODEBLOB=$CB bash $D/run_rung.sh $K $TAG 3600 "$@" > /dev/null 2>&1
  local S H
  S=$(sed -nE 's/.*seconds to that point ([0-9]+);.*/\1/p' $D/ks${K}_$TAG/rung.txt)
  H=$(sed -nE 's/.*ended by: (.*); seconds.*/\1/p' $D/ks${K}_$TAG/rung.txt)
  note "K $K $TAG (keep_plan $KPV): ended by $H after $S s"
  grep -E '^base: double-double|^base re-seed' $D/ks${K}_$TAG/stdout.log | cut -c1-330 | sed 's/^/    /' >> results.txt
}
note "start of amendment 3: K 293 controls, then K 315 330 360 420, (i) and (ii) each, --tol 1e40"
rung 293 c1_i 1 $H966 '^base: double-double' 2e-34 "" -- --tol 1e40
A=$(grep -m1 '^base: double-double' ks293_c1_i/stdout.log | sed -E 's/.*octo-double max\|F\| ([0-9.e+-]+) .*/\1/')
case "$A" in 1.0e-38|1.1e-38) note "CONTROL C1 K 293 (i), keep_plan 1: $A is within 1.0e-38 to 1.1e-38: passes";;
  *) note "CONTROL C1 K 293 (i): '$A' is not 1.0e-38 to 1.1e-38: stop"; echo stop > STOP.txt; exit 1;; esac
rung 293 c2_ii 1 $H1087 '^base re-seed' 1e-40 7e34d721 -- --tol 1e40 --reseed_base 1
for K in 315 330 360 420; do
  rung $K b_i 0 $H966 '^base: double-double' 2e-34 "" -- --tol 1e40
  rung $K b_ii 0 $H1087 '^base re-seed' 2e-34 7e34d721 -- --tol 1e40 --reseed_base 1
done
note "done"
exit 0
}
