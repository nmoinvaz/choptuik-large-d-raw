# I628-dh370: gamma(3.5) at M 96 (control) and M 128 on hp/lowD_gamma.py's path (dh370, Fedora Linux 45)

Machine: dh370, Fedora Linux 45 Workstation, Intel Core i7-8700 (6 cores, 12 threads, AVX2 and FMA), 31 GB.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/628 (macm3 runs M 160 beside, in I628-macm3/)
Code: choptuik-large-d main at b58895bd28e87d1760d5ca98ad39a24008badb84, worktree `choptuik-large-d-628`; the kernel is the
build of I604-dh370/ (hp/src, hp/python, the Cargo files and the pyprojects are unchanged since e835d94).
Runs (from the worktree's root, nice 10, 6 threads each, both at once, no memory guard):
`python3 -u hp/lowD_gamma.py OUT.jsonl hp/data/lowD_states/lowDvh_D3.5000_M{96,128}.npz --threads=6 --polish=2 --lam0=3.1018757202 --xtol=1e-11`
Pass: the M 96 rerun gives gamma = 0.32238557898599024 (lambda 3.1018757202022877) bit for bit; each run has one sign change and
records F after the polish; gamma(128) - gamma(96) reported.
