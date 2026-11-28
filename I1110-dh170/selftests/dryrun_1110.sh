#!/bin/bash
# Dry run of run_1110.sh with a fake i1101_weakdir.py (the real units of systemd-run are used, with the prefix i1110t), DRY=1 (no pins of the worktree), a fake R3 folder, MAXP=2 and
# fake scanner processes (processes whose command line matches the admission pattern). usage: dryrun_1110.sh SCENARIO
#   ok       all bars pass; R3's fake steps.txt gets its "[r3] secant starts" line after 15 s (the root must wait for it) and two other scanner processes run 2 to 62 s with MAXP=2 (the root must wait
#            for a slot); the root is formed at delta 0
#   cap      as ok without the waits; the root fake runs long and the root's timeout CAP=20 s ends it (exit 124): partial bracket read
#   widen    (0.10, 0.13) refused, the widened (0.05, 0.16) forms a root at 0.08
#   bar1     the kappa 0.35 chord state has 8350 steps: STOP        bar1f  its |F| is 7e-10: STOP       bar2  the control gives 8351 steps: STOP        jac3  jac exits 3: STOP
SC=${1:?scenario}
HERE=$(cd $(dirname $0)/.. && pwd)
T=$(mktemp -d /tmp/claude-1000/dryr1110.XXXXXX); mkdir -p $T/out/in $T/out/selftests $T/wtm $T/r3
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python
cp $HERE/run_1110.sh $HERE/results_1110.py $T/out/; cp $HERE/../I1101-dh170/scan_admit.sh $T/r3/
cp $HERE/in/l1kc127k070w2.jsonl $T/out/in/; for f in sol_l1kc127k070w2_D23.0000.npy R2_sol_l1kc127k035w2_D23.0000.npy; do cp $HERE/in/$f $T/out/in/; done
cat > $T/wtm/i1101_weakdir.py <<'PYEOF'
import json, os, sys, time
a = [x for x in sys.argv[1:] if not x.startswith("--")]
cmd = a[0]; env = os.environ
if cmd == "jac":
    if env.get("FAKE_JAC_RC") == "3":
        print("pin differs"); sys.exit(3)
    open(a[4], "wb").write(b"x"); print(json.dumps(dict(out=a[4], F=1e-10, J_shape=[2, 2], seconds=1, steps=4179)))
elif cmd == "svd":
    open(a[2], "wb").write(b"x"); print("svd (2, 2): 0.1 s, s_max 1.0e+00, s_min 1.0e-12")
elif cmd == "chord":
    mp, out = a[5], a[6]; k = mp.split("=")[1]
    steps = int(env.get("FAKE_STEPS35", 8351)) if k == "0.35" else int(env.get("FAKE_STEPS34", 8100))
    F = float(env.get("FAKE_F35", 3e-10)) if k == "0.35" else 3e-10
    open(out, "wb").write(b"x"); json.dump(dict(D=23.0, kc=127, kappa=0.7, map=mp, steps=steps, F=F, Delta=1.0), open(out.replace(".npy", ".map.json"), "w"))
    print(f"{mp}: steps {steps} (record 4179); chord |F| 1e-9 {F:.3e}; kept {F:.4e}; Delta 1.0 (from 1.0); saved {out}")
elif cmd == "coords":
    print("weak vectors (from the smallest): [8349, 8348]"); print("chord035: |dz| 1.0e-09, dDelta +1.0e-12; fraction null 1.0e-03 weak 0.100000 strong 1.0e-02; weak coords +1.0e-10 -2.0e-10")
elif cmd == "root":
    st, lo, hi, outf = a[1], float(a[2]), float(a[3]), a[4]
    wide = lo < 0.1; r = float(env.get("FAKE_R_WIDE" if wide else "FAKE_R", 0.1178))
    def ev(lam, role):
        d = r - lam; rec = dict(kind="eval", lam=lam, sign=1.0 if d > 0 else -1.0, robust=True, ln=-4000.0 + 100 * abs(d), dln=1e-5, role=role, it=0, sec=5)
        open(outf, "a").write(json.dumps(rec) + "\n"); time.sleep(float(env.get("FAKE_EV", 5))); return rec
    ra, rb = ev(lo, "lo"), ev(hi, "hi")
    if ra["sign"] == rb["sign"]:
        open(outf, "a").write(json.dumps(dict(kind="root", status="refused", why="the ends have the same hybrid sign", bracket=[lo, hi], width=hi - lo, signs=[ra["sign"], rb["sign"]], robust=[True, True], lam_lin=None, lam_brent=None, n_eval=2, tol=1e-6, sec=10)) + "\n"); sys.exit(2)
    n = int(env.get("FAKE_N", 6))
    for i in range(n):
        ev(r + (0.01 if i % 2 == 0 else -0.01) / (i + 1), "interior")
    open(outf, "a").write(json.dumps(dict(kind="root", status="tol", why="", bracket=[r - 5e-7, r + 5e-7], width=1e-6, signs=[1.0, -1.0], robust=[True, True], lam_lin=r, lam_brent=r, n_eval=n + 2, tol=1e-6, sec=50)) + "\n")
PYEOF
cd $T/out
cat > $T/fakescan.sh <<EOS
#!/bin/bash
# fakescan.sh SLEEP NAME: a process whose command line matches the scanner pattern
exec -a "$PY -u /x/d18_secant.py scan /dryin/\$2.jsonl" sleep \$1
EOS
chmod +x $T/fakescan.sh
X="FAKE_R=0.1178"; MAXP=2
case $SC in
  ok) ( sleep 15; echo "2026-11-28 00:00:00 UTC [r3] secant starts: fake" >> $T/r3/steps.txt ) & ( sleep 2; $T/fakescan.sh 60 other1 ) & ( sleep 2; $T/fakescan.sh 60 other2 ) & export FAKE_EV=6 FAKE_N=8 ;;
  cap) touch $T/r3/DONE_r3.txt; export FAKE_EV=6 FAKE_N=40 CAP=20 ;;
  widen) touch $T/r3/DONE_r3.txt; export FAKE_R=0.2 FAKE_R_WIDE=0.08 FAKE_EV=2 FAKE_N=4 ;;
  bar1) export FAKE_STEPS35=8350 ;;
  bar1f) export FAKE_F35=7e-10 ;;
  bar2) export FAKE_STEPS34=8351 ;;
  jac3) export FAKE_JAC_RC=3 ;;
esac
export SCAN_PAT="^$PY -u .*d18_secant\\.py scan (root1110|/dryin/)"   # the real scanner processes of the machine are not counted
export DRY=1 OUT=$T/out WT=$T WTM=$T/wtm PY=$PY R3=$T/r3 UP=i1110t YTICK=2 MAXP=2 ADMIT_POLL=2 ADMIT_SETTLE=20 ADMIT_TICK=1
timeout 900 bash $T/out/run_1110.sh; echo "driver exit $?"
cut -c1-260 $T/out/steps.txt | grep -E 'STOP|bar|jac|svd|chord|coords|root|results|done' | grep -v 'selftest'
cat $T/out/DONE_1110.txt $T/out/STOP_1110.txt 2>/dev/null; tail -6 $T/out/results_1110.md 2>/dev/null | cut -c1-240
echo "dir $T"
