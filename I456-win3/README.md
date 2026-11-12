# I456-win3: D 55.04, M 64, kf 23 gamma solve taken to the floor

Machine: win3 (NATHAN-PC, Windows 11 Pro, i7-12700, 20 logical processors, 64 GB). Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/456 (reference lambda(64, kf 23) = 2.047684127603771 from #291).

Code: choptuik-large-d at main ce758f70 (gamma_dd.py with `--newton_it` and `--lm_it` from 98f7735), hpkernel built
from 80b50568's hp/src (no kernel change since), Python 3.14.10. Command, from the repository root:
`python hp/gamma_dd.py gamma_M64_kf23.jsonl hp/data/states/up10_D55.0351.npz --threads=1 --polish=4 --Mhi=64 --kf48=23
--newton_it=24 --lm_it=80`, output in `gamma_M64_kf23.log`, exit status in `gamma_M64_kf23.exit`.

## Result (D 55.035, M 64, kf 23, one thread, 08:53 to 09:04 UTC)

Exit 1 (the script's floor check, |est| <= 1e-15). lambda(64, kf 23) = 2.047684127603771, equal to #291's
2.047684127603771 (difference 0.0e+00). |F(64)| = 5.8e-24, est = -1.28e-15, floor ABOVE (#291: by a factor 1.3).
The solve stopped by its own floor rule after 1 Newton step and 2 Levenberg-Marquardt steps (largest Newton-step
component at the solution 2.8e-5), so the raised limits (--newton_it=24 --lm_it=80) were not reached. The M 32 lambda
is 2.0476841277123925. The M 64 solve took 575 s.
Files: `gamma_M64_kf23.jsonl` (the record), `.log`, `.exit` (the exit status), `.start` (start and end, UTC).
