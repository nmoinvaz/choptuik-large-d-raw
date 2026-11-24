#!/bin/bash
# #1082 (t5's hc): after rate 1's quad-double row lands, stop the decisive test's chain (unit i1082a, which would go on to rate 2) and run rate 3 alone (5.1408197887863025) with the same code, state and options;
# the test ends with that row. Unit i1082gate. No hc from here.
{
OUT=/home/nathan/Source/choptuik-large-d-raw-wt613/I1082-dh370
RAWIN=/home/nathan/Source/choptuik-large-d-raw-push960
S96=$RAWIN/I1072-dh370/states3/tmap_tmap_tmap_lowDhm_x0.000157-0.975_D3.0444_M384_L0.4_M160_s1.9635_L0.4_M128_s1.9635_L0.4_M96_s1.9635.npz
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps_1082.txt; }
until [ -s $OUT/qd.jsonl ] && grep -q '"lam": 5.1408197887857,' $OUT/qd.jsonl; do sleep 20; done
sleep 5
systemctl --user stop i1082a
step "gate: rate 1's quad-double row landed ($(head -1 $OUT/qd.jsonl | python3 -c 'import json,sys; r=json.loads(sys.stdin.readline()); print("sign", r["sign"], "ln", r["ln"], "matrix", r["sec_matrix"], "s")')); unit i1082a stopped ($(systemctl --user is-active i1082a)); starting rate 3 alone (unit i1082c)"
[ "$(git -C /home/nathan/Source/choptuik-large-d-1082 rev-parse --short=8 HEAD)" = a9975061 ] && [ "$(git hash-object --no-filters $S96 | cut -c1-8)" = 6a0f83d2 ] || { step "STOP: the worktree or the state is not pinned"; exit 1; }
systemd-run --user --unit i1082c --collect systemd-inhibit --what=sleep:idle --who=i1082c --why="#1082 rate 3 alone" bash -c "cd /home/nathan/Source/choptuik-large-d-1082/hp && OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6 nice -n 10 /home/nathan/Source/choptuik-large-d-1082/.venv/bin/python -u mode_qd_decide.py $OUT $S96 --threads=4 --lams=5.1408197887863025 --skip_dd > $OUT/decide_rate3.log 2>&1; rc=\$?; echo \"\$(date -u '+%F %T') UTC rate 3 alone: mode_qd_decide.py exit \$rc (the verdict of one rate is not the test's; judge by hand)\" >> $OUT/steps_1082.txt; echo \"1082 TEST ENDED after rates 1 and 3 (t5's order) \$(date -u '+%F %T') UTC; exit \$rc\" > $OUT/1082_DONE.txt"
sleep 3
step "gate: unit i1082c $(systemctl --user is-active i1082c)"
exit 0
}
