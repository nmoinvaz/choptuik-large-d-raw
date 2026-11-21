#!/bin/bash
{
# #1025 D 18 (B), then (A) on reading (1) (d18_dd_criteria.log). usage: lane_d18b.sh PID1 PID2 [dry]   (waits for both to exit)
set -u
P1=$1; P2=$2; MODE=${3:-}
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac; Q=$R/d18; PY=/Users/nathan/venv-1025dd/bin/python
WT=/Users/nathan/Source/choptuik-1025; W=$WT/solver/matter
ST=$Q/sol_l1kc63W1025_D18.000000.npy; STUB=$Q/d18_stub_l1kc63W1025.jsonl
HS=$Q/d18_hybsign_1025.jsonl; DDJ=$Q/ell_ddm_D18_1025.jsonl; SCAN=$Q/d18_scan_1025.jsonl
LAMS=1.788704083622953,1.8
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 VECLIB_MAXIMUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 P4_WT_MATTER=$W
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; }
hb() { git hash-object --no-filters "$1"; }
bad=0
for pb in "$ST 45e72c6a5c22ee3f0196f7b08f07fecfe3a07b21" "$STUB 2cfdb8334ed6ba7013396190d8a4833b2b854c4b" \
          "$Q/d18_hybsign.py e089207a61fbd98614716abd309571cbc4888db2" "$Q/d18_dd_read.py ddf56fc92a3a18a76911a280b52b8f76ca6415d2"; do
  set -- $pb
  [ -f $1 ] && [ "$(hb $1)" = "$2" ] || { say "refuse: $1 missing or not blob $2"; bad=1; }
done
git -C $WT diff --quiet 505d839940456a3d04321d75cf66cc3b5bc831c4 -- solver/matter/dss_ell.py solver/matter/ell_ddm.py solver/matter/ell_dd.py \
  solver/matter/ddnp.py || { say "refuse: the worktree's solver code differs from 505d8399"; bad=1; }
for f in $HS $DDJ $SCAN; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
say "pins checked: state 45e72c6a, stub 2cfdb833, d18_hybsign e089207a, d18_dd_read ddf56fc9, solver code = 505d8399; waiting for pids $P1 $P2"
[ "$MODE" = dry ] && exit 0
while kill -0 $P1 2> /dev/null || kill -0 $P2 2> /dev/null; do sleep 30; done
say "pids $P1 $P2 have exited"
grep -E '^D 18' $Q/d18_root.log | tail -n 1
cd $W
say "1. planted control: ell_ddm.py selftest (must PASS), then --mutate=slices (must FAIL)"
timeout 1800 nice -n 10 $PY -u ell_ddm.py selftest < /dev/null > $Q/d18_ddm_selftest.log 2>&1; r1=$?
timeout 1800 nice -n 10 $PY -u ell_ddm.py selftest --mutate=slices < /dev/null >> $Q/d18_ddm_selftest.log 2>&1; r2=$?
grep -E '^selftest:' $Q/d18_ddm_selftest.log
[ $r1 = 0 ] && [ $r2 = 1 ] || { say "STOP: the planted control did not behave (selftest exit $r1, --mutate=slices exit $r2)"; exit; }
say "2. the hybrid at lam 1.8 (timeout 3600 s)"
timeout 3600 nice -n 10 $PY -u $Q/d18_hybsign.py $STUB $ST 18 1.8 $HS < /dev/null 2>&1 | grep --line-buffered -vE 'Warning|^  [a-z]+ = ' > $Q/d18_hybsign.log
r=${PIPESTATUS[0]}; cat $Q/d18_hybsign.log; say "hybrid at 1.8 exit $r"
[ $r = 0 ] || { say "STOP: the hybrid at 1.8 did not finish"; exit; }
say "3. the full dd M at $LAMS (timeout 10800 s)"
timeout 10800 nice -n 10 $PY -u ell_ddm.py det $ST 18 63 $LAMS --noise 1e-24,1e-20,1e-16 --out $DDJ < /dev/null 2>&1 \
  | grep --line-buffered -vE 'Warning|^  [a-z]+ = ' > $Q/d18_ddm.log
r=${PIPESTATUS[0]}; cat $Q/d18_ddm.log; say "dd det exit $r"
[ $r = 0 ] || { say "STOP: the dd det did not finish"; exit; }
$PY $Q/d18_dd_read.py $Q/ell_d18_hybrid_1025.jsonl $HS $DDJ $LAMS > $Q/d18_dd_read.log 2>&1; code=$?
cat $Q/d18_dd_read.log; say "reading code $code"
say "4. information: the dd M with --mutate=hionly at $LAMS (timeout 7200 s)"
timeout 7200 nice -n 10 $PY -u ell_ddm.py det $ST 18 63 $LAMS --out $DDJ --mutate=hionly < /dev/null 2>&1 \
  | grep --line-buffered -vE 'Warning|^  [a-z]+ = ' > $Q/d18_ddm_hionly.log
r=${PIPESTATUS[0]}; cat $Q/d18_ddm_hionly.log; say "hionly exit $r"
[ $code = 0 ] || { say "no (A): the reading code is $code (d18_dd_criteria.log)"; say "lane d18b done"; exit; }
L=$($PY -c 'print(",".join(f"{1.70 + 0.01 * i:.2f}" for i in range(21)))')
say "(A): the hybrid scan at $L (timeout 21600 s)"
timeout 21600 nice -n 10 $PY -u $Q/d18_hybsign.py $STUB $ST 18 $L $SCAN < /dev/null 2>&1 | grep --line-buffered -vE 'Warning|^  [a-z]+ = ' > $Q/d18_scan.log
r=${PIPESTATUS[0]}; say "scan exit $r"
$PY -c 'import sys, json
L = sorted((json.loads(l) for l in open(sys.argv[1])), key=lambda r: r["lam"])
sg = lambda r: "%.2f%s" % (r["lam"], "+" if r["sign"] > 0 else "-")
print("signs:", " ".join(sg(r) for r in L))
ch = [(a["lam"], b["lam"]) for a, b in zip(L, L[1:]) if a["sign"] != b["sign"]]
print("sign changes:", len(ch), "in", [(round(a, 2), round(b, 2)) for a, b in ch])
print("points not noise-robust:", [round(r["lam"], 2) for r in L if not r["noise_robust"]] or "none")' $SCAN | tee -a $Q/d18_scan.log
say "lane d18b done"
exit
}
