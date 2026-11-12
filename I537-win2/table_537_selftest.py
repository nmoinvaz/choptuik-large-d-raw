#!/usr/bin/env python3
"""#537: the verdict rule of table_537.py on planted shifts. usage: python table_537_selftest.py (exits 1 if a planted case is judged wrongly)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from table_537 import verdict
cases = (((41.0, -13.7), (True, False)), ((36.0, -12.0), (True, False)), ((30.0, -13.7), (False, False)), ((0.0, 6.7), (False, True)), ((3.0, 13.4), (False, True)),
         ((9.0, 6.7), (False, False)), ((0.0, -3.0), (False, False)), ((41.0, 6.7), (False, False)))
bad = 0
for (f, l), want in cases:
    got = verdict(f, l)
    print(f"first {f:+.1f}, last {l:+.1f}: fast {got[0]}, G^p {got[1]} (wanted {want})" + ("" if got == want else "  WRONG"))
    bad += got != want
print("selftest: ok" if not bad else f"selftest FAILED ({bad})")
sys.exit(1 if bad else 0)
