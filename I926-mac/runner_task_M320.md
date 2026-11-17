# #926's M 320 / 384 test at D 3.04315 (a runner task for win2; not run by I926-mac)

Code: branch `wip/sa-926` of choptuik-large-d (Python only: `hp/lowD_highM.py`, `hp/sonic_valley.py`; no rebuild, the
installed hpkernel of #343 serves). A worktree at that branch, commands from its `hp/`. RAW is the raw-data clone, R
the new folder `I926-win2` (README first line `# I926-win2: ...`). 10 threads, as #343.

**Setup.** The leg's state at #343's stop, before the hand edit of its targets: `I343-win2/leg2.jsonl.progress.json.bak`
(history of three states per M: 3.04375 from T105-win2, 3.04355 and 3.04335 from I343-win2; targets from 3.04315).

```
mkdir -p $R/states
cp $RAW/I343-win2/leg2.jsonl.progress.json.bak $R/leg.jsonl.progress.json
python -c "import json,sys; p=sys.argv[1]; s=json.load(open(p)); s.update(targets=[3.04315], t_used=0.0, post=None, done=None, point_start=None, last_point_s=None, last_point_wall=None); json.dump(s, open(p,'w'), indent=1)" $R/leg.jsonl.progress.json
```

Check before the run: the file's `hist_w` and `hist_n` end at D 3.04335 and their paths exist on the machine (they are
win2's absolute paths; edit them if the clone moved).

**0. The planted check of the gate (about 20 min at normal load; stopped on the loaded Mac, I926-mac README 3).**

```
python -u sonic_valley.py planplant $R/planplant.jsonl $RAW/I343-win2/states/lowD343_D3.043350_M320.npz \
    $RAW/T82-win/states/lowDhm_x0.000157-0.975_D3.0475_M320.npz --refine 4 --levels 2 --delta 1e-8 --threads 10 \
    > $R/planplant.log 2>&1; echo "exit $?" >> $R/planplant.log
python -u sonic_valley.py planplant $R/planplant_control.jsonl $RAW/I343-win2/states/lowD343_D3.043350_M320.npz \
    $RAW/T82-win/states/lowDhm_x0.000157-0.975_D3.0475_M320.npz --refine 4 --levels 2 --delta 1e-8 --threads 10 \
    --mutate norefine > $R/planplant_control.log 2>&1; echo "exit $?" >> $R/planplant_control.log
```

Criteria (fixed in `sonic_valley.py`'s docstring before the run): the first exits 0 (the truth nan on the coarse plan;
the truth moved by 1e-8 admitted by the coarse plan split 4 or 16 times near x = c; the truth finite on that plan; the
moved truth's residual on its own plan between 1e-10 and 1e-4), and the control exits 1. Expected from the Mac's
partial runs: own 1.170e-28, coarse nan, the moved truth nan at split 4, the truth 2.917e-21 at split 16.

**1. The starts (minutes).**

```
python -u sonic_valley.py startcase $R/startcase.jsonl \
    $RAW/T105-win2/states/lowDhm_x0.000157-0.975_p1_D3.0438_M320.npz \
    $RAW/I343-win2/states/lowD343_D3.0436_M320.npz $RAW/I343-win2/states/lowD343_D3.043350_M320.npz \
    --predict 3.04315 --plan own --tol_step 1e-32 --refine 4 --levels 2 --threads 10 > $R/startcase.log 2>&1
```

Expected, from I926-mac (M 320, same inputs): the predictor nan on the unsplit plan (#343's log: 7808 steps), the last
state 2.71e-2 there; the predictor finite on the plan split 4 times near x = c.

**2. The point (hours).**

```
python -u lowD_highM.py --start_w $RAW/I343-win2/states/lowD343_D3.043350_M320.npz \
    --start_n $RAW/I343-win2/states/lowD343_D3.043350_M384.npz --Ms 320,384 --dD 0.0002 --D_end 3.0431 \
    --min_step 0.00005 --diff_max 1e-8 --hours 60 --point_hours 30 --threads 10 \
    --states $R/states --out $R/leg.jsonl --points $R/leg_points.jsonl --resume --it_max 8 \
    --sonic_refine 4 --sonic_stop > $R/leg.log 2>&1
```

With `--resume` the progress file's tag (`lowD343`) names the new states; they go to `$R/states`, apart from #343's.

Criteria (each can fail):
1. At the start the log prints the gaps of the three M 384 history states (`sonic valley of the M 384 state`), and
   the leg does not stop before 3.04315 (the line through them must reach 0 below it).
2. M 320 at 3.04315: the predictor's |F| is nan on the reused plan and finite on the plan split 4 (or 16) times near
   x = c (`the refined plan is used`), and Newton converges (|F| below 1e-27) within the two passes; M 384 the same.
3. The pair is recorded with `sonic_gap_n`, the gap of the M 384 solution at 3.04315, which must lie within 20% of the
   value at 3.04315 of the line through the three M 384 gaps of criterion 1 (M 320's line gives 1.71e-6).
4. The control: the same setup in a second fresh folder R2 and the same command without `--sonic_refine 4`. Its M 320
   predictor stays nan and the solve falls back to the last state at |F| 2.7e-2, as in #343; stop it after its first
   Newton call.

Stops: a traceback; Newton at 8 calls in a pass without convergence (the script then halves the step to 3.04325,
which #343's leg2b may already hold; stop there and report); more than 30 h.
