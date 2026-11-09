# I252-mac: D 55.04 and D 61.03 at M 64, kf 23: determinant checks, counts, and circles at the M 40 and M 48 zeros

Machine: mac (Apple M5, 10 cores, shared). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/252

Code: worktree branch `wip/i252` of the main repository: main 590d88a with #242's rule cherry-picked
(`hp/modecount_wind.py` and `hp/modecount_planted.py` of `wip/i242` 01f6c59 and bc9fd22). Python
/Users/nathan/venv-314/bin/python (hpkernel and modecount_cx as installed, not rebuilt). At most 2 single-thread
processes, `nice -n 10`, `caffeinate -i`.

## Inputs

- `states/modecount_state_D61.0264_M64_kf23.npz`: #141's D 61 M 64 kf 23 state (nodes 0.3 ... 0.7, ks 191, |F| 8.5e-21;
  raw `I141-mac/states/`, 76fbf9b).
- `states/modecount_state_D61.0264_M64_kf23_outer085.npz`: #141's state with the node at 0.85, whose det M failed (the
  control of the determinant check).
- `states/modecount_state_D55.0351_M48_kf23_from_I232.npz`: the D 55 M 48 kf 23 state of #232 (raw
  `I232-macm3/D55/hp_data_after/`, identical to #241's), the start of the D 55 M 64 setup.
- lambda_phys = 2.043532530673195 (D 61.03) and 2.04768412771239 (D 55.04), as the M 40 and M 48 counts.

## Criteria (written before the runs)

1. **D 55 setup.** `hp/modecount_probe.py <D55 M48 state> --M=64 --kf=23 --setup --fmax=1e-15` (resample, fit_nodes,
   Newton then Levenberg-Marquardt). Its gates must pass (both series truncations <= 1e-15, |F| <= 1e-15), or D 55
   stops there.
2. **Determinant checks** (`scripts/det_check.py`, before each count): det M changes sign between lambda_phys - 0.015
   and lambda_phys + 0.015 in both LUs (hpkernel's real one and modecount_cx's complex one), the two LUs agree in
   ln|det M| to 1e-4 at both points, and their signs agree. The pivot range is recorded. Control: the same check on the
   outer-node state must fail (#141 found the LUs 2.2 apart and no sign change there). If the control passes, the check
   is not used. If a state fails, its count does not run.
3. **Counts.** `hp/modecount_wind.py <M64 state> --kf=23 --h0=0.6 --lam=<lambda_phys> --aLL=-0.096 --aL=0.124
   --fmax=1e-15 --resolve=last` (the fixed left column of #241; a1, a2 and aR chosen by the count as at M 48), with
   #242's alias rule (default pi/2). Reported per box: wind(g), resolved, both mismatch counts (any pass, last pass),
   largest step. An unresolved box is not a count.
4. **Circles** on the M 64 states (`hp/modecount_circle.py`, n0 20, tol pi/4). Each is read only if every step is
   below pi/4 with 0 verification mismatches. A lambda_phys circle (R 0.2) at each D must wind +1 with its zero within
   1e-5 of lambda_phys, or that D's circles are not read.
   - D 61 at the M 48 zeros (#230, kf 23): 1.3065 + 1.4158i, 2.0073 + 0.9727i, 2.5584 + 0.5825i, 3.0196 + 0.0958i.
   - D 55 at the M 48 zeros (#238): 0.1996 + 0.2548i, 0.3189 + 3.3314i, 0.0612 + 3.8526i, and -0.2267 + 4.2800i
     (outside the boxes).
   - D 55 at the M 40 zeros (#231): 0.4773 + 1.4533i (circle), and the moment positions 0.2427 + 0.9252i,
     0.0992 + 4.4804i, 0.3486 + 2.6122i, 0.3603 + 2.1609i, 0.5953 + 5.0393i.
   Reading per position: winding 0 means no zero within R of it at M 64 (absent). A winding >= 1 means a zero within R
   (present), and its M 64 position from the circle is compared with the lower-M one.
5. **Keeps its lambda.** A zero keeps its lambda if its M 64 position lies within 0.01 of its M 48 (or M 40) position,
   a tenth of the smallest shift seen between kf 21 and kf 23 at M 48 (0.054, #230), and present at every M where it
   was looked for. Otherwise it moved, multiplied or vanished.
6. **M 64 extras.** The zeros the count finds are located with `hp/modecount_moment.py` (no new determinants), and
   each located zero with spread below 0.05 is confirmed by a circle (R 0.2, n0 20) as time allows.

modecount_cx: the build of the main checkout (`hp/modecount_cx/build/modecount_cx.cpython-314-darwin.so`, 2026-11-08 16:26,
sha256 3e485ab9a27d6da50135b3fa94d758c922cd080f02d4a07a97e42b0de6136073, the same file #242 uses), copied into the
worktree's build folder, not rebuilt. The first launch (15:22 UTC) imported the crate's source folder instead and every
step exited 1 at once; its logs are in `failed_import/`.

## Redirect (coordinator, 2026-11-09 15:55 UTC)

After #250 both slots run circles: D 61 in one (`scripts/run_circles_D61.sh`), D 55 in the other
(`scripts/run_circles_D55.sh`), each with its lambda_phys control. Both full M 64 counts (`scripts/run_count_D61.sh`, and
the D 55 count of criterion 3) are held until the circles are in; the coordinator decides where they run.
