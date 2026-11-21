#!/bin/bash
{
# #1025 step (2) (d18_criteria.log, the coordinator's rulings of 2026-11-21): after lane_d18.sh, and only if D 18 passed its rules and
# signtest, the k_c 63 leap D 18 -> 18.5 (winb's flags, h 0.0625, seeds winb's D 17.9375 and D 18 states), then the D 18.5 guess
# (d185_guess.py, written into the README and the criteria log before the root), the hybrid root at D 18.5, its rules, the signtest.
# usage: lane_d185.sh WAIT_PID [dry]
set -u
WAIT=$1; MODE=${2:-}
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac; Q=$R/d18; PY=/Users/nathan/venv-1025dd/bin/python
WT=/Users/nathan/Source/choptuik-1025; W=$WT/solver/matter; TAG=l1kc63Wm1025
SA=$Q/sol_l1kc63W1025_D17.937500.npy; SB=$Q/sol_l1kc63W1025_D18.000000.npy
LJ=$W/data/$TAG.jsonl; ST=$Q/sol_${TAG}_D18.5000.npy; STUB=$Q/d185_stub_$TAG.jsonl; JS=$Q/ell_d185_hybrid_1025.jsonl
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 VECLIB_MAXIMUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4
export P4_WT_MATTER=$W P4_OUT=$JS
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; }
hb() { git hash-object --no-filters "$1"; }
bad=0
for pb in "$R/p4_hybrid.py a402559b5d37661b49da50f07f877af21fd29b3a" "$R/signtest.py 179ea09681b0a75f7cefdff98984b48051b3f085" \
          "$W/ell_leap.py 1eb873e49348f400d9d0dfc1cd95be5761473d0c" "$SA a8f78f18fed4ea395aa025dc12ec3009ceb7c92b" \
          "$SB 45e72c6a5c22ee3f0196f7b08f07fecfe3a07b21" "$Q/d18_check.py 08969ea28fbd6cb0d83e17c2d4ded1901ce6b209" \
          "$Q/d185_guess.py de86edaaae97b395f00b869f49520453270318cd"; do
  set -- $pb
  [ -f $1 ] && [ "$(hb $1)" = "$2" ] || { say "refuse: $1 missing or not blob $2"; bad=1; }
done
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_leap.py \
  || { say "refuse: the worktree's solver code differs from 505d8399"; bad=1; }
for f in $LJ $ST $STUB $JS $Q/leap_kc63_d185.log; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
say "pins checked: p4_hybrid a402559b, signtest 179ea096, ell_leap 1eb873e4, seeds a8f78f18 (D 17.9375) and 45e72c6a (D 18), d18_check 08969ea2, d185_guess de86edaa; waiting for pid $WAIT"
[ "$MODE" = dry ] && exit 0
while kill -0 $WAIT 2> /dev/null; do sleep 60; done
say "pid $WAIT has exited"
grep -q '^== .* lane d18 done' $Q/lane_d18.log && grep -q '^signtest control fires as written' $Q/lane_d18.log \
  && grep -q '^signtest: .*-> PASS$' $Q/lane_d18.log || { say "STOP: D 18 did not pass all its rules and its signtest (lane_d18.log); no leap"; exit; }
say "D 18 passed; leap: ell_leap.py $TAG 1 63 D 17.9375, 18 -> 18.5, h 0.0625 (timeout 43200 s)"
cd $W
timeout 43200 nice -n 10 $PY -u ell_leap.py $TAG 1 63 $SA 17.9375 $SB 18 18.5 0.0625 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold \
  < /dev/null 2>&1 | grep --line-buffered -vE 'Warning|^  ' > $Q/leap_kc63_d185.log
rc=${PIPESTATUS[0]}
say "leap exit $rc"
tail -n 2 $Q/leap_kc63_d185.log | cut -c1-200
cp $LJ $Q/ 2> /dev/null
[ $rc = 0 ] && grep -q '^reached D 18.5' $Q/leap_kc63_d185.log && [ -f $W/data/sol_${TAG}_D18.5000.npy ] \
  || { say "STOP: the leap did not reach D 18.5; no root"; exit; }
cp $W/data/sol_${TAG}_D18.5000.npy $ST
$PY $Q/d185_guess.py $R/out/ell_p4_hybrid_1025.jsonl $Q/ell_d18_hybrid_1025.jsonl 18.5 $LJ $STUB > $Q/d185_guess.log 2>&1 \
  || { cat $Q/d185_guess.log; say "STOP: d185_guess.py failed"; exit; }
cat $Q/d185_guess.log
g=$(awk '/^slope over/ {print $NF}' $Q/d185_guess.log); w2=$(awk '/window 0.02:/ {print $4, $5, $6}' $Q/d185_guess.log)
T=$(date -u '+%Y-%m-%d %H:%M:%S')
echo "== $T D 18.5 guess (d185_guess.py, d185_guess.log), written before the D 18.5 root: $g; first grid $w2 (p4_hybrid's ladder). Stub $(basename $STUB) blob $(hb $STUB); state $(basename $ST) blob $(hb $ST)." >> $Q/d18_criteria.log
echo "- D 18.5 guess, $T UTC, before the D 18.5 root: $g (the line through the D 17 and D 18 hybrid roots at k_c 63; \`d18/d185_guess.log\`); first grid $w2." >> $R/README.md
say "root: p4_hybrid.py on the stub, D 18.5 (timeout 21600 s)"
timeout 21600 nice -n 10 $PY -u $R/p4_hybrid.py $STUB $ST 18.5 < /dev/null 2>&1 | grep --line-buffered -vE 'Warning|sl.solve' > $Q/d185_root.log
rc=${PIPESTATUS[0]}
grep -E '^D ' $Q/d185_root.log
say "root exit $rc"
[ $rc = 0 ] && [ -s $JS ] || { say "STOP: the root run did not finish; no signtest"; exit; }
$PY $Q/d18_check.py $JS 18.5; ck=$?
say "d18_check exit $ck"
[ $ck = 0 ] || { say "STOP: the D 18.5 root fails its rules; no lambda at D 18.5"; exit; }
$PY -c 'import sys, json; r = json.loads(open(sys.argv[1]).readlines()[-1]); s = json.loads(open(sys.argv[2]).read())
s.update(lam=r["lam"], lam_is_guess=False, stub_note="the D 18.5 stub with lam = the hybrid root (ell_d185_hybrid_1025.jsonl), for signtest.py around=")
open(sys.argv[3], "w").write(json.dumps(s) + "\n"); print("signtest record: lam", repr(s["lam"]))' $JS $STUB $Q/d185_root_rec.jsonl
say "signtest planted"
timeout 600 nice -n 10 $PY -u $R/signtest.py planted > $Q/d185_signtest.log 2>&1
cat $Q/d185_signtest.log
say "signtest at lam -/+ 0.02 (timeout 3600 s)"
timeout 3600 nice -n 10 $PY -u $R/signtest.py $ST 18.5 63 around=$Q/d185_root_rec.jsonl:18.5:0.02 --u0=0.04 --Ks=30 --kappa=0.7 --rk=1 \
  < /dev/null 2>&1 | grep --line-buffered -vE 'Warning|sl.solve' >> $Q/d185_signtest.log
rc=${PIPESTATUS[0]}
say "signtest exit $rc"
tail -n 4 $Q/d185_signtest.log
$PY -c 'import sys, json
L = [json.loads(l) for l in open(sys.argv[1]) if l.startswith("{") and "signs" in l]
pl = [l for l in open(sys.argv[1]) if l.startswith("planted:")]
ctl = len(pl) == 3 and pl[0].strip().endswith("agree") and pl[1].strip().endswith("agree") and pl[2].strip().endswith("DISAGREE")
ok = len(L) == 2 and all(r["agree"] for r in L) and L[0]["signs"][0] != L[1]["signs"][0]
print("signtest control", "fires as written" if ctl else "DOES NOT behave as written (reading void)")
print("signtest:", [(round(r["lam"], 7), r["signs"][0], r["agree"]) for r in L], "->", "PASS" if ok and ctl else "FAIL")' $Q/d185_signtest.log
say "lane d185 done"
exit
}
