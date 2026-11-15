# #737 on win (the coordinator): the horizon series' transient at M = 32 against M = 48 at D 80 and 100.
# Quad-double terms to order 250 (horizon_radius.py run), at delta 0 and 1e-28 (a_h scaled by 1 + delta), from
# T138-win2's M = 32 chain states and #636's M = 48 solutions of them. Worktree choptuik-i737 at main 0209d4d2,
# venv-t179 (the horizon series does not use the freeze projector, so this build gives main's terms). 6 threads.
$py = "C:\Users\nathan\Source\venv-t179\Scripts\python.exe"
$B = "C:\Users\nathan\scratch737"
$R = "C:\Users\nathan\Source\choptuik-large-d-raw\I737-win"
$env:OPENBLAS_NUM_THREADS = "1"
$env:PYTHONFAULTHANDLER = "1"
cd C:\Users\nathan\Source\choptuik-i737\hp
if ((git rev-parse --short=8 HEAD) -ne "0209d4d2") { "737 worktree is not at 0209d4d2" | Add-Content "$R\exits_737.txt"; exit 9 }
function Log($s) { "737 $s $((Get-Date).ToUniversalTime().ToString('yyyy-MM-dd HH:mm:ss')) UTC" | Add-Content "$R\exits_737.txt" }
function Step($name, $argv) {
  Log "$name start"
  & $py -u @argv *> "$R\$name.log"
  Log "$name exit $LASTEXITCODE"
  return $LASTEXITCODE
}
# step 0: the planted checks (each mutation must fail)
Step "selftest" @("horizon_radius.py", "selftest") | Out-Null
Step "selftest_drop_term" @("horizon_radius.py", "selftest", "--mutate", "drop_term") | Out-Null
Step "table_selftest" @("-I", "$R\table737.py", "--selftest") | Out-Null
# step 1: horizon_radius's controls on real data at D 80, M = 32 (they use the octo-double solver, which is M = 32 only;
# the M = 48 series run in quad-double)
Step "control_m32_D80" @("horizon_radius.py", "control", "$B\T138-win2\chain\anm_pin3_D80.0000.npz", "--threads", "6") | Out-Null
# step 2: the series, M = 32 then M = 48, at delta 0 and 1e-28
foreach ($D in @("80.0000", "100.0000")) {
  Step "run_m32_D$D" @("horizon_radius.py", "run", "$R\m32.jsonl", "$B\T138-win2\chain\anm_pin3_D$D.npz", "--kmax", "250", "--precs", "qd", "--deltas", "0,1e-28", "--threads", "6", "--coef", "$R\c32") | Out-Null
}
Step "run_m48_D80.0000" @("horizon_radius.py", "run", "$R\m48.jsonl", "$B\I636-mac\planted\m48_anm_pin3_D80.0000.npz", "--kmax", "250", "--precs", "qd", "--deltas", "0,1e-28", "--threads", "6", "--coef", "$R\c48") | Out-Null
Step "run_m48_D100.0000" @("horizon_radius.py", "run", "$R\m48.jsonl", "$B\I636-mac\chain\m48_anm_pin3_D100.0000.npz", "--kmax", "250", "--precs", "qd", "--deltas", "0,1e-28", "--threads", "6", "--coef", "$R\c48") | Out-Null
# step 3: the table, and its mutation (must read the grid's)
Step "table737" @("-I", "$R\table737.py", "$R\c32", "$R\c48") | Out-Null
Step "table737_scale48" @("-I", "$R\table737.py", "$R\c32", "$R\c48", "--mutate=scale48") | Out-Null
Log "all done"
