#!/bin/bash
{
# #1025 D 18 (d18_criteria.log): the hybrid root of lambda_1 at k_c 63 on winb's leap state, its rules, then the float64 signtest at
# lam -/+ 0.02. usage: lane_d18.sh [dry]   (dry: the pin checks only)
set -u
MODE=${1:-}
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac; Q=$R/d18; PY=/Users/nathan/venv-1025dd/bin/python
WT=/Users/nathan/Source/choptuik-1025; W=$WT/solver/matter
ST=$Q/sol_l1kc63W1025_D18.000000.npy; STUB=$Q/d18_stub_l1kc63W1025.jsonl; JS=$Q/ell_d18_hybrid_1025.jsonl
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 VECLIB_MAXIMUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4
export P4_WT_MATTER=$W P4_OUT=$JS
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; }
hb() { git hash-object --no-filters "$1"; }
bad=0
for pb in "$R/p4_hybrid.py a402559b5d37661b49da50f07f877af21fd29b3a" "$R/signtest.py 179ea09681b0a75f7cefdff98984b48051b3f085" \
          "$ST 45e72c6a5c22ee3f0196f7b08f07fecfe3a07b21" "$STUB 2cfdb8334ed6ba7013396190d8a4833b2b854c4b" \
          "$Q/d18_check.py d41b6e2fef14d531c37369de0f2d9ad071514943"; do
  set -- $pb
  [ -f $1 ] && [ "$(hb $1)" = "$2" ] || { say "refuse: $1 missing or not blob $2"; bad=1; }
done
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ddnp.py \
  || { say "refuse: the worktree's solver code differs from 505d8399"; bad=1; }
[ -e $JS ] && { say "refuse: $JS exists"; bad=1; }
[ $bad = 0 ] || exit 2
say "pins checked: p4_hybrid a402559b, signtest 179ea096, state 45e72c6a, stub 2cfdb833, d18_check d41b6e2f, solver code = 505d8399"
[ "$MODE" = dry ] && exit 0
say "root: p4_hybrid.py on the stub, D 18 (timeout 21600 s)"
timeout 21600 nice -n 10 $PY -u $R/p4_hybrid.py $STUB $ST 18 < /dev/null 2>&1 | grep --line-buffered -vE 'Warning|sl.solve' > $Q/d18_root.log
rc=${PIPESTATUS[0]}
grep -E '^D ' $Q/d18_root.log
say "root exit $rc"
[ $rc = 0 ] && [ -s $JS ] || { say "STOP: the root run did not finish; no signtest, no leap"; exit; }
$PY $Q/d18_check.py $JS 18; ck=$?
say "d18_check exit $ck"
[ $ck = 0 ] || { say "STOP: the root fails its rules; no lambda at D 18, no leap"; exit; }
$PY -c 'import sys, json; r = json.loads(open(sys.argv[1]).readlines()[-1]); s = json.loads(open(sys.argv[2]).read())
s.update(lam=r["lam"], lam_is_guess=False, stub_note="the D 18 stub with lam = the hybrid root (ell_d18_hybrid_1025.jsonl), for signtest.py around=")
open(sys.argv[3], "w").write(json.dumps(s) + "\n"); print("signtest record: lam", repr(s["lam"]))' $JS $STUB $Q/d18_root_rec.jsonl
cd $W
say "signtest planted"
timeout 600 nice -n 10 $PY -u $R/signtest.py planted > $Q/d18_signtest.log 2>&1
cat $Q/d18_signtest.log
say "signtest at lam -/+ 0.02 (timeout 3600 s)"
timeout 3600 nice -n 10 $PY -u $R/signtest.py $ST 18 63 around=$Q/d18_root_rec.jsonl:18:0.02 --u0=0.04 --Ks=30 --kappa=0.7 --rk=1 \
  < /dev/null 2>&1 | grep --line-buffered -vE 'Warning|sl.solve' >> $Q/d18_signtest.log
rc=${PIPESTATUS[0]}
say "signtest exit $rc"
tail -n 4 $Q/d18_signtest.log
$PY -c 'import sys, json
L = [json.loads(l) for l in open(sys.argv[1]) if l.startswith("{") and "signs" in l]
pl = [l for l in open(sys.argv[1]) if l.startswith("planted:")]
ctl = len(pl) == 3 and pl[0].strip().endswith("agree") and pl[1].strip().endswith("agree") and pl[2].strip().endswith("DISAGREE")
ok = len(L) == 2 and all(r["agree"] for r in L) and L[0]["signs"][0] != L[1]["signs"][0]
print("signtest control", "fires as written" if ctl else "DOES NOT behave as written (reading void)")
print("signtest:", [(round(r["lam"], 7), r["signs"][0], r["agree"]) for r in L], "->", "PASS" if ok and ctl else "FAIL")' $Q/d18_signtest.log
say "lane d18 done"
exit
}
