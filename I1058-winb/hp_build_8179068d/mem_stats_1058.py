#!/usr/bin/env python3
"""#1058 winb: peaks from mem_1058.csv (the 30 s alert-only watcher). Window of the build: 2026-11-20 21:29:45 to 23:29:50 UTC (hp1058b_build.log)."""
import csv, sys
HERE = "C:/Users/nathan/Source/hp1058_winb/"
rows = list(csv.DictReader(open(HERE + "mem_1058.csv")))
T0, T1 = "2026-11-20 21:29:45", "2026-11-20 23:29:50"
inb = [r for r in rows if T0 <= r["utc"] <= T1]
out = []
def say(s):
    print(s); out.append(s)
say(f"samples: {len(rows)} ({rows[0]['utc']} to {rows[-1]['utc']}), in the build window {len(inb)}")
say(f"before the build (first sample {rows[0]['utc']}): commit {rows[0]['commit_gb']} of limit {rows[0]['limit_gb']} GB, available {rows[0]['avail_gb']} GB, page file allocated {rows[0]['pf_alloc_mb']} MB used {rows[0]['pf_used_mb']} MB (peak since boot {rows[0]['pf_peak_mb']}), C: free {rows[0]['c_free_gb']} GB")
def peak(k, fn, rs, label, unit):
    v = [float(r[k]) for r in rs]; x = fn(v); r = rs[v.index(x)]
    say(f"{label}: {x:g} {unit} at {r['utc'][11:]} UTC")
peak("commit_gb", max, inb, "commit charge, peak", "GB")
peak("limit_gb", max, inb, "commit limit, max", "GB")
peak("avail_gb", min, inb, "available memory, min", "GB")
peak("pf_alloc_mb", max, inb, "page file allocated, max", "MB")
peak("pf_used_mb", max, inb, "page file in use, max", "MB")
peak("pf_peak_mb", max, inb, "page file PeakUsage counter, max", "MB")
peak("c_free_gb", min, inb, "C: free, min", "GB")
peak("rustc_ws_gb", max, inb, "biggest rustc working set, max", "GB")
peak("rustc_priv_gb", max, inb, "biggest rustc private bytes, max", "GB")
peak("rustc_n", max, inb, "rustc processes at once, max", "")
peak("python_ws_gb_top", max, inb, "biggest python working set, max (the other session's or P4's, not the build's)", "GB")
rr = [r for r in rows if int(r["rustc_n"]) > 0]
say(f"rustc seen from {rr[0]['utc'][11:]} to {rr[-1]['utc'][11:]} UTC; samples with commit above 40 GB: {sum(float(r['commit_gb']) > 40 for r in inb)}; with available under 1 GB: {sum(float(r['avail_gb']) < 1 for r in inb)}")
a0 = float(rows[0]["pf_alloc_mb"]); am = max(float(r["pf_alloc_mb"]) for r in inb)
say(f"page file growth: allocated {a0:g} -> peak {am:g} MB (+{am - a0:g} MB); last sample {rows[-1]['utc'][11:]} UTC: allocated {rows[-1]['pf_alloc_mb']} MB, used {rows[-1]['pf_used_mb']} MB, C: free {rows[-1]['c_free_gb']} GB")
open(HERE + "mem_stats_1058.txt", "w").write("\n".join(out) + "\n")
