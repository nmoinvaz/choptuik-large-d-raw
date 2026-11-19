import re, json, sys, datetime
N = int(sys.argv[1])
O = "/Users/nathan/Source/choptuik-large-d-raw-903/I903-macm3"
L = open(f"{O}/chain_k135.log").read().splitlines()
rs = [json.loads(l) for l in open(f"{O}/chain_k135/anm_run.jsonl")]
r = rs[N]
i0 = next(i for i, l in enumerate(L) if l.startswith(f"step {N}: D ") and "pivots" in l)
j0 = next((i for i, l in enumerate(L) if i > i0 and l.startswith(f"step {N+1}: the series saved")), len(L))
seg = L[i0:j0]
ends = [i for i, l in enumerate(seg) if re.match(r"\s+a [0-9.]+ -> D ", l)]
att, prev = [], 0
for e in ends:
    blk = seg[prev:e + 1]; prev = e + 1
    a, Dt = re.match(r"\s+a ([0-9.]+) -> D ([0-9.]+)", blk[-1]).groups()
    sec = int(re.search(r"moved \S+, (\d+) s", blk[-1]).group(1))
    rs_ = next((re.sub(r"^a [0-9.]+: ", "", l.strip()) for l in blk if "re-seeded" in l), "")
    ods = next((l.strip() for l in blk if "octo-double Newton" in l), None)
    m = re.search(r"(\d+) steps, max\|F\| (\S+), (not converged|converged)", ods) if ods else None
    th = [re.search(r"theta at its point (\S+) \(bound (\S+)\): (\w+)", l).groups() for l in blk if "theta at its point" in l]
    att.append((a, Dt, sec, rs_.replace("|R|", "\\|R\\|"), m.groups() if m else None, th))
assert len(att) == len(r["attempts"]), (len(att), len(r["attempts"]))
print(f"## #903 macm3b: step {N} (base D {float(r['D0']):.5f}) took {len(att)} attempts and ended at a {float(att[-1][0]):.4g} ({datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d %H:%M UTC')})\n")
print("Read from `chain_k135.log`. The chain continues, nothing changed. The progress table is in the post just before this one.\n")
print("| attempt | a | target D | start (re-seed) | octo-double Newton | outcome | wall s |\n|---|---|---|---|---|---|---|")
for k, (a, Dt, sec, rs_, m, th) in enumerate(att, 1):
    nt = f"{m[0]} steps, max\\|F\\| {m[1]}, {m[2]}" if m else "none"
    out = "refused at the start" if m is None else ("accepted" if m[2] == "converged" else "refused (not converged)")
    print(f"| {k} | {float(a):.4g} | {Dt} | {rs_} | {nt} | {out} | {sec} |")
tot = sum(x[2] for x in att)
ser = re.search(r", (\d+) s$", L[i0]).group(1)
print(f"\nThe attempts took {tot} s in all ({tot/3600:.2f} h), plus {ser} s for the series at the base. Record {N}: p_min {r['pivots'][0]:.4e} at the base, a_max {r['a_max']:.3f}, converged {r['converged']}, the state reached D {r['attempts'][-1]['D']:.9f}. Refused attempts so far: {sum(len(x['attempts'])-1 for x in rs)} over {len(rs)} records.")
