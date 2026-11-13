"""#713 pilot: the residual that ElimO's projection leaves at a converged point, with the quad-double projection alone
(reseed_o 0) and with three octo-double corrections of its horizon data (reseed_o 3). With switch 0 every point of the
corrector is projected, so this residual is a floor of the corrector.

    cd hp && python3 pilot_floor.py RAW STATE CONVERGED [--threads 3]

STATE: the planted check's truth state (its pinned system is built exactly as octo_corrector.planted builds it).
CONVERGED: an eight-part point converged on that system (octo_corrector.planted --out). Prints the pinned octo-double
max|F| at CONVERGED, then at its projection for each reseed_o, with the max per row block (crawl_probe.per_block)."""
import json
import os
import sys
import time

sys.path.insert(0, os.getcwd())


def main(argv):
    import mpmath as mp
    from crawl_probe import per_block
    from hpkernel.driver import load_q
    from octo_corrector import ElimO, load_o, o8, omax, pinned_o
    from reseed import Reseeder
    raw, state, conv = argv[0], argv[1], argv[2]
    threads = int(argv[argv.index("--threads") + 1]) if "--threads" in argv else 3
    z4, meta = load_q(os.path.join(raw, state))
    z4 = o8(z4)
    D = mp.mpf(meta["D_str"])
    M, K = int(meta["M"]), len(meta["nodes"])
    s, sp, sq, so = pinned_o(meta, z4, threads=threads)
    zc, _ = load_o(os.path.join(raw, conv))
    F = so.residual_o(zc)
    out = dict(state=state, converged=conv, D_str=meta["D_str"], F_conv=omax(F), blocks_conv=per_block(F[0] + F[1], M, K))
    print(f"pilot {state} at {conv}: D {mp.nstr(D, 12)}, pinned max|F| (octo) at the converged point {out['F_conv']:.3e}",
          flush=True)
    print(f"  per block {json.dumps({k: f'{v:.1e}' for k, v in out['blocks_conv'].items()})}", flush=True)
    for od in (0, 3):
        rs = Reseeder(meta, D, threads=threads, qd=True, od=od)
        el = ElimO(so, rs, switch=0.0)
        t0 = time.time()
        zp = el.project(zc)
        Fp = so.residual_o(zp)
        rec = dict(F=omax(Fp), blocks=per_block(Fp[0] + Fp[1], M, K), counts=dict(el.counts), seconds=round(time.time() - t0, 1),
                   rung=[float(r) for r in getattr(rs, "last_o", [])] if od else [])
        out[f"reseed_o{od}"] = rec
        print(f"  projected, reseed_o {od}: pinned max|F| (octo) {rec['F']:.3e}, projections {rec['counts']}, "
              f"{rec['seconds']} s" + (f", rung max|R| " + " -> ".join(f"{r:.2e}" for r in rec["rung"]) if od else ""),
              flush=True)
        print(f"  per block {json.dumps({k: f'{v:.1e}' for k, v in rec['blocks'].items()})}", flush=True)
    if "--out" in argv:
        with open(argv[argv.index("--out") + 1], "w") as f:
            f.write(json.dumps(out) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
