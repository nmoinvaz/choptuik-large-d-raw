#!/usr/bin/env python3
"""One table over the planted-zero runs of #585: the registered noise (sigma of the near points) and the exploratory ones (sigma 1e-3, sigma of the far points).
Per run and circle: sigma used, the range over the four phi of the rms error of lam0 (from the planted position), the rms movement (from the noise-free recovered position), the rms error over the
circle's own estimate, and the fraction of the 200 realizations whose error exceeds the own estimate. usage: python sweep_table_585.py"""
import glob, json, os
H = os.path.dirname(os.path.abspath(__file__))
runs = [("registered: near points", ""), ("exploratory: 1e-3", "_mid"), ("exploratory: far points", "_far")]
print("| run | sigma ln, arg | circle | own estimate | noise-free error | rms error | rms movement | rms / estimate | realizations over the estimate |\n|---|---|---|---|---|---|---|---|---|")
rng = lambda v, f="%.2e": (f % min(v)) if min(v) == max(v) else (f % min(v)) + " to " + (f % max(v))
for label, tag in runs:
    for c in "AB":
        rows = [json.load(open(p)) for p in sorted(glob.glob(os.path.join(H, f"planted_585{tag}_{c}_*.json")))]
        assert len(rows) == 4 and all(r["nreal"] == 200 and r["bad_realizations"] == 0 and not r["capped"] for r in rows), (tag, c)
        s = f"{rows[0]['sigma_ln']:.2e}, {rows[0]['sigma_arg']:.2e}"
        print(f"| {label} | {s} | {c} | {rng([r['est0'] for r in rows])} | {rng([r['err0'] for r in rows])} | {rng([r['rms_err'] for r in rows])} | {rng([r['rms_move'] for r in rows])} | "
              f"{rng([r['rms_over_est'] for r in rows], '%.2f')} | {rng([r['frac_over_est'] for r in rows], '%.2f')} |")
