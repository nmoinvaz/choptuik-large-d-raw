# I912-rpi5: lemma S's series control over a box after the #865 fix, on aarch64 Linux (Raspberry Pi 5)

Machine rpi5 (Raspberry Pi 5 Model B, aarch64 Linux, 4 cores, 8 GB), issue
https://github.com/nmoinvaz/choptuik-large-d/issues/912 (depends on #865; the Mac's outputs are `I865-mac/`, raw
f9f5f629). Script `run912.sh` (the coordinator's, md5 df8f3da4dcefb54a317c243d36c111ac, unedited):
`bash run912.sh <venv python> <raw clone root> <worktree> rpi5`, from `solver/proof/` of the worktree
`~/Source/choptuik-large-d-912` (wip/i912-rpi5 at origin/main 40cbc871, never committed). It runs lemma S's certificate
runs over the box (`s3`, `s5` over 1e-6, `s1` over 1e-9), the series mutation over boxes (`m3box`, `m5box`, `m5box9`,
`m1box`) and the control `m3box_prefix` (the M = 3 box mutation through the code before the fix, commit 34b00905, which
must exit 3). Each line of `exits.txt` has the run, its exit status, the status it must have and its wall time, followed
by the byte comparison of `s3.json` and `s5.json` with the Mac's. Versions in `env.txt`.

Run 2026-11-16 07:12 UTC, `done` within 30 s (the runs took 1 to 5 s each, 22 s in all). python-flint 0.9.0, FLINT 3.6.0,
python 3.13.7, aarch64 glibc 2.42 (`env.txt`), worktree commit 40cbc871, never committed (`git status` clean; the
script's temporary `lemma6_sector_M_prefix.py` is removed).

## Result

The fixed series control fires on aarch64: all seven runs and mutations exit 0, the three box mutations of lemma S print
`lemma S holds: False (must be False)` and the M = 1 one `lemma S passes: False (must be False)`, and the control, the
code before the fix (34b00905), exits 3 with `holds: True (must be False)`. Every log equals the Mac's in every character
(the Mac's `exit N` line aside). `s3.json` and `s5.json` are not byte-identical to the Mac's: the keys and all 55 and 73
leaves are the same, and the differing leaves are the f64 weights (relative differences up to 4.15e-14 for M = 3 and
5.62e-13 for M = 5) and, for M = 5, four ball radii (ratio 0.989 to 0.994, all overlap).

| acceptance (#912) | verdict |
|---|---|
| every run has its required exit status | yes: `s3`, `s5`, `s1`, `m3box`, `m5box`, `m5box9`, `m1box` exit 0, the control `m3box_prefix` exits 3 (`exits.txt`) |
| each mutation log reports "holds: False" (M = 1 "passes: False") | yes: `m3box`, `m5box`, `m5box9` `lemma S holds: False (must be False)`, `m1box` `lemma S passes: False (must be False)` |
| the control (code before the fix) does not catch the box mutation | yes: `m3box_prefix` prints `lemma S holds: True (must be False)` and exits 3, as the Mac's `box.log` |
| `s3.json` and `s5.json` equal the Mac's byte for byte, or the differing fields are reported | **not byte-identical, fields reported below**; the logs `s3.log`, `s5.log`, `s1.log`, `m3box.log`, `m5box.log`, `m5box9.log` and the control against the Mac's `box.log` are identical |

### The differing fields of `s3.json` and `s5.json` (`cmp912.py`, output `compare_mac.txt`)

| file | leaves | equal | differing f64 leaves | differing ball strings |
|---|---|---|---|---|
| `s3.json` | 55 | 16 | 39 (`wts_S`, `wts_R_plain`, `wts_R_diag`), largest relative difference 4.15e-14 at `wts_R_plain[4]` | 0 |
| `s5.json` | 73 | 12 | 57 (`wts_S`, `wts_R_plain`, `wts_R_diag`), largest relative difference 5.62e-13 at `wts_R_plain[12]` | 4, all overlap: `lip_S` radius 1.62e-11 against 1.63e-11, `F_S` 5.27e+24 against 5.33e+24, `Lambda_plain` 6.84e-12 against 6.90e-12, `Lambda_diag` 1.01e-11 against 1.02e-11 |

The midpoints of the balls and all other fields (the integers, the contraction constants, the verdicts) are equal. The
weights are the f64 weights the issue says may differ in the last digits by machine; the radii move with them
(AGENTS.md, #111: a bound assembled from upper bounds moves with every radius).

### Discrepancies

None of a result. The only difference from the Mac's files is the last digits above.

### Recommended tasks

None.
