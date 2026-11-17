# I930-dh610: #925's stall-rule leg control, `test_stall.py --cases 4 --mutate nostall` and its pair, on dh610

Machine dh610 (Fedora 45, i7-12700, 20 threads), issue https://github.com/nmoinvaz/choptuik-large-d/issues/930.
Code: worktree `choptuik-large-d-930` at origin/main 9cc648d2, run from `hp/`; hpkernel from #923's build (worktree
`choptuik-large-d-923` at d2be15c7, venv `choptuik-large-d-923/.venv`). Commands (`run930.sh`, 3 threads, nice 10, beside
the #842 and #903 chains): `python3 test_stall.py --cases 4 --mutate nostall` (must exit 1) then
`python3 test_stall.py --cases 4` (must exit 0); logs `nostall.log` and `plain.log`, exit codes in `exits_930.txt`.
