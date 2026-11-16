# I845-mac: the sigma-model kernel's deflated Newton on the near-null band at D 10.475, eta = 1 (in progress)

Machine: mac (Apple M5 Mac). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/845. Code: branch `wip/sa-845`.
The kernel module is the build of #652 (`I652-mac/README.md`), with `/Users`-free paths in the copies here: python
3.14 of venv-314, `PYTHONPATH` at that build's site directory.

## Stage 2: the planted test (`planted/`)

`planted_band.py` and its four mutations, each run's output and record. The test passes, and each mutation exits 1.

## Stage 3: the kernel at D 10.475 (`out/`), in progress

`run_i845.sh` (with `gate.sh`, which waits for a 1-minute load below 31): one process, 2 threads, nice 10.

- `pilotB.txt`, `sm_pilotB_D10.475_M32.*`: the pilot, 3 + 3 iterations from start B (sigdss m1hi, Δ 0.9935). An
  iteration takes 125 s, of which the Jacobian and its SVD take 65 s. The spectrum has 32 singular values below 10⁻¹⁰ of
  the largest and the next at 10⁻⁴. The resolved rows converge in two steps (S 5.0×10⁻⁴, 1.0×10⁻⁸, 3.1×10⁻¹³), and four
  band steps of length 0.18 lower the band's residual from 1.02×10⁻¹⁰ to 8.1×10⁻¹¹ while Δ rises to 0.99978.
