# I954-dh610: speed round 1, hp-level bit checks of #953, multidouble #72 and #952's split on dh610

Machine dh610 (Fedora 45, i7-12700, 20 threads, AVX2), issue https://github.com/nmoinvaz/choptuik-large-d/issues/954.
Two hp builds, each in its own fresh worktree and venv, built at nice 10 with `CARGO_BUILD_JOBS=8`, checks at 8 threads (the
#842 chain keeps its 9 and its worktree and venv are not touched):
- **A**, `choptuik-large-d-954a`: origin/main at 4c3bb0ef (multidouble 4.8.2, #952's opt-in split series, `octo_hashes.py`);
- **B**, `choptuik-large-d-954b`: branch `perf/dup-eval` at 7583e787 (PR #953) with `hp/Cargo.toml` patched to multidouble's
  `perf/od-dd-const-products` branch (PR #72).
Inputs (extracted from the raw repository's origin/main into `~/scratch954/raw`, which is R for the checks): ST =
`I903-win2/ks_chain/leg07_D222.0000_ks240/anm_pin3_D229.0509.npz`, ST2 = `I608-dh610/restart4_d6/anm_pin3_D253.3382.npz`, the
prediction `.../pred_pin3_D229.5165.npz`, `T81/ref_main.json`, `T81/scaled_main.json`, `anm-mac/jets_inputs/jets_inputs.json`.
Scripts, in order: `build954.sh` (both builds), `checksA.sh`, `checksB.sh`; each check writes `<name>.log` (its first lines are
`hpkernel.__file__` and the .so's multidouble strings; the last is `exit N`) and a line in `summary_A.txt` or `summary_B.txt`.

## Note, 2026-11-18: jet_by_order_check.py from main 9bff3a1e

The hook line of the first run on A failed at order 6 because the old check compared the payload bits of inf and NaN words (#954, comments 6970974909 and 6971226549). Main's script `jet_by_order_check_main.py` (origin/main 9bff3a1e: finite words bit for bit, non-finite ones by place) is used for the reruns on A (`jboA_main954.sh`, `A_jbo_main.log`). In the worktrees of B and C the file `hp/jet_by_order_check.py` was replaced before their line ran: B's by main's file (byte for byte), C's by its own file with main's `same_words` and `differ` (C keeps its `--save`, `--compare` and two extra controls). No kernel code changed, so no rebuild. The `A_jet_by_order` line of `summary_A.txt` (old script) is the failed first run.

## Note, 2026-11-18: decisions of the coordinator (hc)

No C2 build: checksC stays on build C (6d7b2927, PR #955's head at that time); dh370 builds the merged head (main, #956 and the rebased #955) and runs both PRs' lines there. B's `checkq` mismatch at PRED is the check's, since A fails identically (`A_checkq.log`, `checksG.sh`). B's planted-at-ST verdict waits for A's planted at ST in checksD.

## Closing, 2026-11-18 18:00 UTC

All scripts ended: checksA 06:26, checksB 10:50, checksC 12:47 (its timing lines failed on my path error and were rerun by `checksH.sh`, 12:48 to 13:30), checksD 17:07, checksE 17:12, checksF 17:56. `checksG.sh` is A's `checkq`. The closing comment on #954 has the table of every check.
