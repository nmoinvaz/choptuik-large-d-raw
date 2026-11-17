# I936-dh170: the chain's own build (multidouble 4.7.0) against 4.8.2, octo-double bits on the order-150 state

Machine dh170 (Fedora 45, i7-7700, 4 cores / 8 threads, AVX2, 31 GB). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/936,
after #935 (I935-dh170/) and #934's scripts (I934-dh610/).

## Setup

| | old build (the chain's own) | new build |
|---|---|---|
| code | main checkout ~/Source/choptuik-large-d at 7f88c5bb (the same commit as the chain's worktree -903) | ~/Source/choptuik-large-d-935 at cdb5a6bc (origin/hp/multidouble-4.8.2) |
| venv | its .venv, hpkernel from main 5897ee28, multidouble 4.7.0 / multishoot 3.1.0 / multisolver 0.1.1 | its .venv, multidouble 4.8.2 / multishoot 3.2.0 / multisolver 0.1.1 |

State: I903-dh170/chain_k150/anm_pin3_D230.0000.npz (order 150, D 230, eight parts, stored plan), read from a worktree of the raw
repository's origin/main (the committed bytes, equal to the live file by cmp). state_dump.py is I934-dh610/state_dump.py with
STATES replaced by this state and the thread count read from STATE_DUMP_THREADS (diff in this folder's history: two changed lines).
octo_corrector.py and reseed.py are identical in the two code bases (git diff 7f88c5bb cdb5a6bc is empty for them), so the
Python that builds the system is the same and the kernel is the running venv's.

## Pass criteria, fixed before the first run

- Compare (state_dump.py --compare OLD NEW CTL) exits 0: every part of every entry of residual_o and of newton_o (dz0-dz7, a1, a2,
  f3, f4) has the same bits in OLD and NEW, and CTL's step (new build, tangents reversed, mutate=25) differs from OLD's in at least
  one entry.
- A differing entry is reported with its count and is not explained away; it marks a place where the chain's build hit the
  renormalization bug (multidouble 3.0.0-4.8.0) or another change between 4.7.0 and 4.8.2.

Run: `bash states936.sh` (old and new at the same time, 4 threads each, then the control at 8 threads; nice 10).

## Result (13:09 to 13:13 UTC, 2026-11-17)

| acceptance | verdict | number |
|---|---|---|
| `residual_o` bits, old (4.7.0) against new (4.8.2) | equal | 0 of 6152 entries differ (F0-F7, 769 each) |
| `newton_o` bits, old against new | equal | 0 of 7692 entries differ (dz0-dz7, a1, a2, f3, f4) |
| control (new build, tangents reversed, `mutate=25`) differs from old | fires | 6092 entries of dz0-dz7 differ (769 in each of parts 0-5, 765 in part 6, 713 in part 7) |
| compare exit code | pass | exit 0, `PASS: residuals and steps are the same bits; control fired` |

The old and new dumps are also byte-identical files (`cmp states_old_k150_D230.npz states_new_k150_D230.npz`).

The compared entries are populated, so equal bits is not equal zeros: 13,844 entries over both dumps' common keys, 9,664 nonzero. max|F| is 8.5e-04
in part 0 and falls by about 16 orders per part, 3.9e-118 in part 7 (parts 2-7 of F have 263, 128, 32, 32, 32, 32 nonzero entries, the
step's parts 0-5 are nonzero throughout). The octo-double parts down to part 7 are therefore all exercised.

Timing: the old and new dumps each took 2 min 36 s at 4 threads (run at the same time), the control 1 min at 8 threads.

## What this does and does not show

- It shows that at this state, one `residual_o` and one `newton_o` (stored plan, two tangents) are bit-for-bit the same under the
  chain's own build and under multidouble 4.8.2. At this evaluation the old build did not hit the octo-double renormalization bug.
- It is one state, D 230 of the 34 stored ones (D 201 to 233.125), and one evaluation each. The bug depends on the data, so it says nothing
  about the chain's other states, its series (jets, `series_o`) or the corrector's trial steps.
- The old side is the main checkout at 7f88c5bb with its .venv (hpkernel from main 5897ee28, multidouble 4.7.0 / multishoot 3.1.0), which
  is the producing build of the chain: the chain's worktree ~/Source/choptuik-large-d-903 is at the same commit 7f88c5bb. Only the
  kernel differs between the two sides, because octo_corrector.py and reseed.py are identical in the two code bases.
- Shared between the two sides: the state file, state_dump.py, the Python that builds the system, the thread count (4) and the machine.
  Not shared: the compiled kernel and the installed hpkernel driver.

## Files

states936.sh (the run), state_dump.py (I934-dh610's, two lines changed), states.log, dump_old.log, dump_new.log, dump_ctl.log, and the
dumps states_old_k150_D230.npz, states_new_k150_D230.npz, states_ctl_k150_D230.npz.
