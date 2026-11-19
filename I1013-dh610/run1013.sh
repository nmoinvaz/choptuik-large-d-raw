#!/bin/bash
# #1013 on dh610: xfchecks' commands (#1013's body), N = 8 workers, nice 10. Stops at the first step whose exit is not as expected, and at the pilot's gate (gate1013.py).
. "$(dirname "$0")/common1013.sh"
EX=$RAW/exits_1013.txt
log() { echo "1013 $* $(stamp) UTC" >> $EX; }
cd $WT/solver/inner_stokes || exit 1
mkdir -p $RAW/m3 $RAW/logs
log "start, code $(git -C $WT rev-parse --short=8 HEAD), $($PY --version), numpy $($PY -c 'import numpy; print(numpy.__version__)'), load $(cut -d' ' -f1-3 /proc/loadavg)"
step() { local name=$1 want=$2; shift 2; local s=$(date +%s); "$@"; local rc=$?; log "$name exit $rc (expected $want) wall $(( $(date +%s) - s )) s"; [ $rc = $want ] || { log "stopped at $name"; exit 1; }; }
step selftest 0 bash -c "$PY argcount.py --selftest > $RAW/logs/selftest.log 2>&1"
step selftest_norecount 1 bash -c "$PY argcount.py --selftest --mutate=norecount > $RAW/logs/selftest_norecount.log 2>&1"
step pilot 0 bash -c "nice -n 10 timeout 2h $PY -u argcount.py --M=3 --A=2.5,3.0 --wf=0.8,1.2 --nA=2 --nwf=4 --procs=$N --out=$RAW/m3 --tag=pilot_known > $RAW/logs/m3_pilot.log 2>&1"
step gate_pilot 0 bash -c "python3 $RAW/gate1013.py $RAW/m3/count_pilot_known.json > $RAW/logs/gate_pilot.log 2>&1"
step gate_pilot_control 1 bash -c "python3 $RAW/gate1013.py $RAW/m3/count_pilot_known.json --mutate=shift > $RAW/logs/gate_pilot_control.log 2>&1"
step cand 0 bash -c "nice -n 10 timeout 12h $PY -u argcount.py --M=3 --A=1.9,3.9 --wf=0.2,1.1 --nA=8 --nwf=9 --procs=$N --out=$RAW/m3 --tag=M3_cand > $RAW/logs/m3_cand.log 2>&1"
step recount_r0.25 0 bash -c "nice -n 10 timeout 6h $PY -u argcount.py --M=3 --recount=$RAW/m3/leaves_M3_cand.jsonl --r1=0.25 --r1b=0.2 --seed=$RAW/m3/points_M3_r0.2.jsonl --procs=$N --out=$RAW/m3 --tag=M3_cand_r0.25 > $RAW/logs/m3_cand_r0.25.log 2>&1"
step recount_r0.17 0 bash -c "nice -n 10 timeout 6h $PY -u argcount.py --M=3 --recount=$RAW/m3/leaves_M3_cand_r0.25.jsonl --r1=0.17 --r1b=0.2 --seed=$RAW/m3/points_M3_r0.2.jsonl --procs=$N --out=$RAW/m3 --tag=M3_cand_r0.17 > $RAW/logs/m3_cand_r0.17.log 2>&1"
log "all steps done"
