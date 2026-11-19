import re, sys
N = int(sys.argv[1])
O = "/Users/nathan/Source/choptuik-large-d-raw-903/I903-macm3"
L = open(f"{O}/chain_k135.log").read().splitlines()
cap = re.search(r"--qd_it (\d+)", open(f"{O}/run_903_k135.sh").read()).group(1)
i0 = next(i for i, l in enumerate(L) if l.startswith(f"step {N}: D ") and "pivots" in l)
j0 = next(i for i, l in enumerate(L) if l.startswith(f"step {N+1}: the series saved"))
seg = L[i0:j0]
ends = [i for i, l in enumerate(seg) if re.match(r"\s+a [0-9.]+ -> D ", l)]
prev = 0
out = []
for k, e in enumerate(ends, 1):
    blk = seg[prev:e + 1]; prev = e + 1
    a = re.match(r"\s+a ([0-9.]+) -> D", blk[-1]).group(1)
    rows = []
    for l in blk:
        m = re.match(r"\s+on (\d+): \|F\| \S+ -> (\S+), \|dz\| \S+ -> \S+, lam ([0-9.]+)", l)
        if m: rows.append((m.group(2), m.group(3)))
    nh = sum(1 for r in rows if r[1] == "0.5")
    out.append((k, a, rows, nh))
print(f"\nThe octo-double Newton's corrections, from the log's `on k:` lines (`--qd_it {cap}` is the cap in the chain's command, `run_903_k135.sh`):\n")
for k, a, rows, nh in out:
    print(f"- attempt {k} (a {float(a):.4g}): {len(rows)} corrections (the table counts the final convergence check as a step when converged), {nh} of them at lam 0.5. max|F| after each correction: " + ", ".join(r[0] for r in rows) + ".")
    print(f"  lam: " + ", ".join(r[1] for r in rows) + ".")
print("\nAt lam 0.5 the max|F| halves each step, so the corrections near the cap are mostly these halving ones. This note reports it and changes nothing.")
