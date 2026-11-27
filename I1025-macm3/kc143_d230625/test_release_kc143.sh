#!/bin/bash
# sandbox tests of release_hold_kc143.sh (fake exits file, fake HOLD files, fake hc, decoy python processes): it releases only on the secant line with no scan process and enough memory,
# reports the chain's scan, and re-places the hold at the secant exit. Each case states what must happen; a case that does not behave exits 1 at the end.
PY=$HOME/Source/venv-macm3-1058b/bin/python
W=${1:-/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/953e9688-2a12-485d-a7d9-b760c6e8569c/scratchpad/reltest143}
S=${S:-$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc143_d230625/release_hold_kc143.sh}
rm -rf "$W.old" 2>/dev/null; [ -d "$W" ] && mv "$W" "$W.old.$(date +%s)"; mkdir -p "$W"; cd "$W"
printf '#!/bin/bash\necho "HC: $*" >> "$FAKELOG"\n' > fakehc.sh; chmod +x fakehc.sh
export SCANPAT="sandbox_scan[.]py" CHAINPAT="sandbox_scan[.]py" FAKELOG=$W/fake.log HC=$W/fakehc.sh NAME=kc143_sandbox LANEPAT=no_such_lane_pattern_$$ POLL=1 SETTLE=1 AFTER=1 REPWAIT=20 WAITH=1 CLOG=$W/chain.log LG=$W/exits.txt HOLD=$W/HOLD_kc143.txt REHOLD=$W/HOLD_kc143b.txt
echo "2026-11-27 00:00:00 UTC next: D 99 (sandbox)" > chain.log
bad=0
decoy() { "$PY" -c "import time; time.sleep($2)" sandbox_scan.py "$1" > /dev/null 2>&1 & echo $!; }
reset() { rm -f HOLD_kc143* fake.log exits.txt; echo held > HOLD_kc143.txt; : > fake.log; }
# case 1: the lane is gone and no secant line: must NOT release
reset; echo "== x kc143_sandbox: start" > exits.txt
bash $S > run1.out 2>&1
[ -f HOLD_kc143.txt ] && grep -q 'NOT released' fake.log && echo "case 1 ok (lane gone: held, hc says NOT released)" || { echo "case 1 FAILED"; bad=1; }
# case 2: the secant line, a scan process still runs: must NOT release
reset; echo "== x kc143_sandbox: secant starts: d18_secant.py run" > exits.txt; P=$(decoy a 25)
bash $S > run2.out 2>&1; kill $P 2>/dev/null
[ -f HOLD_kc143.txt ] && grep -q '1 scan processes still run' fake.log && echo "case 2 ok (a scan process runs: held)" || { echo "case 2 FAILED"; bad=1; }
# case 3: the secant line, no scan process, memory wanted 9999 GiB: must NOT release
reset; echo "== x kc143_sandbox: secant starts: d18_secant.py run" > exits.txt
MINAVAIL=9999 bash $S > run3.out 2>&1
[ -f HOLD_kc143.txt ] && grep -q 'NOT released' fake.log && echo "case 3 ok (memory short: held)" || { echo "case 3 FAILED"; bad=1; }
# case 4: the secant line, no scan process, memory enough: release; then the chain's scan (2 decoys) is reported; then the secant exit places the hold again
reset; echo "== x kc143_sandbox: secant starts: d18_secant.py run" > exits.txt
( bash $S > run4.out 2>&1 ) &
B=$!
for i in 1 2 3 4 5 6 7 8; do sleep 1; ls HOLD_kc143.txt.released.* > /dev/null 2>&1 && break; done
P1=$(decoy b 30); P2=$(decoy c 30)
for i in $(seq 1 20); do sleep 1; grep -q "chain's scan has started" fake.log && break; done
kill $P1 $P2 2>/dev/null
echo "== x kc143_sandbox: secant exit 0" >> exits.txt
wait $B
[ ! -f HOLD_kc143.txt ] && ls HOLD_kc143.txt.released.* > /dev/null 2>&1 && grep -q 'RELEASED' fake.log && grep -q '2 scan processes (d18_hybsign)' fake.log && [ -f HOLD_kc143b.txt ] && grep -q 'held again' fake.log && echo "case 4 ok (released, 2 chain processes reported, re-held at the secant exit)" || { echo "case 4 FAILED"; bad=1; }
echo "--- fake hc log of case 4"; cut -c1-260 fake.log
exit $bad
