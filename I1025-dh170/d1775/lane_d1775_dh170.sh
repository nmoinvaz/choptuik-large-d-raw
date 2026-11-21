#!/bin/bash
{
# v2 (21 Nov 07:58 UTC): stage 2 replaced after the first cross-check failed its own 1e-6 ln|det| criterion (see README); v1 is lane_d1775_dh170_v1.sh.
# #1025 D 17.75 on dh170 (coordinator's hc, 21 Nov ~07:45 UTC): xfkappa's scan (A) of lane_d18b.sh (the hybrid sign scan, d18_hybsign.py with the noise test and the float64 sign beside each point) at D 17.75 on winb's
# state sol_l1kc63W1025_D17.750000.npy (k_c 63), lambda 1.70 to 1.95 at 0.01 (26 points), 4 threads, nice 10, an 8 h cap by exact pid. Stages: pins; 1 the planted control ell_ddm.py selftest (PASS) and --mutate=slices (FAIL);
# 2 the cross-check: the hybrid at D 18, lam 1.8 on xfkappa's inputs must give +1 with ln|det| -1925.0182289868 (his d18_hybsign.log) to 1e-6, noise-robust, float64 +1; 3 the scan; 4 the reading (d1775_read.py).
# xfkappa's command of (A) (lane_d18b.sh):  timeout 21600 nice -n 10 $PY -u $Q/d18_hybsign.py $STUB $ST 18 $L $SCAN   with L = 1.70,1.71,...,1.90. Here: STUB = winb's record file (the D 17.75 row), ST = winb's D 17.75 state, D 17.75.
set -u
D=/home/nathan/Source/choptuik-large-d-raw-p4/I1025-dh170/d1775; I=/home/nathan/scratch1025d1775
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python; WT=/home/nathan/Source/choptuik-large-d-1025p4; W=$WT/solver/matter
ST=$I/sol_l1kc63W1025_D17.750000.npy; REC=$I/l1kc63W1025.jsonl; ST18=$I/sol_l1kc63W1025_D18.000000.npy; STUB18=$I/d18_stub_l1kc63W1025.jsonl
HS=$D/d18_hybsign.py; SCAN=$D/d1775_scan_dh170.jsonl; XJ=$D/d18_crosscheck3_dh170.jsonl; L=$D/exits_d1775.txt
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 VECLIB_MAXIMUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 P4_WT_MATTER=$W
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*" | tee -a $L; }
hb() { git hash-object --no-filters "$1"; }
bad=0
for pb in "$ST de9fc3e55aa46bafd4ef62536861f94aed9e3035" "$REC c33039dfa38b495486fb3ef7da77077d43db775a" "$ST18 45e72c6a5c22ee3f0196f7b08f07fecfe3a07b21" "$STUB18 2cfdb8334ed6ba7013396190d8a4833b2b854c4b" "$HS e089207a61fbd98614716abd309571cbc4888db2" "$I/ell_d18_hybrid_1025.jsonl fbeaa7a1be52f6fe9c3c52bb2c243b28eb9b57ee"; do
  set -- $pb
  [ -f $1 ] && [ "$(hb $1)" = "$2" ] || { say "refuse: $1 missing or not blob $2"; bad=1; }
done
[ "$(git -C $WT rev-parse HEAD)" = 505d839940456a3d04321d75cf66cc3b5bc831c4 ] && [ -z "$(git -C $WT status --short)" ] || { say "refuse: worktree $WT is not clean at 505d8399"; bad=1; }
for f in $SCAN $XJ; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done
$PY -c "import numpy, scipy, mpmath, multidouble; multidouble.dd_logdet" || { say "refuse: $PY lacks numpy/scipy/mpmath/multidouble.dd_logdet"; bad=1; }
[ $bad = 0 ] || exit 2
say "pins checked: state de9fc3e5 (D 17.75), record c33039df, D 18 state 45e72c6a, D 18 stub 2cfdb833, d18_hybsign e089207a, worktree 505d8399 clean; $PY; 4 threads"
cd $W
say "1. planted control: ell_ddm.py selftest (must PASS), then --mutate=slices (must FAIL), 1800 s each"
timeout 1800 nice -n 10 $PY -u ell_ddm.py selftest < /dev/null > $D/ell_ddm_selftest.log 2>&1; r1=$?
timeout 1800 nice -n 10 $PY -u ell_ddm.py selftest --mutate=slices < /dev/null >> $D/ell_ddm_selftest.log 2>&1; r2=$?
grep -E '^selftest:' $D/ell_ddm_selftest.log | tee -a $L
[ $r1 = 0 ] && [ $r2 = 1 ] || { say "STOP: the planted control did not behave (selftest exit $r1, --mutate=slices exit $r2)"; exit; }
say "2. cross-check (v2, replaces the failed 1e-6 ln criterion of v1): the hybrid at D 18 at xfkappa's three grid points 1.752930001950494, 1.788704083622953, 1.824478165295412 must give his signs -1, +1, -1 (ell_d18_hybrid_1025.jsonl, blob fbeaa7a1), each noise-robust, with ln|det| within 1e-2 of his; 3600 s per point"
LX=1.752930001950494,1.788704083622953,1.824478165295412
timeout 10800 nice -n 10 $PY -u $HS $STUB18 $ST18 18 $LX $XJ < /dev/null 2>&1 | grep --line-buffered -vE 'Warning|^  [a-z]+ = ' > $D/d18_crosscheck3_dh170.log
r=${PIPESTATUS[0]}; cat $D/d18_crosscheck3_dh170.log | tee -a $L; say "cross-check exit $r"
ok=$($PY - $XJ $I/ell_d18_hybrid_1025.jsonl <<'PYE'
import json, sys
try:
    mine = {r["lam"]: r for r in (json.loads(l) for l in open(sys.argv[1]))}
    ref = json.load(open(sys.argv[2]))["evals"] if False else json.loads(open(sys.argv[2]).readline())["evals"]
    good, parts = True, []
    for k in ("1.752930001950494", "1.788704083622953", "1.824478165295412"):
        m, x = mine[float(k)], ref[k]
        g = m["sign"] == x["sign"] and m["noise_robust"] and abs(m["ln"] - x["ln"]) <= 1e-2
        good &= g
        parts.append(f"{float(k):.6f}: sign {m['sign']:+.0f} (xfkappa {x['sign']:+.0f}) robust {m['noise_robust']} ln {m['ln']:.7f} (xfkappa {x['ln']:.7f}, diff {m['ln'] - x['ln']:+.2e}) float64 {m['f64_sign']:+.0f}")
    print(("PASS " if good else "FAIL ") + " | ".join(parts))
except Exception as e:
    print("FAIL no record:", e)
PYE
)
say "cross-check: $ok"
case "$ok" in PASS*) ;; *) say "STOP: the cross-check failed"; exit;; esac
LAMS=$($PY -c 'print(",".join(f"{1.70 + 0.01 * i:.2f}" for i in range(26)))')
say "3. the scan (A) at D 17.75: lam $LAMS; 8 h cap (28800 s) by exact pid"
s0=$(date +%s)
nice -n 10 /usr/bin/time -v $PY -u $HS $REC $ST 17.75 $LAMS $SCAN < /dev/null > $D/d1775_scan.raw 2>&1 &
tp=$!; echo $tp > $D/time_pid_scan.txt; say "scan started under /usr/bin/time pid $tp"
while kill -0 $tp 2>/dev/null; do
  if [ $(( $(date +%s) - s0 )) -gt 28800 ]; then
    py=$(ps -o pid= --ppid $tp | head -1 | tr -d ' '); say "8 h cap reached: TERM to python pid $py and time pid $tp"; kill -TERM $py $tp 2>/dev/null; break
  fi
  sleep 10
done
wait $tp; r=$?
grep -vE 'Warning|^  [a-z]+ = |slogdet' $D/d1775_scan.raw > $D/d1775_scan.log
say "scan exit $r, $(( $(date +%s) - s0 )) s wall"
$PY -I $D/d1775_read.py $SCAN > $D/d1775_read.txt 2>&1; say "reading: $(grep -E '^READING' $D/d1775_read.txt)"
say "lane d1775 done"
exit
}
