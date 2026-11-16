# I906-rpi5: two checks of Delta_inf (Bulirsch-Stoer and Akaike-averaged fits) on the Raspberry Pi 5

Machine rpi5 (Raspberry Pi 5 Model B, aarch64 Linux, 4 cores, 8 GB), issue
https://github.com/nmoinvaz/choptuik-large-d/issues/906 (`hp/dinf_check.py`, the six plants of `hp/planted_dinf.py`, then
the real double-double points). Script `run906.sh` (the coordinator's, md5 7ae710395fc4dddaf1bd0fe078f6ece2, unedited):
`bash run906.sh <venv python> <worktree> <raw clone root>`, run from the raw clone's root with the worktree
`~/Source/choptuik-large-d-906` (wip/i906-rpi5 at origin/main 49bfccec, never committed). It runs four commands of
`dinf_check.py` one after another at nice 10: `bst`, `bst --mutate omega2`, `aic`, `aic --mutate noweight`, with the
required exit status 0, 1, 0, 1. Each command's output is `<name>.log`, `exits_906.txt` has its start, its exit status
against the required one and its wall time, `env.txt` the commit and the versions.
