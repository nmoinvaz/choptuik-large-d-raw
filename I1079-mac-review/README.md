# I1079-mac-review: the independent review's reruns for #1079 (excited M = 3 zeros): box runs with planted last-bit perturbations, default-option checks, the Lean regeneration

Machine: mac (Apple arm64, macOS 27.0.1; numpy 2.5.4 on Accelerate). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1079.
Written 2026-11-23 22:05 UTC, before any run of this folder. The review note is `notes/EXCITED_REVIEW_1079.md` on branch
`review/excited-1079` of the main repository; the scripts are in `solver/proof/review_1079/` there.

Code: branch `review/excited-1079` (on top of `feat/certify-excited` c40fbc77). Python
`/Users/nathan/Source/choptuik-large-d/.venv/bin/python` (3.13.15, python-flint 0.9.0, FLINT 3.6.0). At most 2 processes,
`nice -n 10`, one BLAS thread each.

## Runs planned (written first)

Check 5, the macOS/Linux margin gap. The stated cause: last-digit float64 differences in the start data, amplified on the
real leg. Test: box runs of x2 (h 1e-12, w 1e-12) and x1 (h 1e-12, w 1e-13) at `CERTIFY_M_NTAY=28 CERTIFY_M_NJAC=16`, from
macm3's refine files, through `review_1079/perturb_box.py`:

| run | perturbation | prediction, before the run |
|---|---|---|
| none | none | reproduces macm3's box file (same platform family): margins equal to the digits printed |
| perron | the start lemma's Perron weights by 1 ulp (start-data radii move in the last digits) | if the stated cause is right, margins move by tens of percent |
| qr | the Lohner frames Q of every step by 1 ulp | margins move by tens of percent if the gap is frame noise |

Each margin is from `certify_M.py krawczyk --box=<this run> --point=<macm3's point file>`. A run whose margins do not
move says that perturbation is not the cause. Pass or fail of the Krawczyk test is recorded for every run.

## Added after the first four runs (2026-11-23 22:12 UTC)

- The first prediction failed: the unchanged code on this Mac does not reproduce macm3's margins. So `none` was repeated
  (determinism on one machine), `perron` was repeated at 4096 ulp, and `qr` was given more seeds (1 to 5) at both zeros,
  to see the range of margins and whether any draw fails the test.
- `light_checks.sh`: the short reruns (dh610's and macm3's files through this machine; H1; lemma 6a from macm3's stored
  enclosure with the `coords` mutation; the inclusion; the covering's check, a dropped tile, `c1check` and its `nov`
  mutation; row 11 again). Records in `light_steps.txt`, logs in `logs/`.
- `c1_control.sh`: a C^1 ray run at h = 1e-9 at each centre, for `c1check` and its mutation at a box where the mutation
  can fire (a control only; the covering of record is macm3's, at h = 1e-11).
- `lean/`: the build log of `feat/lean-excited` with `review_1079/Exc1079.lean`, and the must-fail file's log.
- One run with `REVIEW_TIES=1` counts near ties in the pivot order of `validated_int.qr_pivot`.

## Added after the frame-perturbed runs of the second zero failed (22:39 to 23:02 UTC)

- `qrin`: the input of the QR moved by 1 ulp in place of its output (seeds 1, 2, 3, second zero), a change closer to
  what two machines differ by.
- `REVIEW_NJAC=28`: the failing seed-4 run at a higher order of the step Jacobian. Prediction: if the Jacobian's
  remainder were the lever, the margins improve. They did not. The same for seed 1 was stopped by the reviewer at
  22:51 UTC to free its slot (the `start` line in `steps.txt` has no end; no file was written).
- `REVIEW_STABLE=1`: a trial pivot order that does not depend on last bits (weights rounded to 6 digits, ties by column
  index), on the unperturbed run and on the failing runs (frames seeds 1 and 4) and one passing run (QR input seed 1).
  Prediction: if ties in the pivot order were the mechanism, the failing runs pass or at least move. They did not move.

## Files

- `steps.txt`: one line per box run and per Krawczyk test (start, exit, the margins line).
- `out/A_M_box_<tag>_<perturbation>_s<seed>[_u<ulps>].json`: the box runs. `logs/A_M_box_*`, `logs/A_M_krawczyk_pt_*`.
- `light_steps.txt`, `logs/XL*`, `logs/H1_*`, `logs/H3_*`, `logs/INCL_*`, `logs/H2_*`, `logs/PATHMIX_*`, `logs/C1CTRL_*`.
- `out/row_11_exc{1,2}.json`: row 11 rerun from macm3's stored ray state. `out/lemma6b1_check_M3_exc{1,2}.json`.
- `out/lemma6b1_runs_M3_c1ctrl_exc{1,2}/`: the C^1 ray runs at h = 1e-9 of `c1_control.sh` (controls only).
- Tags: `_none`, `_qr`, `_qrin`, `_perron` the perturbation, `_s<seed>`, `_u<ulps>` its size if not 1, `_nj<n>` another
  `CERTIFY_M_NJAC`, `_ties` the tie counter, `_stable` the trial pivot order.
- `logs/theorem_A_sets_M3_default_{main,branch}.log`: the one printed line that differs with the options unset.

## Results

In `notes/EXCITED_REVIEW_1079.md` (branch `review/excited-1079`), sections 1 to 5. The margins table of its section 5 is
written by `review_1079/perturb_table.py` from the logs here.
