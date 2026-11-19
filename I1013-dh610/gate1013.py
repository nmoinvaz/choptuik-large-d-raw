#!/usr/bin/env python3
"""gate1013.py COUNT.json [--mutate=shift]: the pilot's pre-registered reading (xfchecks, #1013): one zero of sign +1 located at (2.72648, 1.01560) to 1e-4 at xi1 0.2 (located)
and again at 0.17 (located_r1b), with no unresolved cells. --mutate=shift moves the located A by 2e-4 first, which must fail. Exit 0 pass, 1 fail."""
import json
import sys

d = json.load(open(sys.argv[1]))
shift = 2e-4 if "--mutate=shift" in sys.argv else 0.0
A0, W0, tol = 2.72648, 1.01560, 1e-4
msgs = []
z = d["zeros"]
if len(z) != 1:
    msgs.append(f"{len(z)} zeros, not 1")
else:
    z = z[0]
    if z["W"] != 1:
        msgs.append(f"sign {z['W']:+d}, not +1")
    for key in ("located", "located_r1b"):
        loc = z.get(key)
        if not loc:
            msgs.append(f"{key}: not located")
            continue
        dA, dw = loc["A"] + shift - A0, loc["wf"] - W0
        print(f"{key}: A {loc['A'] + shift:.6f}, wf {loc['wf']:.6f}; difference from ({A0}, {W0}): {dA:+.2e}, {dw:+.2e}")
        if abs(dA) > tol or abs(dw) > tol:
            msgs.append(f"{key} off by ({dA:+.2e}, {dw:+.2e}) > {tol}")
if d["unresolved"]:
    msgs.append(f"{len(d['unresolved'])} unresolved cells")
print(("PASS" if not msgs else "FAIL: " + "; ".join(msgs)) + (" (control --mutate=shift)" if shift else ""))
sys.exit(0 if not msgs else 1)
