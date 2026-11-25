#!/bin/bash
# #1025 macm3 kc87_leg2: starts part c2, the continuation of part c past the psi-constraint bar (t5, hc 25 Nov ~05:1x UTC: "when part c stops at the 1e-2 bar, restart it from its last two states with --cmax 2e-2 to D 24.0, as part c2").
# Conditions: c/LEG_DONE.txt with exit 1, no c/leg_STOP.txt (a guard or crossing stop is not this), no Traceback in c/leap.log, and the leap log's last "stop at D" line is the constraint bar (psi-constraint above its bar, |F| below its bar).
# Seeds: the last two accepted rows of part c's record (data/l1kc87Lmacm3c.jsonl of the worktree), their states; step H2 = 0.0625 (part c's step). If part c ended another way: "part c2 not needed" (exit 0, ended by the crossing stop, the guard, or D 24.0)
# or "NOT started" (an error), hc to t5 either way. Log: start_cont.log (the chain reads "NOT started" and "not needed" in it).
L2=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg2
WTM=$HOME/Source/choptuik-large-d-1025m3/solver/matter
HC=$(command -v hc)
LOG=$L2/start_cont.log
say() { echo "$(date -u '+%F %T') UTC $*" >> $LOG; }
tell() { say "hc: $*"; [ -n "$HC" ] && "$HC" send nathans-macbook-air-m5-3/t5 "$*" >> $LOG 2>&1; }
say "waiting for part c (c/LEG_DONE.txt)"
while [ ! -e $L2/c/LEG_DONE.txt ]; do
  grep -q 'NOT started' $L2/start_c2.log 2>/dev/null && { tell "macm3 #1025 kc87_leg2: part c2 NOT started: part c was not started"; exit 1; }
  grep -q 'not needed' $L2/start_c2.log 2>/dev/null && { tell "macm3 #1025 kc87_leg2: part c2 not needed: part c was not started (not needed)"; exit 0; }
  sleep 30
done
sleep 5
why=""; notneeded=""
grep -q 'LEG DONE exit 1' $L2/c/LEG_DONE.txt || notneeded="c/LEG_DONE says: $(cat $L2/c/LEG_DONE.txt)"
[ ! -e $L2/c/leg_STOP.txt ] || notneeded="$notneeded a STOP file in c: $(head -1 $L2/c/leg_STOP.txt | cut -c1-200);"
[ "$(grep -c Traceback $L2/c/leap.log)" = 0 ] || why="$why a Traceback in c/leap.log;"
stopline=$(grep '^stop at D' $L2/c/leap.log | tail -1)
python3 - "$stopline" <<'PY' || notneeded="$notneeded the leap log's last stop line is not the constraint bar ($stopline);"
import re, sys
m = re.search(r"stop at D ([\d.]+): \|F\| ([\d.e+-]+) \(bar ([\d.e+-]+)\), psi-constraint ([\d.e+-]+) \(bar ([\d.e+-]+)\)", sys.argv[1])
sys.exit(0 if m and float(m.group(4)) > float(m.group(5)) and float(m.group(2)) < float(m.group(3)) else 1)
PY
if [ -n "$why" ]; then tell "macm3 #1025 kc87_leg2: part c2 NOT started:$why"; exit 1; fi
if [ -n "$notneeded" ]; then tell "macm3 #1025 kc87_leg2: part c2 not needed (part c did not stop at the constraint bar): $notneeded"; exit 0; fi
read DA DB SA SB < <(python3 - $WTM/data/l1kc87Lmacm3c.jsonl <<'PY'
import json, sys
rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
a, b = rows[-2]["D"], rows[-1]["D"]
print(repr(a), repr(b), "sol_l1kc87Lmacm3c_D%.6f.npy" % a, "sol_l1kc87Lmacm3c_D%.6f.npy" % b)
PY
)
say "part c stopped at the constraint bar ($stopline); part c2 from D $DA and D $DB ($SA, $SB), h 0.0625, --cmax 2e-2, to D 24.0"
SAC2=$SA SBC2=$SB DAC2=$DA DBC2=$DB H2=0.0625 bash $L2/run_leg2cont.sh run >> $L2/start_cont.out 2>&1 &
drv=$!
for i in $(seq 1 90); do [ -e $L2/c2/leap.started ] && break; kill -0 $drv 2>/dev/null || break; sleep 10; done
if [ -e $L2/c2/leap.started ]; then tell "macm3 #1025 kc87_leg2: part c2 STARTED $(date -u '+%F %T') UTC from D $DA and D $DB with --cmax 2e-2, h 0.0625, to D 24.0 (part c stopped: $stopline)"
else tell "macm3 #1025 kc87_leg2: part c2 did NOT start its leap (see c2/exits_leg2c2.txt)"; fi
wait $drv; rc=$?
say "run_leg2cont.sh run returned $rc"
