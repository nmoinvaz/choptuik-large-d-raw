# anm-mac/jets_inputs: the jets bit-identity reference with its plans and inputs, made on the Mac

Machine: the Mac (Apple M5, NEON), the build of main at bfaa03d (venv-qds), hp/highm_check.py jets of main.

- `jets_inputs.json` (`save.log`): the 28 hashes, the three plans and the input hashes (M 32, 48, 64);
  `jets_inputs_inputs.npz` the inputs themselves (M 32 is the M 48 state resampled to 32 by numpy on the Mac).
- `compare.log`: the same build against it, on the stored plans and inputs: 28 of 28 bit-identical.
