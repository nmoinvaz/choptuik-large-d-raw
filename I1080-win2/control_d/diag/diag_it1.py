"""#1080 walk d, diagnosis of iteration 1: the same centre call as zero_mp's newton() makes at iteration 1, with a line per
residual call. It does not touch the walk. Code: worktree choptuik-i1080d (feat/inner-mp 73dcf243) unchanged; the residual is wrapped
here to print its max |r_3..r_5| and the seconds, which is all VALUE_MP_PROGRESS=1 prints in later commits.

    python -u diag_it1.py ROWS.jsonl     (ROWS = walk d's rows; the centre of the next iteration is built from the last row)
"""
import json
import sys
import time

sys.path.insert(0, r"D:\choptuik-i1080d\solver\inner_stokes")
import mpmath as mp  # noqa: E402
import inner_mp as IM  # noqa: E402
import value_mp as VM  # noqa: E402

row = [json.loads(l) for l in open(sys.argv[1]) if l.strip()][-1]
A, wf = row["A"] + float(row["dA"]), row["wf"] + float(row["dwf"])        # zero_mp: A + float(dx[0]), wf + float(dx[1])
print(f"centre of iteration {row['it'] + 1}: A {A!r} wf {wf!r}; v0 {[s[:18] for s in row['F3']]}; chord J from row {row['it']}'s J_inner",
      flush=True)
t0, n = time.time(), [0]
orig = IM.residual_demixed


def wrapped(*a, **k):
    out = orig(*a, **k)
    n[0] += 1
    print(f"  call {n[0]} dps {mp.mp.dps}: max|r3..r5| {mp.nstr(max(abs(x) for x in out[0][2:]), 3)}, {time.time() - t0:.0f} s", flush=True)
    return out


IM.residual_demixed = wrapped
res = VM.value_v(repr(A), repr(wf), list(row["F3"]), 5, r1="0.17", J=row["J_inner"], want_J=True)
res.pop("J", None)
print(json.dumps(res), flush=True)
print(f"done: {n[0]} calls, {time.time() - t0:.0f} s", flush=True)
