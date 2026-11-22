#!/bin/bash
# #1067 (dh610), the coordinator's (B) of 22 Nov: call 4 from the call-3 checkpoint (lowD_dd.py --resume --it_max 1). If call 4's Delta correction is below 1e-25 (the issue's rule, kept) the state after call 4 is accepted and the fine plan and the series
# run automatically (run1067_s23.py); if not, stop and report the correction sequence (calls 2, 3, 4). The command is diffed against run1014b.py's B1 before the launch (cmddiff1067.py): only the expected options may differ.
cd ~/Source/choptuik-large-d-raw/I1067-dh610 || exit 9
PY=/home/nathan/Source/venv-i1058/bin/python
export RESUME_CALLS=3 MAX_CALLS_TOTAL=4
H=$(git hash-object ~/Source/choptuik-large-d-1067/hp/data/lowD_states/lowD1067_D3.0475_M512_ckpt.npz); case "$H" in 9be82013*) ;; *) echo "1067 call 4: the checkpoint's blob is not 9be82013 ($H): stop $(date -u '+%F %T') UTC" >> exits_1067.txt; exit 1;; esac
$PY -I run1067_s1.py --print-cmd > cmd_stage1_call4.txt && $PY -I cmddiff1067.py cmd_stage1_call4.txt > cmddiff_stage1_call4.txt 2>&1; R=$?
echo "1067 call 4 command diff against run1014b.py's B1: $(tail -1 cmddiff_stage1_call4.txt) (exit $R) $(date -u '+%F %T') UTC" >> exits_1067.txt
[ $R = 0 ] || { echo "1067 call 4: the command differs unexpectedly: not launched $(date -u '+%F %T') UTC" >> exits_1067.txt; exit 1; }
$PY -u run1067_s1.py >> run1067_s1.out 2>&1 || { echo "1067 stage 1 (call 4) did not choose a state: stages 2 and 3 not run $(date -u '+%F %T') UTC" >> exits_1067.txt; exit 1; }
[ -f run1067_s23.py ] || { echo "1067 run1067_s23.py is missing: stages 2 and 3 not run $(date -u '+%F %T') UTC" >> exits_1067.txt; exit 1; }
exec $PY -u run1067_s23.py >> run1067_s23.out 2>&1
