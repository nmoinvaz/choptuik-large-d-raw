# I1025-win2/kc95_d22: macm3's k_c 87 leg state at D 22.0 regridded to k_c 95, then a hybrid sign scan around lambda_1

Machine win2 (Windows 11, 20 logical CPUs, 95.5 GB RAM; runner win2, Sonnet 5.5). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-24 17:45 UTC, before any regrid or scan of this folder
(the drivers `kc95_regrid.sh` and `kc95_scan.sh` and the tools in `inputs/` are here; the dry runs are in `dry21875/`). The D 22.5 point is the same drivers in `../kc95_d225/`.

## Order (coordinator t5, hc, 24 Nov ~17:25 UTC), verbatim
"STOP THE FAR SCOUT NOW by exact pid ... (done at 17:27 UTC, see ../kc79_leap/README.md)
2. CANCEL THE QUEUED k_c 95 LEAP (same reason: an h 0.0625 path; at h 0.03125 a k_c 95 leg would take ~35 h to D 21.75). Instead, from tag g's end (19:20), k_c 95 REGRIDS at chosen D from macm3's k_c 87 leg states, which are at h 0.03125 from D 21.8125 on:
first D 22.0, then D 22.5, each as soon as macm3 pushes that state (raw I1025-macm3/kc87_leg2/b/, tag l1kc87Lmacm3b). Each: pin by blob, kc87_syscheck accepts it (controls 1 1); ell_refine.py <tag> 87 <new tag> 95 1 <D> <lambda_0 from its record>
--kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma, 4 threads BelowNormal, 6 h cap; kc95_syscheck_1025.py accepts the result (controls 1 1, kc87 check refuses); then d18_hybsign.py with 4 processes on lambda = (macm3's k_c 87 root at that D + 0.003)
rounded to 0.005, +-0.01 by 0.005, plus a repeat of the centre (prediction: k_c 87 root + 0.003, bar 0.005). Raw kc95_d22/ and kc95_d225/ in your folder, README first. dh610 does the same at D 21.75 now.
Two new Opus sessions of mine run on this machine since 17:21 (desktop-pc/t24 and t25, 6 threads each): leave their processes alone, as they leave yours."

## Inputs (pinned by `git hash-object --no-filters`; the drivers refuse any other blob)
| item | where | blob |
|---|---|---|
| macm3's k_c 87 state and record at D 22.0 | raw `I1025-macm3/kc87_leg2/b/` (`sol_l1kc87Lmacm3b_D22.000000.npy`, `l1kc87Lmacm3b.jsonl`), fetched by `fetch_macm3.py` through `gh api` and checked against the listing's blob; the blobs are recorded in `in/fetched.txt` | recorded at the fetch |
| k_c 87 check (dh610's; the source's acceptance); k_c 95 check (the result's acceptance) | `../kc95_leap/inputs/` | 6df5d960; d487e628 |
| `d18_hybsign.py` (xfkappa's, unmodified; its first line is the record-system check); `read_lower.py` (dh170's); `repeat_check.py`; `leg_read.py`; `d185_scan_read.py`; `d18c_read.py` | copies of `I1025-dh610/kc95_d2175/in/` in `inputs/` | e089207a; 89309d3c; aaf598a9; 5cae2639; 7c9d400f; 1383470f |
| `pair2025.py` (my repeat gate, from `../kc79_d2025/`); `centre.py` (the scan centre from macm3's `roots87.txt`) | `inputs/` | e692c61d; the file's own selftest |
Code for the regrid and the scan: worktree `D:/choptuik-i1025k79` at 48c36355 (`dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's; `ell_refine.py` 631e5801; `ell_delta.py` fde699f5), python 3.14 with multidouble 5.1.0 (`venv-md510`).

## Commands
1. `kc95_regrid.sh 22.0 l1kc95win2d22 kc95_d22` (one driver, own session through `cim_start.ps1`, BelowNormal): pins and selftests (the k_c 87 and k_c 95 checks `--selftest` 0; `fetch_macm3.py --selftest` 0 and `--mutate` 1); waits for macm3's D 22.0 state and record row;
   `kc87_syscheck_1025.py` accepts the source (controls `--mutate=F` and `--mutate=steps` exit 1 each); the state goes into the worktree's `data/` under the name `ell_refine.py` reads; waits for the tag g leap's end (all8.done, 19:19:49 UTC at its cap) and for any other regrid of mine;
   in `solver/matter`, 4 threads, cap 21600 s by the exact root pid, no retry:

       python -u ell_refine.py l1kc87Lmacm3b 87 l1kc95win2d22 95 1 22.0 <lambda_0 = ell_delta.lam0_at(22.0)> --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma

   Accepted only when `kc95_syscheck_1025.py` exits 0 on the result, `--mutate=F` and `--mutate=steps` exit 1 each, and `kc87_syscheck_1025.py` on the result exits 1 (refuses). `regrid_accepted.txt` or `regrid_refused.txt` says which.
2. `kc95_scan.sh 22.0 l1kc95win2d22 kc95_d22`: waits for `regrid_accepted.txt` and for macm3's k_c 87 root at D 22.0 in raw `I1025-macm3/kc87_leg_lambda/roots87.txt` (read with `gh api`); centre = (root + 0.003) rounded to 0.005 (`centre.py`; selftest 0, `--mutate` 1);
   the six evaluations centre-0.01, -0.005, centre, +0.005, +0.01 and the repeat of the centre on FOUR processes of one thread (P1 centre, centre+0.01 | P2 the repeat, centre-0.01 | P3 centre-0.005 | P4 centre+0.005), caps 28800 s by exact pids,
   after my other `d18_hybsign.py` scans have ended and 18.4 GB are free (a wait, not a stop; nothing is stopped for memory); then `read_lower.py` on the folder over centre +-0.01, `repeat_check.py`, `pair2025.py` (P1 and P2 first records, the same lambda), and
   `leg_read.py read` against the prediction root + 0.003 (bar 0.005).

## Acceptance (fixed before the run)
Source accepted with controls 1 1; the regrid exits 0 inside 21600 s; the result accepted by `kc95_syscheck_1025.py` with controls 1 1 and refused by the k_c 87 check; every scan process prints "the record system" (else it exits 3); the repeat of the centre agrees with the centre
(`pair2025.py` 1e-6); a robust sign change found by `read_lower.py` is reported by position as read (a bracket, with the estimator range named as a spread over estimator choices, not an enclosure). No robust change in the window: reported as read, no widening.
A pin that differs, a selftest or control that does not read as written, a source not accepted, a regrid not accepted or over the cap, or a scan process that fails stops the lane and I report it.

## Status
- 2026-11-24 17:45 UTC: folder, drivers, inputs and README written; dry runs of both drivers (`dry21875/`, on macm3's D 21.875 state) first, then the lane for D 22.0 waits for macm3's state and tag g's end.
