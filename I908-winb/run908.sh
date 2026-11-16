#!/bin/bash
# #908 on winb (the coordinator), for Git Bash: every run of I427-mac (#427), then #866, #869, #870, #877 and #878, from solver/proof/
# of a worktree at main. Adapted from I427-mac/run_i427.sh; the output folder is I908-winb; adapted from run901.sh (#901, rpi5).
# Usage: run908.sh <python> <root of the raw-data clone> <worktree at main>. Each line of exits.txt has the run, its exit status, the
# status it must have, its wall time and its command.
PY=$1; ROOT=$2; WT=$3
export PYTHONUTF8=1
cd $WT/solver/proof || exit 9
RAW=$ROOT/I908-winb
mkdir -p $RAW
{ echo "commit $(git rev-parse --short=8 HEAD)"; $PY -c "import flint, sys, platform; print('python-flint', flint.__version__, 'FLINT', flint.__FLINT_VERSION__, platform.platform(), 'python', sys.version.split()[0])"; } > $RAW/env.txt 2>&1
RAY=$ROOT/I38-macm3/lemma6b1_runs_M5_cert/ray.json
RAYW=$ROOT/I121-win2/lemma6b1_runs_M5_cert/ray.json
: > $RAW/exits.txt
run() {   # run <log name> <expected exit> <command...>
  local log=$1 want=$2; shift 2
  local t0=$(date +%s)
  "$@" > $RAW/$log.log 2>&1
  local rc=$?
  echo "$log: exit $rc (must be $want), $(( $(date +%s) - t0 )) s: $*" | sed "s|$PY|python3|; s|$ROOT/|RAW/|g" >> $RAW/exits.txt
}
START="--start --rho0=405 --h=1e-18 --cauchy=1e-3"
# planted truth: the linear problem against Kummer's U, at the start point and at the edge |z| = R of the domain
for M in 1 3 5; do run planted_M$M 0 $PY fixed_point_M_b.py --planted --M=$M; done
for M in 1 3 5; do run planted_M${M}_edge 0 $PY fixed_point_M_b.py --planted --M=$M --rho0=204.1; done
for m in truth coef radius; do run planted_M5_mut_$m 3 $PY fixed_point_M_b.py --planted --M=5 --mutate=$m; done
# planted: M = 1 against fixed_point.py's start values; the Lipschitz matrices against fixed_point_M.py's
run check_m1 0 $PY fixed_point_M_b_check.py m1
for m in coef sign scale; do run check_m1_mut_$m 3 $PY fixed_point_M_b_check.py m1 --mutate=$m; done
run lip_M1 0 $PY fixed_point_M_b_check.py lip --M=1
run lip_M3 0 $PY fixed_point_M_b_check.py lip --M=3
run lip_M5 0 $PY fixed_point_M_b_check.py lip --M=5
run lip_M5_sector 0 $PY fixed_point_M_b_check.py lip --M=5 --sector=0.2
run lip_M5_mut_drop 3 $PY fixed_point_M_b_check.py lip --M=5 --mutate=drop
# two truncations of the full M = 5 problem
run two_M5_60_105 0 $PY fixed_point_M_b.py --M=5 --two=60,105 --compare=$RAY
run two_M5_95_105 0 $PY fixed_point_M_b.py --M=5 --two=95,105 --compare=$RAY
run two_M5_60_105_mut_forcing 3 $PY fixed_point_M_b.py --M=5 --two=60,105 --compare=$RAY --mutate=forcing
# M = 5: the start set at s0 = 405 e^{-3 i pi/4} against the stored one
run start_M5 0 $PY fixed_point_M_b.py --M=5 $START --compare=$RAY --json=$RAW/start_M5.json
run start_M5_sector 0 $PY fixed_point_M_b.py --M=5 $START --sector=0.2 --compare=$RAY --json=$RAW/start_M5_sector.json
run start_M5_k40_sector 0 $PY fixed_point_M_b.py --M=5 $START --sector=0.2 --k=40 --compare=$RAY --json=$RAW/start_M5_k40_sector.json
for m in radius coef sign scale rho0; do run start_M5_mut_$m 3 $PY fixed_point_M_b.py --M=5 $START --compare=$RAY --mutate=$m; done
# beyond the issue: win2's stored reproduction of the same set, and the M = 3 certificate's stored start set
run start_M5_vs_win2 0 $PY fixed_point_M_b.py --M=5 $START --compare=$RAYW
run start_M3_cert 0 $PY fixed_point_M_b.py --M=3 --start --rho0=262 --r0=0.1 --h=1.1e-9 --cauchy=1e-3 --compare=lemma6b1_runs_M3_cert/ray.json --json=$RAW/start_M3_cert.json
run start_M3_cert_mut_sign 3 $PY fixed_point_M_b.py --M=3 --start --rho0=262 --r0=0.1 --h=1.1e-9 --cauchy=1e-3 --compare=lemma6b1_runs_M3_cert/ray.json --mutate=sign
# --- #866 and #870: the point certificates' own start data (M = 3, and the three M = 5 boxes)
run cert_M3 0 $PY fixed_point_M_b_check.py cert --box=data/A_M_box_M3_1e-10.json
run cert_M3_mut_sign 3 $PY fixed_point_M_b_check.py cert --box=data/A_M_box_M3_1e-10.json --mutate=sign
run cert_M3_mut_radius 3 $PY fixed_point_M_b_check.py cert --box=data/A_M_box_M3_1e-10.json --mutate=radius
for h in 1e-10 1e-9 1e-11; do
  run cert_M5_$h 0 $PY fixed_point_M_b_check.py cert --box=data/A_M2_box_M5_$h.json --second
  run cert_M5_${h}_mut_sign 3 $PY fixed_point_M_b_check.py cert --box=data/A_M2_box_M5_$h.json --mutate=sign
  run cert_M5_${h}_mut_radius 3 $PY fixed_point_M_b_check.py cert --box=data/A_M2_box_M5_$h.json --mutate=radius
done
# --- #869: start_data2's second-derivative columns
for h in 1e-10 1e-9 1e-11; do run cert2_M5_$h 0 $PY fixed_point_M_b_check.py cert2 --box=data/A_M2_box_M5_$h.json; done
run cert2_M5_1e-10_mut_w0 3 $PY fixed_point_M_b_check.py cert2 --box=data/A_M2_box_M5_1e-10.json --mutate=w0
run cert2_M5_1e-10_mut_sign 3 $PY fixed_point_M_b_check.py cert2 --box=data/A_M2_box_M5_1e-10.json --mutate=sign
# --- #877: the fast-row kernel bound; #878: the command line's precision
run kernel 0 $PY fixed_point_M_b.py --kernel
run kernel_mut_offbyone 3 $PY fixed_point_M_b.py --kernel --mutate=offbyone
run cli 0 $PY fixed_point_M_b_check.py cli
run cli_mut_read53 3 $PY fixed_point_M_b_check.py cli --mutate=read53
echo "all done $(date -u '+%F %T') UTC" >> $RAW/exits.txt
