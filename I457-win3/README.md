# I457-win3: D 58 gamma solves at kf 13, 15 and 17 taken to the floor

Machine: win3 (NATHAN-PC, Windows 11 Pro, i7-12700, 20 logical processors, 64 GB). Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/457 (#273 found lambda(48, kf 15) - lambda(48, kf 13) = -4.9e-13).

Code: choptuik-large-d at main ce758f70 (gamma_dd.py with `--newton_it` and `--lm_it` from 98f7735), hpkernel built
from 80b50568's hp/src (no kernel change since), Python 3.14.10. Three runs, each from the repository root:
`python hp/gamma_dd.py gamma_D58_kfK.jsonl hp/data/states/up12_D58.0060.npz --threads=1 --polish=4 --M48 --kf48=K
--newton_it=24 --lm_it=80` for K = 13, 15, 17, output in `gamma_D58_kfK.log`, exit status in `gamma_D58_kfK.exit`.

## Results (D 58.006, M 48, one thread each, 08:53 to 09:01 UTC)

| kf | exit | lambda(48) | est | floor | newton / lm | wall |
|---|---|---|---|---|---|---|
| 13 | 0 | 2.0455297614777623 | +2.04e-18 | ok | 10 / 0 | 6 min |
| 15 | 1 | 2.0455297614787296 | -2.32e-15 | ABOVE | 24 (stalled at 1.67e-19) / 2 | 8 min |
| 17 | 1 | 2.045529761477736 | -2.44e-15 | ABOVE | 1 / 2 | 5 min |

lambda(15) - lambda(13) = +9.67e-13, lambda(17) - lambda(13) = -2.62e-14, lambda(17) - lambda(15) = -9.93e-13.
Exit 1 is the floor check (|est| <= 1e-15), as the script defines it. The kf 13 lambda equals #273's (macm3,
I273-macm3) to every digit; #273's kf 15 lambda was 2.045529761477269 with est -2.36e-15.
Files: `gamma_D58_kfK.jsonl` (the record), `.log`, `.exit` (the exit status), `.start` (start and end, UTC).

## kf 15 with the default limits (12 Newton, 20 LM), 09:05 to 09:10 UTC

`gamma_D58_kf15_default.*`: the kf 15 command without `--newton_it`/`--lm_it`, same code and state. Exit 1 (floor
check). lambda(48) = 2.045529761477269, est = -2.360e-15, ABOVE, |F| 2.3e-23, 12 Newton and 1 LM steps.

| run | lambda(48, kf 15) | est | minus kf 13 |
|---|---|---|---|
| win3, 12 / 20 (default) | 2.045529761477269 | -2.360e-15 | -4.934e-13 |
| win3, 24 / 80 | 2.0455297614787296 | -2.320e-15 | +9.673e-13 |
| macm3, #273 (default) | 2.045529761477269 | -2.36e-15 | -4.93e-13 |

The default run equals macm3's lambda to every digit; the two win3 runs differ by 1.461e-12.
