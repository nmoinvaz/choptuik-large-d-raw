#!/usr/bin/env python3
"""control_demo1067.py CKPT FACTOR TAG: the scaled checkpoint control of run1067_s1.py on one checkpoint, as the production path runs it (run1067_s1.resid): the as-saved max|F| F, the nominal plant P = 1e3 F, the plant actually applied FACTOR * P (1: the
control must detect it, reading within [P/2, 2P]; 0: nothing planted, the control must report the miss) and the control's verdict plant_ok(F, P, reading). Exit 0 when the verdict is as expected for FACTOR (ok for 1, miss for 0), else 1."""
import sys

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import run1067_s1 as s  # noqa: E402

ck, factor, tag = sys.argv[1], float(sys.argv[2]), sys.argv[3]
F, P, reading = s.resid(ck, tag, factor)
ok = s.plant_ok(F, P, reading)
want = factor > 0
print(f"checkpoint {ck.split('/')[-1]}: as-saved max|F| {F:.3e}; nominal plant P {P:.3e}, applied {factor * P:.3e}; reading {reading:.3e}; control {'DETECTS the plant' if ok else 'REPORTS THE MISS (plant not seen)'}; expected {'detect' if want else 'miss'}: {'as expected' if ok == want else 'UNEXPECTED'}")
sys.exit(0 if ok == want else 1)
