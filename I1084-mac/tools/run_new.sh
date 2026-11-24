#!/bin/bash
# #1084 new code (worktree wip/value-mp-floor): the floor check and its controls, zero_mp's selftest, then the three
# #1076 points and the M = 5 centre through drive.py; one process at a time, nice 10, one BLAS thread
{
S=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/i1084
W=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3aa6f99477123b54/solver/inner_stokes
PY=/Users/nathan/venv-314/bin/python
export OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_OPERATION_COUNT=1
while pgrep -f "run_probes_old.sh" >/dev/null; do sleep 5; done
cd "$W" || exit 1
git -C "$W" log --oneline -1
for m in "" off tau-low tau-high keepj; do
  date -u "+check ${m:-plain} %F %T"
  if [ -z "$m" ]; then nice -n 10 timeout 900 "$PY" value_mp_floor_check.py > "$S/runs/check_plain.log" 2>&1
  else nice -n 10 timeout 900 "$PY" value_mp_floor_check.py --mutate=$m > "$S/runs/check_$m.log" 2>&1; fi
  echo "check ${m:-plain} exit $?"
done
nice -n 10 "$PY" zero_mp.py selftest > "$S/runs/zero_selftest.log" 2>&1; echo "zero_mp selftest exit $?"
nice -n 10 "$PY" zero_mp.py selftest --mutate=sign > "$S/runs/zero_selftest_sign.log" 2>&1; echo "zero_mp selftest --mutate=sign exit $?"
cd "$S" || exit 1
run() {  # name args...
  local name=$1; shift
  date -u "+start $name %F %T"
  nice -n 10 timeout 3600 "$PY" tools/drive.py "$W" "$@" > "runs/$name.out" 2> "runs/$name.err"
  echo "$name exit $?"
}
run new_p1 point 3.642554027092 0.345236176729 0.0039137451601883935 -0.4353814310277417 --iters=12
run new_p2 point 3.553347058422 0.413172823632 0.006041017694051223 -0.3799219466832089 --iters=12
run new_p3 point 3.5529706 0.41289086625 0.006040267478291 -0.380031415605351 --iters=12
VALUE_MP_PROGRESS=1 run new_m5 pointv 2.726475885672135 1.0156030949093042 --M=5 --v=0.1444194785,0.0110874259,0,0 --iters=8
date -u '+end %F %T'
exit 0
}
