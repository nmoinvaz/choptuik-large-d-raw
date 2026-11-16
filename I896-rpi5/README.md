# I896-rpi5: the regenerated B8 outputs (b8_chain_regen.sh) reproduced on aarch64 Linux (Raspberry Pi 5)

Machine rpi5 (Raspberry Pi 5 Model B, 4 cores, 8 GB, Ubuntu), issue
https://github.com/nmoinvaz/choptuik-large-d/issues/896 (recommended by #890, raw `I890-mac/`). Code: worktree
`~/Source/choptuik-large-d-896` (wip/i896-rpi5 at origin/main aa05bf92, which holds 80601d56; never committed),
`solver/proof/b8_chain_regen.sh` unedited with the venv python, one process at nice 10 (the script's own).
`run896.sh` (mine) wraps it: it checks that `solver/proof` is clean, runs the script, copies the 35 outputs to `regen/`,
records `status_after.txt` and `diff_against_stored.txt`, and runs `b8m_lc_liprep.py --compare` (the stored matrix, kept
in `stored_b8m_lc_lip.json`, against this run's). `stored/` has the 35 files as stored at HEAD (`git show`).
Exits and wall times in `exits_896.txt`, the script's statuses in `regen.log`, versions in `env.txt`.

## Result

Started 2026-11-16 03:13 UTC, finished 03:52 UTC (`b8_chain_regen.sh` 2341 s = 39 min; the coordinator's estimate was
1 h, the Mac took 20 min). Every command of the script exits 0 (`regen.log`: `b8_chain_regen: every command exits 0`; 35
statuses, the script exits 0). `env.txt`: python-flint 0.9.0, FLINT 3.6.0, numpy 2.5.4, mpmath 1.3.0, scipy 1.18.1,
python 3.13.7, commit aa05bf92, `b8_chain_regen.sh` md5 0b0b81d4. The worktree was clean at the start; the script's
changes to it are in `status_after.txt` and `diff_against_stored.txt` (12 files differ in bytes, 24 lines).

### Acceptance

| criterion | verdict |
|---|---|
| theta = 0.7355 | yes: `b8m_lc_K4.out` and `b8m_lc_lipcheck.log` give Perron root 0.7051, certified theta = 0.7355 (< 1: True) |
| n0 = e^89.75, C7 = 2.8959e+29 | yes: `b7_ift.log`, `n >= n0 = e^89.75 (D = n + 2) ... C7 = 2.8959e+29 = e^67.838` |
| lemma J's theta = 0.17593 | yes: `b8m_lcj.log`, `theta = 1.7593e-01`, `theta0 = 5.8367e-05` |
| the six mutations are caught | yes, all six: `b7_ift_mutJD.log` (JD), `b8m_lc_numcheck_mut.log` (d0, weight, rho2L of the LC certificate), `b8m_lcj_mutations.log` (kernel, Om), each `must FAIL: caught` |
| each of the 35 files equals the stored one to its printed digits | 35 of 35 (`compare_stored.txt`, below) |
| lemma LC's matrix agrees to 1e-9 in every entry | yes: `liprep_compare.log`, 1600 entries, 0 differ by more than 1e-9, the largest difference 0.0e+00, theta = 0.7355 and 0.7355, `LIPREP: PASS` |

### The 35 files against the stored ones (`compare_stored.txt`, `compare_i890.py regen stored`)

`compare_i890.py` is the coordinator's comparator from `I890-mac/`: per file, the count of lines or records, the fields
or text that differ, and the largest relative difference of a number, with wall times dropped. 23 files are byte for
byte the stored ones. The other 12 differ in bytes, in these ways only:

| files | difference |
|---|---|
| `b8m_scan_K4_box.log`, `.out`, `b8m_scan_K4_d0.log`, `_d0_1e6.log`, `_d0_1e7.log`, `_fixedZ.log`, `_k0.85.log`, `b8m_lc_K4_mut_rho2L.log`, `.out` (9) | the `time` field of each record (wall times); every other number and field is equal (0.0e+00) |
| `b8m_lc_K4.log`, `b8m_lc_K4.out` | the time, and doubles in the Perron-root line (0.7051322167123087 against ...082, theta 0.7354677564068199 against ...197): 1.1e-14 relative at the worst, none at the printed digits |
| `b8m_lc_numcheck_n1e3.log` | line 2, the jump of the two continuations, `1.18e-20` against the stored `1.40e-20` (a roundoff-level quantity, 1.6e-1 relative); every verdict equal |

`b8m_lc_lip.json` (1600 entries) is equal in every entry: the 1204 entries at the floor 1e-50 are the floor in both, and
the 396 above it and `hprime` differ by 0.0e+00. The scan at L0 = 62 gives 67 iterations, as the stored record (the
regenerated stored files carry the current code's records).

The same `1.18e-20` was the Pi's value in #882 (`I882-rpi5/`, against the older stored `1.40e-20`), so it is
the aarch64 roundoff of this check and does not move between the two Pi runs.

### Files

`regen/` the 35 regenerated outputs, `stored/` the same 35 as stored at HEAD, `regen.log`, `exits_896.txt`, `env.txt`,
`status_after.txt`, `diff_against_stored.txt`, `liprep_compare.log`, `stored_b8m_lc_lip.json`, `compare_stored.txt`,
`compare_i890.py` (the coordinator's, from `I890-mac/`), `run896.sh` (mine, md5 ebd9dc56).
