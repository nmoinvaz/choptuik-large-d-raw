# I1110-mm5: the root of dh170's kappa-0.35 chord state at k_c 127, D 23.0 (#1110, the root step)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1110 ("l = 1 at D 23, k_c 127: a chord state's root against the LM state's on one map"; its body is the record). Written 2026-11-28 02:41 UTC by the clock, before the run, on the coordinator's order of 2026-11-28 02:40 UTC (R3's freed threads).

The chord state is computed on machine dh170 (task #1110's jac, svd and chord steps, bars 1 and 2) and pushed to raw `I1110-dh170/` as `sol_chord035_D23.0000.npy` and `sol_chord035_D23.0000.map.json`. This folder holds only the root step on this machine. A waiter fetches the raw repository every 10 min (4 h at most) for both files, which are then copied together into `in/`.

## Inputs (blobs by `git hash-object --no-filters`; filled in when the files arrive, and pushed before the run)

| file | where from | blob |
|---|---|---|
| `in/sol_chord035_D23.0000.npy` | `origin/main:I1110-dh170/sol_chord035_D23.0000.npy` | (to be filled) |
| `in/sol_chord035_D23.0000.map.json` | `origin/main:I1110-dh170/sol_chord035_D23.0000.map.json` | (to be filled) |

## Code

Worktree `~/Source/choptuik-1109` at 49664990 (detached): `solver/matter/i1101_weakdir.py` blob 8709abbd and `solver/matter/d18_secant.py` blob eb1396ad (the same blobs as dh170's db7f9c60). `~/venv-314/bin/python`, run from `solver/matter`, `D18_DIR` the worktree's `solver/matter` (the script's default `~/Source/choptuik-kmm` does not exist here), 2 threads (OPENBLAS/OMP/VECLIB = 2), `nice -n 10`, `timeout 14400`.

## Command (the order's)

```
python3 i1101_weakdir.py root CHORDSTATE 0.10 0.13 I1110-mm5/root_chord035.jsonl --tol=1e-6 --b12=fast
```

`root` reads `STATE.map.json` beside the state (both copied into `in/`) and refuses (exit 3) unless the state's |F| on that map equals the saved one to 1e-2. If (0.10, 0.13) does not bracket (the run is refused, exit 2), it is widened once to **(0.05, 0.16)**, written to `root_chord035_wide.jsonl`, and said so in the report.

## Bars (#1110's bar 3, written before the run; bars 1 and 2 are dh170's)

On arrival, checked here as a sanity check, not as the bars: the map's step count equals R2's 8351 and its |F| <= 5e-10.

3. **Report** delta = root(chord) - 0.117824909 (R2's det-linear root), with the root the `lam_lin` of the final record, read only when the run ends with status `tol` (tol 1e-6) and both bracket ends robust with opposite hybrid signs.
   - |delta| <= **2e-3** (under 1/10 of R1 - R2 = 0.0229): the scatter does not hide R0-R2's order, and #1104 may use it.
   - |delta| >= **7e-3** (about 1/3 of it): the order from R0-R2 is not readable either; #1104's kappa step waits for the double-double and ladder-free roots of #1111.
   - Between: mixed; reported as such.

Posted on #1110, pushed here (the state and map copies, the root records, the logs), reported to the coordinator. The state-difference |z_chord - z_R2| by band is dh170's (`i1101_weakdir.py coords`, in its folder); this machine computes none.
