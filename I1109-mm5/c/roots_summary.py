#!/usr/bin/env python3
"""#1109 stage 1c: the three roots' records (root_*.jsonl): robust bracket, status, lam_lin, bar 2, dln growth (run from c/)."""
import json
REF = 0.045967998
for n in ("r0", "w01", "w10"):
    rs = [json.loads(l) for l in open(f"root_{n}.jsonl") if l.strip()]
    ev = [e for e in rs if e.get("kind") != "root"]
    fin = [e for e in rs if e.get("kind") == "root"]
    lo = max(e["lam"] for e in ev if e["sign"] > 0 and e.get("robust"))
    hi = min(e["lam"] for e in ev if e["sign"] < 0 and e.get("robust"))
    print(f"{n}: {len(ev)} evaluations; robust bracket [{lo!r}, {hi!r}] width {hi - lo:.4e}; "
          + (f"status {fin[-1]['status']} ({fin[-1]['why']}), lam_lin {fin[-1]['lam_lin']!r}, {fin[-1]['sec']} s" if fin else "no root record (stopped by the gate, SIGTERM)"))
    if fin:
        d = fin[-1]["lam_lin"] - REF
        print(f"   bar 2: lam_lin - {REF} = {d:+.4e}; |d| <= 1e-5: {abs(d) <= 1e-5}; dh170's value inside the final bracket: {fin[-1]['bracket'][0] <= REF <= fin[-1]['bracket'][1]}")
    print("   evaluations (lam, hybrid sign, float64 sign, dln, robust):")
    for e in sorted(ev, key=lambda e: e["lam"]):
        print(f"     {e['lam']!r:24} {int(e['sign']):+d} {int(e['f64_sign']):+d} dln {e['dln']:.2e} {e['robust']}" if e.get("dln") is not None else
              f"     {e['lam']!r:24} {int(e['sign']):+d} {int(e['f64_sign']):+d} dln - {e['robust']}")
