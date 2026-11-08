"""I178-macm3: the circles of the scan (circles.jsonl) and of the locating rounds (circles_locate.jsonl) as tables.    python3 summarize.py"""
import json, os

for fn in ("circles.jsonl", "circles_locate.jsonl"):
    if not os.path.exists(fn):
        continue
    print(f"\n{fn}\n| tag | kf | setup F | center | R | winding | points | max step | mismatches |\n|---|---|---|---|---|---|---|---|---|")
    for ln in open(fn):
        r = json.loads(ln)
        print(f"| {r['tag']} | {r['kfreeze']} | {r['F']:.1e} | {r['center'][0]:.4f} | {r['R']} | {r['winding']:+.6f} | {r['points']} | {r['max_step']:.3f} | {r['verify_mismatch']} |")
