# I1025-dh610/kc79_d195: k_c 79 at D 19.5 on dh370's regridded state: the control at D 19.125 first, then the hybrid sign scan at lambda_1 1.41 to 1.50

Machine dh610 (Fedora 45, i7-12700, 20 threads, 62 GB). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Task from the coordinator (hc, 22 Nov 2026), after `../kc71_d1925up/` (raw 93fce3d7), which ends k_c 71's roots: "half of the k_c 79 scan at D 19.5 (dh370 takes 1.30-1.40)".

## Order (the coordinator's)

1. **Control, 1 process:** `d18_hybsign.py` on dh370's k_c 79 D 19.125 state and record (raw `I1025-dh370/kc79_d19125/`, c58e5052; blobs pinned) at lambda 1.50. It must print the record system and dh370's hybrid sign and ln|det| at 1.50 (-2537.823195774449) to 1e-9 relative (dh170 matched it to 1.1e-15). Stop and report if not.
2. **Scan,** when dh370 pushes its accepted k_c 79 D 19.5 state and record (`I1025-dh370/kc79_d195/`; the coordinator forwards the commit): lambda 1.41 to 1.50 at 0.01 (10 values) plus a repeat of 1.45, 6 processes of 1 thread, nice 10, a systemd unit, `read_lower.py`. The k_c 79 line puts lambda_1 near 1.404 at D 19.5 (information, not a pass rule).
3. Report every robust change with det-linear estimate and range, the edge signs, any ln|det| minimum without a change; k_c 79 roots. Estimate: control about 15 min, scan 2 rounds of about 15 to 20 min. Post on #1025 and send the verdict with the raw commit.

The cross-machine record at k_c 79 (information): the control at D 19.0 of `../kc79_d19low/` differed from winb's Windows build by 1.914e-6 relative in ln|det| with this machine's own spread over 1, 2 and 4 threads at 2.9e-15 (raw c0d4213f); the bar here is 1e-9 against dh370's Linux build, which dh170's run matched to 1.1e-15.

## Setup

Budget: 1 process of 1 thread for the control (OMP, OPENBLAS, MKL, VECLIB, RAYON = 1), nice 10, a systemd user unit `i1025n` (`lane_kc79_d195_control.sh`, started by `start_kc79_d195_control.sh`, log `exits_kc79_d195.txt`); nothing else of mine runs. Worktree `~/Source/choptuik-large-d-1025f` clean at 505d8399 (its `dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` are the ones dh370's worktree 48c36355 matched, README of `I1025-dh370/kc79_d19125/`), interpreter `~/Source/venv-i1058/bin/python`.

Inputs (dh370's, raw `I1025-dh370/kc79_d19125/` at c58e5052, copied to `in/`; pinned by `git hash-object --no-filters`, `in_blobs.txt`; the lane refuses on any other blob): `sol_l1kc79dh370_D19.1250.npy` 3ff3fcb5, `l1kc79dh370.jsonl` 15ac964f (the D 19.125 line is used), `ref_dh370_scan_kc79_D19.125_1025.jsonl` 9a6ef239 (dh370's scan of that state; its lambda 1.50 rows, both -2537.823195774449, bit-identical), `d18_hybsign.py` e089207a (xfkappa's, unmodified). For the scan: `read_lower.py` 89309d3c, `d185_scan_read.py` 7c9d400f, `d18c_read.py` 1383470f, `repeat_check.py` aaf598a9 (dh170's, unedited).

## Commands

1. `d18_hybsign.py in/l1kc79dh370.jsonl in/sol_l1kc79dh370_D19.1250.npy 19.125 1.50 control/scan_D19.125_p0.jsonl`, cap 3 h by exact pid, 1 process of 1 thread, nice 10.
2. `control_check.py control/control.log control/scan_D19.125_p0.jsonl in/ref_dh370_scan_kc79_D19.125_1025.jsonl 1.50`: pass only if the log prints `the record system`, the hybrid sign equals dh370's (-1) and ln|det| equals dh370's -2537.823195774449 to 1e-9 relative. Its selftest (planted agreeing rows for a + and a - reference and a 5e-10 shift pass; a not-the-record-system log, both sign flips and a 1e-8 shift fail) must exit 0 and its `--mutate` (bar raised to 1e-6) must exit 1: `selftest_control_exits.txt`, wanted 0 1. The bar is not changed whatever the control reads.

## Acceptance (the coordinator's)

- the control prints the record system and matches dh370's sign and ln|det| to 1e-9 relative; otherwise stop and report, no scan. The scan has its own lane, written after the state arrives.

Written as the run goes.
