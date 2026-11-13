# I628-dh370: gamma(3.5) at M 96 (control) and M 128 on hp/lowD_gamma.py's path (dh370, Fedora Linux 45)

Machine: dh370, Fedora Linux 45 Workstation, Intel Core i7-8700 (6 cores, 12 threads, AVX2 and FMA), 31 GB.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/628 (macm3 runs M 160 beside, in I628-macm3/)
Code: choptuik-large-d main at b58895bd28e87d1760d5ca98ad39a24008badb84, worktree `choptuik-large-d-628`; the kernel is the
build of I604-dh370/ (hp/src, hp/python, the Cargo files and the pyprojects are unchanged since e835d94).
Runs (from the worktree's root, nice 10, 6 threads each, both at once, no memory guard):
`python3 -u hp/lowD_gamma.py OUT.jsonl hp/data/lowD_states/lowDvh_D3.5000_M{96,128}.npz --threads=6 --polish=2 --lam0=3.1018757202 --xtol=1e-11`
Pass: the M 96 rerun gives gamma = 0.32238557898599024 (lambda 3.1018757202022877) bit for bit; each run has one sign change and
records F after the polish; gamma(128) - gamma(96) reported.

## Files and results

| file | what |
|---|---|
| lowD_gamma_D3.5_M96.jsonl, .log | the M 96 control: gamma 0.32238557898570824, lambda 3.101875720205001, F after the polish 4.388038785291878e-30, 4 determinants, one sign change, 578 s, exit 0 |
| lowD_gamma_D3.5_M128.jsonl, .log | M 128: gamma 0.3223855827556097, lambda 3.101875683932393, F after the polish 3.373458890588682e-30, 6 determinants, one sign change, 1299 s, exit 0 |
| memory.log | one line a minute (available memory, swap used, summed RSS of the lowD_gamma processes), alert-only. It covers the two runs up to 02:31 UTC (minimum available 25568 MB, maximum summed RSS 1887 MB, no swap), and then the #614 build in I614-dh370/ until 06:53 UTC, where the available memory fell to 2601 MB: ignore the lines after 02:31 for this task. |

The stored M 96 record (hp/data/lowD_gamma*.jsonl) has gamma 0.32238557898599024, lambda 3.1018757202022877, 16 determinants, 3355 s, the same F. The
rerun is not bit for bit because the command (`--lam0 3.1018757202 --xtol=1e-11`) brackets the root to about 5e-12 in lambda, and the stored
run started from another guess (3.0921) and located the root more finely. Lambda differs by 2.7e-12, gamma by -2.8e-13. gamma(128) - gamma(96)
is 3.77e-9 (3.7699e-9 against the rerun, 3.7696e-9 against the stored value).
