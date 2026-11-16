# I882-rpi5: Theorem B(1)'s certified constants (B8, B5, B_chain) reproduced on aarch64 Linux (Raspberry Pi 5)

Machine rpi5 (Raspberry Pi 5 Model B, 4 cores, 8 GB, Ubuntu), issue
https://github.com/nmoinvaz/choptuik-large-d/issues/882. Script (the coordinator's): `run882.sh`, every command of
proof/B8_constants.md 13, proof/B5_inner.md 10 and proof/B_chain.md 11 as written, from `solver/proof/` of the worktree
`~/Source/choptuik-large-d-882` (wip/i882-rpi5 at origin/main 4f2595c7, never committed), one process at a time at nice 10.
Exits and wall times in `exits_882.txt`; versions in `env.txt`; each command's stdout and stderr in `<name>.log`.

The commands overwrite the worktree's stored files, and the scan commands append to their `--log` file, so the script ends
by recording `status_after.txt` and `diff_against_stored.txt` and copying every changed or new file of `solver/proof/` to
`changed/`.
