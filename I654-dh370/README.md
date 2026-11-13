# I654-dh370: the 0.975 last node on the exact projector, polish and a chain leg beside #603 (the dh370 run of #654)

Machine: dh370, Fedora Linux 45 Workstation, Intel Core i7-8700 (6 cores, 12 threads, AVX2 and FMA), 31 GB. Run at `nice -n 10`, 12 threads, `OPENBLAS_NUM_THREADS=1`, no memory guard.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/654 (moved from win2 to dh370 by the coordinator, 2026-11-13).
Code: choptuik-large-d main at 37c7955c (a descendant of 141d9d48), worktree `choptuik-large-d-654`, run in the venv of `choptuik-large-d-614` (the 3c35f0c build, multishoot 1.2.2, multidouble 4.2.1);
hp/src, hp/Cargo.* and hp/pyproject.toml are unchanged between 3c35f0c and 37c7955c, and so is hp/python.
Start state S: `I603-win2/chain/anm_pin3_D252.2497.npz` (sha256 f9ee739b78cbd097..., #603's newest converged state in the raw repository at fd59b5b2, step 40, D 252.2497), read in place.
#603's flags: `I603-win2/run_603.sh`.
