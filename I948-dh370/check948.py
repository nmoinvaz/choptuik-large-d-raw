"""#948: has a ks-ladder rung's base polish converged, and did the run write only the base?

    python check948.py RUNG_DIR K [--mutate]       (run with the 935 worktree's .venv; exit 0 pass, 1 not converged, 3 other files)

RUNG_DIR is an anm_run.py output directory (--steps 0 --save_base 1). Pass: it holds base_pin3_D232.0000.npz whose meta says
base_polish converged, max|F| (the polish's final octo-double max|F|) at most 1e-60, and ks equal to K. Other files than the base,
anm_run.jsonl and anm_run.log are reported (exit 3: --steps 0 should write nothing past the base). --mutate reads max|F| as 1e-50,
and the check must then fail (exit 1)."""
import os
import sys

sys.path.insert(0, "/home/nathan/Source/choptuik-large-d-935/hp")
from octo_corrector import load_o  # noqa: E402

d, K = sys.argv[1], int(sys.argv[2])
mut = "--mutate" in sys.argv
base = os.path.join(d, "base_pin3_D232.0000.npz")
extra = sorted(set(os.listdir(d)) - {"base_pin3_D232.0000.npz", "anm_run.jsonl", "anm_run.log"})
if not os.path.exists(base):
    print(f"{d}: no base_pin3_D232.0000.npz (files: {sorted(os.listdir(d))})")
    sys.exit(1)
z, m = load_o(base)
bp = m.get("base_polish", {})
mf = float(bp["max_F"][-1] if isinstance(bp.get("max_F"), (list, tuple)) else bp.get("max_F", float("inf")))
if mut:
    mf = 1e-50
ok = bool(bp.get("converged")) and mf <= 1e-60 and int(m["ks"]) == K
print(f"{d}: D {m['D']}, ks {m['ks']} (asked {K}), base_polish converged {bp.get('converged')}, max|F| {mf:.2e}: {'pass' if ok else 'FAIL'}"
      + (" (--mutate: max|F| read as 1e-50, must FAIL)" if mut else ""))
if extra:
    print(f"  files past the base: {extra}")
sys.exit(1 if not ok else (3 if extra else 0))
