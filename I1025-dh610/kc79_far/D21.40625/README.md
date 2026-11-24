# I1025-dh610/kc79_far/D21.40625: win2's tag g leap state and tag i far scout state at D 21.40625, side by side (no lambda_1 scan)

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (the orders, win2's plan, the lane, the predictions for the four comparisons). Written 2026-11-24 12:03 UTC, before either state of this D may be on origin and before any run of this folder. The k_c 79 states are not yet physical.

## Order (coordinator t5, hc, 24 Nov)
"Far-scout points at D the tag g leap also reaches (21.28125, 21.34375, 21.40625, 21.46875; tag g ends at 21.5): no lambda_1 scan; record instead the two states' Delta, |F|, steps and constraint side by side (two continuation paths to one D and k_c: the state reproducibility)."

## What is done here
- `wait_compare.sh 21.40625` (unit `i1025-cmp-21_40625`): waits for the tag g state (`sol_l1kc79Lw1025g_D21.406250.npy`, h 0.03125) and the tag i state (`sol_l1kc79Lw1025i_D21.406250.npy`, h 0.0625) of `I1025-win2/`, pins each with its record by blob (`g/in_blobs.txt`, `i/in_blobs.txt`, `g/source_commit.txt`, `i/source_commit.txt`), pushes the pins, then `lane_compare.sh 21.40625`: selftests (`kc79_syscheck_1025.py --selftest`, `compare_states.py selftest` exit 0 and its `--mutate` exit 1), the source check on each state (exit 0; `--mutate=F` and `--mutate=steps` exit 1), `compare_states.py` into `compare.txt`.
- No scan, no widening. `compare.txt`: Delta, |F|, steps, psi-constraint side by side with the difference and ratio i over g, then h and seconds, and, as an extra the order does not ask for, the L2 distance of the two state vectors.

## Acceptance (fixed before the run)
Both states accepted by the source check with both controls exit 1 (a refusal stops the lane and I report it, I do not loosen it); the selftests as wanted; the pins equal the commits' blobs. Reported: the four ordered quantities side by side as printed, by position, with the predictions of the parent README scored here.

## Predictions
The parent README's, for each D (registered before any of the four): sources accepted 90%; steps equal 55%, within 2 85%; |F| ratio within 1 +- 0.01 70%, within 0.05 90%; Delta within 1e-6 55%, within 1e-4 85%; constraints within 0.1% 60%; state distance below 1e-6 45%, below 1e-4 80%.

## Status
- 2026-11-24 12:03 UTC: folder and README written.
