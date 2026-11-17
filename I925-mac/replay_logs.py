"""Replay the stall rule (#925) on the Newton histories in solve_point logs: per solve, max |F| before each accepted
step and after it (the next step's |F|, the converged line's, or the solve's final |F|). Reports every solve where
the rule (window W, factor f) would have fired, with the solve's outcome."""
import glob
import os
import re
import sys

W = int(sys.argv[2]) if len(sys.argv) > 2 else 3
FAC = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
root = sys.argv[1]

HEAD = re.compile(r"D ([\d.]+) M (\d+): L \d+, steps \d+, start \|F\| (\S+)")
ACC = re.compile(r"^\s+newton \d+: \|F\| (\S+) \|dz\| (\S+) lam (\S+)")
CONV = re.compile(r"^\s+newton \d+: \|F\| (\S+) converged")
LSF = re.compile(r"^\s+newton \d+: \|F\| (\S+): no decrease along the Newton step")
END_OK = re.compile(r"D ([\d.]+) M (\d+): Delta \S+ \(\S+\) \|F\| (\S+) its (\d+)")
END_NO = re.compile(r"D ([\d.]+) M (\d+): NOT converged, \|F\| (\S+)")
CHORD = re.compile(r"^\s+chord \d+: max\|F\| (\S+) -> ")


def solves(path):
    cur = None
    for ln in open(path, errors="replace"):
        m = HEAD.search(ln)
        if m:
            if cur:
                yield cur
            cur = dict(file=path, D=m.group(1), M=int(m.group(2)), F0=float(m.group(3)), steps=[], after=[], end=None,
                       final=None)
            continue
        if cur is None:
            continue
        m = ACC.search(ln)
        if m:
            F = float(m.group(1))
            if len(cur["after"]) < len(cur["steps"]):
                cur["after"].append(F)
            cur["steps"].append((F, float(m.group(3))))
            continue
        m = CHORD.search(ln)
        if m and len(cur["after"]) < len(cur["steps"]):
            cur["after"].append(float(m.group(1)))
            continue
        for rx, kind in ((CONV, "conv_line"), (LSF, "ls_fail")):
            m = rx.search(ln)
            if m:
                if len(cur["after"]) < len(cur["steps"]):
                    cur["after"].append(float(m.group(1)))
                cur["last"] = kind
                cur["Fconv"] = float(m.group(1))
                break
        for rx, kind in ((END_OK, "converged"), (END_NO, "failed")):
            m = rx.search(ln)
            if m and m.group(1) == cur["D"] and int(m.group(2)) == cur["M"]:
                cur["end"] = kind
                cur["final"] = float(m.group(3))
                if len(cur["after"]) < len(cur["steps"]):
                    cur["after"].append(float(m.group(3)))
                yield cur
                cur = None
                break
    if cur:
        yield cur


rows = []
n = dict(solves=0, full=0, conv=0, failed=0, open=0)
for p in sorted(glob.glob(os.path.join(root, "**", "*.log"), recursive=True)
                + glob.glob(os.path.join(root, "**", "*.txt"), recursive=True)):
    for s in solves(p):
        n["solves"] += 1
        n["conv" if s["end"] == "converged" else "failed" if s["end"] == "failed" else "open"] += 1
        Fb = [f for f, _ in s["steps"]]
        if len(Fb) >= W:
            n["full"] += 1
        fire = None
        for k in range(W - 1, len(Fb)):
            if k >= len(s["after"]):
                break
            Fa = s["after"][k]
            # converged at the next line: below tol, no stall
            if k == len(Fb) - 1 and s.get("last") == "conv_line":
                continue
            if not Fa <= FAC * Fb[k - W + 1]:
                fire = (k, Fb[k - W + 1], Fa)
                break
        if fire:
            rows.append((s, fire))

print(f"window {W}, factor {FAC}: {n['solves']} solves ({n['conv']} converged, {n['failed']} not converged, "
      f"{n['open']} without an end line), {n['full']} with at least {W} accepted steps; the rule fires in {len(rows)}")
for s, (k, Fa0, Fa) in rows:
    lams = [lam for _, lam in s["steps"]]
    print(f"  {os.path.relpath(s['file'], root)}: D {s['D']} M {s['M']}: {s['end']} (final |F| {s['final']}), "
          f"{len(lams)} steps, lams {lams}; fires after step {k}: |F| {Fa0:.2e} -> {Fa:.2e}; "
          f"Fs {[f'{f:.1e}' for f, _ in s['steps']]}")
