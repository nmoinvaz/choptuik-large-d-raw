# I901-rpi5: the second start-value implementation (fixed_point_M_b.py) reproduced on aarch64 Linux (Raspberry Pi 5)

Machine rpi5 (Raspberry Pi 5 Model B, 4 cores, 8 GB, Ubuntu), issue
https://github.com/nmoinvaz/choptuik-large-d/issues/901 (proof/A_lemmas_M.md 2.5; the Mac's runs are `I427-mac/`,
`I866-mac/`, `I869-mac/`, `I870-mac/`, `I877-mac/`, `I878-mac/`). Script (the coordinator's, md5 841c6350, unedited):
`run901.sh <python> <raw clone>`, run from `solver/proof/` of the worktree `~/Source/choptuik-large-d-901`
(wip/i901-rpi5 at origin/main 62f64c9a, never committed), one process at a time at nice 10. Each run's output is
`<name>.log`, each line of `exits.txt` has the run, its exit status, the status it must have (0 for checks, 3 for
mutations), its wall time and its command. Versions in `env.txt`.
