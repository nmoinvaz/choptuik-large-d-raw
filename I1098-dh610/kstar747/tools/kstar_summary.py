"""The k* stage's summary (#1098): the first-order bound on Delta at kfree K before and after the k* system's
re-converge, as kstar.json for ladder_record.py --kstar_json.

    python3 kstar_summary.py TAIL_LOG.jsonl K GAIN OUT.json [RECONV_LOG.jsonl START.npz]

TAIL_LOG: the tail's release_ls.jsonl, whose release record of harmonic K gives F_before (the target system's |F| at
K's release). bound_before = GAIN x F_before. RECONV_LOG (release_ls at kmax K from START, the h<K> state): F_after is
its last target |F| (the release record's, or the last accepted step's), shift its Delta minus START's, and
bound_after = GAIN x F_after + |shift| (the bound at the re-converged state plus the move from the state the point's
later harmonics started from).
"""
import json
import sys

from mpmath import mp

from octo_corrector import delta_digits, load_o


def records(path):
    with open(path) as fh:
        return [json.loads(line) for line in fh if line.strip()]


def main():
    a = sys.argv[1:]
    tail, k, gain, out = a[0], int(a[1]), float(a[2]), a[3]
    mp.dps = 50
    rel = [r for r in records(tail) if r.get("harm") == k and r.get("done")]
    if not rel:
        raise SystemExit(f"{tail}: no release record of h{k}")
    Fb = float(rel[-1]["F"])
    res = dict(kstar=k, gain=gain, F_before=Fb, bound_before=gain * Fb, rule="re-converge when gain x F_before > 1e-27",
               reconv=False)
    if len(a) > 4:
        rc = records(a[4])
        d0 = mp.mpf(delta_digits(load_o(a[5])[0], 40))
        acc = [r for r in rc if r.get("accepted") and "Delta" in r]
        done = [r for r in rc if r.get("done")]
        Fa = done[-1]["F"] if done else (acc[-1]["F_new"] if acc else None)
        d1 = mp.mpf(acc[-1]["Delta"]) if acc else d0
        if Fa is not None:
            sh = float(d1 - d0)
            res.update(reconv=True, released=bool(done), F_after=float(Fa), Delta_start=mp.nstr(d0, 40),
                       Delta_after=mp.nstr(d1, 40), shift=sh, bound_after=gain * float(Fa) + abs(sh))
    with open(out, "w") as fh:
        json.dump(res, fh, indent=1)
    print(json.dumps(res), flush=True)


if __name__ == "__main__":
    main()
