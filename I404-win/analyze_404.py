#!/usr/bin/env python3
"""#404: the per-D table and the verdict of the criteria in README.md, from rt_grids.py's output for each grid.
usage: python analyze_404.py D60.0020|D54.9961|D50.0075|D40.0201     (run from this folder)
For each N in the ladder with both roots' records: `rt_grids.py roots/a101_32xN.jsonl roots/b121_32xN.jsonl --D <D> --tol 1e-14` through rt_launch.py (log fit/verdict_32xN_<Dtag>.log); its row gives
A - hp, B - hp and A - B in arb from the records' 30-digit Delta. E(N) = max(|A - hp|, |B - hp|); the grid passes when rt_grids.py exits 0 (both converged records, both within 1e-14 of hp, spread below 1e-14).
Verdict (README): the ladder FALLS to below 1e-14 when some grid N* passes and E decreases strictly along the ladder up to N* (or N* is the first rung); otherwise it STOPS FALLING at N_s, the first rung
whose E is not below the previous rung's (or the rung with the smallest E if E falls to the end)."""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PY = r"C:\Users\nathan\Source\venv-t151\Scripts\python.exe"
REPO = r"C:\Users\nathan\Source\choptuik-i404"
DVAL = {"D60.0020": "60.001952", "D54.9961": "54.996085", "D50.0075": "50.007491", "D40.0201": "40.020065"}
LADDER = (99, 103, 107, 111, 115, 119, 123)


def grid_row(N, dtag):
    a, b = os.path.join("roots", f"a101_32x{N}.jsonl"), os.path.join("roots", f"b121_32x{N}.jsonl")
    if not (os.path.exists(os.path.join(HERE, a)) and os.path.exists(os.path.join(HERE, b))):
        return None
    cmd = [PY, os.path.join(HERE, "rt_launch.py"), os.path.join(REPO, "solver", "rt", "rt_grids.py"), a, b, "--D", DVAL[dtag], "--tol", "1e-14", "--table"]
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=HERE, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    os.makedirs(os.path.join(HERE, "fit"), exist_ok=True)
    open(os.path.join(HERE, "fit", f"verdict_32x{N}_{dtag}.log"), "w", encoding="utf-8").write(p.stdout + p.stderr + f"\nexit {p.returncode}\n")
    row = [ln for ln in p.stdout.splitlines() if ln.startswith(f"| {float(DVAL[dtag])}") or ln.startswith(f"| {DVAL[dtag]}")]
    if not row:
        return dict(N=N, exit=p.returncode, missing=True, text=p.stdout.strip().splitlines()[-1] if p.stdout.strip() else p.stderr.strip()[-200:])
    f = [x.strip() for x in row[0].strip("|").split("|")]
    if f[1].startswith("missing"):
        return dict(N=N, exit=p.returncode, missing=True, text=f[1])
    num = lambda s: float(s)
    return dict(N=N, exit=p.returncode, missing=False, delta=f[1], ea=num(f[2]), eb=num(f[3]), dab=num(f[4]), verdict=f[5])


def main():
    dtag = sys.argv[1]
    rows = [r for r in (grid_row(N, dtag) for N in LADDER) if r]
    print(f"== D {DVAL[dtag]}: Delta_RT - Delta_hp of the two roots on each grid (rt_grids.py --tol 1e-14)")
    print("| N | root a - hp | root b - hp | spread a - b | E(N) | passes 1e-14 |\n|---|---|---|---|---|---|")
    E = []
    for r in rows:
        if r["missing"]:
            print(f"| {r['N']} | missing | | | | no ({r['text'][:60]}) |")
            E.append(None)
            continue
        e = max(abs(r["ea"]), abs(r["eb"]))
        E.append(e)
        print(f"| {r['N']} | {r['ea']:+.2e} | {r['eb']:+.2e} | {r['dab']:+.2e} | {e:.2e} | {'yes' if r['exit'] == 0 else 'no'} |")
    ok = [i for i, r in enumerate(rows) if not r["missing"] and r["exit"] == 0]
    have = [i for i, e in enumerate(E) if e is not None]
    if len(have) < len(LADDER):
        print(f"\n(partial: {len(have)} of {len(LADDER)} grids have both roots)")
    if ok:
        k = ok[0]
        falls = all(E[i] is not None and E[i + 1] is not None and E[i] > E[i + 1] for i in range(k))
        if falls:
            print(f"\nVERDICT {dtag}: the ladder FALLS to below 1e-14 at N* = {rows[k]['N']} (E = {E[k]:.2e}, spread {abs(rows[k]['dab']):.2e})" + ("" if k else " (the first rung)"))
            return
    ns = None
    for i in have[:-1]:
        j = have[have.index(i) + 1]
        if E[j] >= E[i]:
            ns = i
            break
    if ns is None and have:
        ns = min(have, key=lambda i: E[i])
    if ns is not None:
        r = rows[ns]
        print(f"\nVERDICT {dtag}: the ladder STOPS FALLING at N_s = {r['N']}: E = {E[ns]:.2e}, spread {abs(r['dab']):.2e}, signs (a, b) {'+' if r['ea'] > 0 else '-'}{'+' if r['eb'] > 0 else '-'}"
              + ("" if not ok else f"; a grid passes (N = {rows[ok[0]]['N']}) but E does not fall strictly up to it"))


if __name__ == "__main__":
    main()
