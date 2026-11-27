# I1098-mm5/ladder/D8000: D 8000's M 32 stages by recipe v2's amendment 2 (the L-20 last node, the downward ks gate) on fastmul7 (#1098)

Part of `../`. Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

Coordinator's order (2026-11-27 06:31 UTC): D 8000, the ladder's top point, moved here from win2's queue, into D 2231's 6 freed threads, now (no wait):

```
TC=c281b00d3dd00ab1a9f9880cb332bf1b14325433 bash tools3/d8000_mm5.sh        # detached, from the ladder folder
```

`tools3/d8000_mm5.sh` (raw 92fe0208e `I1098-mac-a/tools/mm5/d8000_mm5.sh`, blob a1b357b41cc455ac19d53fb98345b5543d49e6d4, verified and read; it is `d6666_mm5.sh` without the wait). It writes the tools pinned at raw TC c281b00d3 into `tools4/` (`ladder_new.sh` 3039e5b9, `ladder_point2.sh` e0cf5880 checked in the script, the others), writes the three sources from their blobs into `../inputs`
(#1088's lastnode states at D 4000, 5657 and 8000: f06d04d5, 127bbb58, 511a1ff8; at D 8000 the last is the lastnode state itself), and **installs `ks_gate.py` of wip/large-d-form-s 3b3bfc60 (blob a91c7363c93ccb2355ea5b72a29f0f9c600cf4b7; `--down`, `--ks0`) as `~/Source/choptuik-fastmul7/hp/ks_gate.py`** (the install time is in `setup.log`, and noted in `../D4000/README.md`).
It is safe for the running points: the diff of the two versions adds only the downward gate and `--ks0` (read here: the options and defaults of the upward gate are unchanged); D 2828 and D 1549 passed their gates already, and D 4000's tail uses the upward gate.

Stages (`tools4/ladder_new.sh`): the guess by `form_s_lastnode.py guess` (degree 2 in 1/n from the three sources, carried outward to the last node **x_l 0.7062221251334241**, D 8000's own L = 20 node), the jump from it (degree 0, held, the Moebius horizon a = max(8, n/400) = **19.995**, start ks = ceil(1.5 n) + 20 = **12017**, kc 260, dd then qd, it_max 12),
then `ladder_point2.sh` with the downward gate (`--down 1 --step 100 --ks0 9600`), KSBAR 1e-64, h5..h11 and h13 (STOP_AFTER=rls13; the M 48 tail is a later job). fastmul7 (d40a9c62 with that `ks_gate.py`, kernel `~/Source/fastmul7-site`), chord-free, kc 260, 6 threads. Output in `D8000/`; the last act writes "job rc N" to its `run.log`.

## Bars, written before the run (as D 6666's; coordinator's order)

- The guess is built and its max |F| reported (**expect about 1e-16 in every block**; dh610's ratio test read 1.1e-16). The jump converges, and its kc+20 line reads |dF| 0 or below its bar (the jump's discretization bar, 1e-25).
- The downward ks gate passes the bar 1e-64: log the ks it settles on (**expect about 1.09 n, 8700**) and its octo-double change. h5..h13 are each released.
- Stop rules (amended): stop and report when a qq inner solve does not converge, when a harmonic's line search fails at every trial, or when an outer step is 3x its harmonic's first. A qd inner floor that hands over to qq is logged, not stopped.
- Pilot: report the guess's max |F|, the jump's time, the gated ks and h5 outer 0's time. Times from `date -u`.
