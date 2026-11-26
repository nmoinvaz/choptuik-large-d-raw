# #1080 walk d, restart at iteration 1's point (the coordinator's order, 2026-11-26): gate on free memory, a float64 M = 5 start there
# from hier_nb (--fixA --schur, seeded with row 0's harmonics), the branch check (check_d2_start.py), then the old walk d is stopped by
# exact pid and the walk restarts from that start with a fresh cap. Stops without touching the old walk if any check fails.
$R = 'D:\choptuik-raw-i1080\I1080-win2\control_d'
$D2 = "$R\d2"
$PYEXE = 'C:\Users\nathan\source\venv-i962\Scripts\python.exe'
$MAINWT = 'D:\choptuik-i1080main'; $X2WT = 'D:\choptuik-i1080x2'; $WALKWT = 'D:\choptuik-i1080d'
$env:OMP_NUM_THREADS = '1'; $env:OPENBLAS_NUM_THREADS = '1'; $env:MKL_NUM_THREADS = '1'
function Step($s) { Add-Content -Path "$D2\steps_d2.txt" -Value ("{0} UTC {1}" -f [DateTime]::UtcNow.ToString('yyyy-MM-dd HH:mm:ss'), $s) }
function FreeGB { [math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1MB, 1) }
function Blob($wt, $rel) { (& git -C $wt hash-object --no-filters "$wt\$rel").Substring(0, 8) }
function Head8($wt) { (& git -C $wt rev-parse --short=8 HEAD) }
function RunBN($argv, $wd, $outf, $errf, $capS) {
    $q = Start-Process -FilePath $PYEXE -ArgumentList $argv -WorkingDirectory $wd -NoNewWindow -PassThru -RedirectStandardOutput $outf -RedirectStandardError $errf
    $null = $q.Handle
    $q.PriorityClass = 'BelowNormal'
    if (-not $q.WaitForExit($capS * 1000)) { & taskkill /T /F /PID $q.Id | Out-Null; return 'cap' }
    return $q.ExitCode
}
function Fail($why) { Step "STOP: $why"; Set-Content "$D2\D2_DONE.txt" "NOT RUN: $why"; exit 1 }

# pins
$pinMain = "$(Head8 $MAINWT) $(Blob $MAINWT 'solver\inner_stokes\hier_nb.py') $(Blob $MAINWT 'solver\inner_stokes\hier.py') $(Blob $MAINWT 'solver\inner_stokes\inner_nb.py')"
$pinX2 = "$(Head8 $X2WT) $(Blob $X2WT 'solver\inner_stokes\start_path.py') $(Blob $X2WT 'solver\inner_stokes\hier_nb.py') $(Blob $X2WT 'solver\inner_stokes\hier.py') $(Blob $X2WT 'solver\inner_stokes\inner_nb.py')"
$pinWalk = "$(Head8 $WALKWT) $(Blob $WALKWT 'solver\inner_stokes\zero_mp.py') $(Blob $WALKWT 'solver\inner_stokes\value_mp.py') $(Blob $WALKWT 'solver\inner_stokes\inner_mp.py')"
$pinRaw = "$((& git -C $WALKWT hash-object --no-filters "$D2\hier_nb_fulldigits.py").Substring(0, 8)) $((& git -C $WALKWT hash-object --no-filters "$R\control_check.py").Substring(0, 8))"
if ($pinMain -ne '57eda12c 68b287ec b4e4d887 53374669') { Fail "main pins read '$pinMain'" }
if ($pinX2 -ne '10a5854f 3788474f 30a15592 2e5461a2 53374669') { Fail "x2 pins read '$pinX2'" }
if ($pinWalk -ne '73dcf243 1077ea0e 56bb4856 563bc062') { Fail "walk pins read '$pinWalk'" }
if ($pinRaw -ne '64363623 483e9871') { Fail "raw pins read '$pinRaw'" }
if (Test-Path "$D2\control_walk_d2.jsonl") { Fail 'control_walk_d2.jsonl exists' }
& $PYEXE "$D2\check_d2_start.py" selftest > "$D2\logs\selftest_check_d2_start.txt" 2>&1; $sc = $LASTEXITCODE
if ($sc -ne 0) { Fail "check_d2_start selftest exit $sc" }
Step "pins ok: main $pinMain; x2 $pinX2; walk $pinWalk; raw $pinRaw; check_d2_start selftest exit 0; gate: free memory >= 20 GB twice 30 s apart (now $(FreeGB) GB)"

# gate
$tg = Get-Date; $okc = 0
while ($okc -lt 2) {
    if ((FreeGB) -ge 20) { $okc++ } else { $okc = 0 }
    if ($okc -lt 2) { Start-Sleep -Seconds 30 }
    if (((Get-Date) - $tg).TotalHours -gt 8) { Fail 'gate timeout, free memory stayed below 20 GB for 8 h' }
}
Step "gate open, free memory $(FreeGB) GB"

$info = (& $PYEXE "$D2\row0_info.py" "$R\control_walk_d.jsonl").Split('|')
$A0 = $info[0]; $W0 = $info[1]; $A1 = $info[2]; $W1 = $info[3]; $V0 = $info[4]
Step "row 0 point ($A0, $W0), iteration 1 point ($A1, $W1), seed v $V0"

# direct float64 start at the new point (dh370's step 1, seeded with row 0's harmonics)
$env:FULLDIGITS_OUT = "$D2\start_direct.json"
$rc1 = RunBN @('-u', "$D2\hier_nb_fulldigits.py", '5', $A1, $W1, "--x=$V0", '--fixA', '--schur', '--procs', '2', '--verbose=1', '--xi1=0.2') "$MAINWT\solver\inner_stokes" "$D2\logs\hier_nb_d2_start.log" "$D2\logs\hier_nb_d2_start.err" 3600
Remove-Item Env:\FULLDIGITS_OUT
Step "hier_nb direct start exit $rc1"
if ($rc1 -ne 0) { Fail "hier_nb direct start exit $rc1" }

# continuation from row 0's point to the new point (x2 worktree's start_path.py): 20 steps, 40 steps, and the control that ends 0.01 in A off
$spd = "$X2WT\solver\inner_stokes"
$rcA = RunBN @('-u', 'start_path.py', '5', $A0, $W0, $A1, $W1, "--v0=$V0", '--n=20', "--out=$D2\path_n20.jsonl") $spd "$D2\logs\path_n20.log" "$D2\logs\path_n20.err" 7200
$rcB = RunBN @('-u', 'start_path.py', '5', $A0, $W0, $A1, $W1, "--v0=$V0", '--n=40', "--out=$D2\path_n40.jsonl") $spd "$D2\logs\path_n40.log" "$D2\logs\path_n40.err" 7200
$rcC = RunBN @('-u', 'start_path.py', '5', $A0, $W0, $A1, $W1, "--v0=$V0", '--n=20', '--mutate=end', "--out=$D2\path_mut.jsonl") $spd "$D2\logs\path_mut.log" "$D2\logs\path_mut.err" 7200
Step "start_path exits: n20 $rcA, n40 $rcB, mutated $rcC (0 each wanted)"
if ($rcA -ne 0 -or $rcB -ne 0 -or $rcC -ne 0) { Fail "a start_path run did not exit 0" }

& $PYEXE "$D2\check_d2_start.py" "$R\control_walk_d.jsonl" "$D2\logs\hier_nb_d2_start.log" "$D2\start_direct.json" "$D2\path_n20.jsonl" "$D2\path_n40.jsonl" "$D2\path_mut.jsonl" > "$D2\check_d2_start.txt" 2>&1; $rcK = $LASTEXITCODE
Step ("check_d2_start exit $rcK (0 = PASS): " + ((Get-Content "$D2\check_d2_start.txt" | Select-Object -Last 2) -join ' | '))
if ($rcK -ne 0) { Fail 'the start check did not pass; the old walk is left running' }
$VS = (& $PYEXE "$D2\solved_v.py" "$D2\start_direct.json")

# walk selftests, then the switch
Push-Location "$WALKWT\solver\inner_stokes"
& $PYEXE zero_mp.py selftest > "$D2\logs\selftest_zero_mp_d2.txt" 2>&1; $s0 = $LASTEXITCODE
& $PYEXE zero_mp.py selftest --mutate=sign > "$D2\logs\selftest_zero_mp_d2_mutsign.txt" 2>&1; $s1 = $LASTEXITCODE
Pop-Location
Step "zero_mp selftest exit $s0 (0 wanted), --mutate=sign exit $s1 (1 wanted)"
if ($s0 -ne 0 -or $s1 -ne 1) { Fail 'a zero_mp selftest did not read as written; the old walk is left running' }
$oldCmd = (Get-CimInstance Win32_Process -Filter 'ProcessId=43332' -ErrorAction SilentlyContinue).CommandLine
if ($oldCmd -and $oldCmd -match 'run_control_d\.ps1') {
    & taskkill /T /F /PID 43332 | Out-Null
    Start-Sleep -Seconds 3
    $left = @(Get-Process -Id 43332, 35324, 48984 -ErrorAction SilentlyContinue).Count
    Step "old walk d stopped by exact pid (taskkill /T /F /PID 43332, the launcher; tree 35324, 48984); processes left: $left"
    Set-Content "$R\control_walk_d.exit" 'stopped for the restart in d2/'
} else { Step "old walk d launcher 43332 not found or not run_control_d.ps1 (already ended?): nothing to stop" }

$a = @('-u', 'zero_mp.py', $A1, $W1, '-', "$D2\control_walk_d2.jsonl", '--M=5', "--v0=$VS", '--procs=3', '--iters=7')
$p = Start-Process -FilePath $PYEXE -ArgumentList $a -WorkingDirectory "$WALKWT\solver\inner_stokes" -NoNewWindow -PassThru `
     -RedirectStandardOutput "$D2\logs\control_walk_d2.log" -RedirectStandardError "$D2\logs\control_walk_d2.err"
$null = $p.Handle
$p.PriorityClass = 'BelowNormal'
Step "walk d2 start pid $($p.Id), BelowNormal, cap 86400 s, v0 $VS"
Set-Content -Path "$D2\control_walk_d2.pid" -Value $p.Id
if (-not $p.WaitForExit(86400 * 1000)) { & taskkill /T /F /PID $p.Id | Out-Null; Step "CAP: killed pid $($p.Id) after 86400 s"; Set-Content "$D2\control_walk_d2.exit" 'cap'; exit 3 }
Step "walk d2 exit $($p.ExitCode)"
Set-Content -Path "$D2\control_walk_d2.exit" -Value $p.ExitCode
& $PYEXE "$R\control_check.py" "$D2\logs\control_walk_d2.log" "$D2\control_walk_d2.jsonl" > "$D2\control_check_d2.txt" 2>&1; $s3 = $LASTEXITCODE
Step ("control_check exit $s3 (0 = PASS): " + ((Get-Content "$D2\control_check_d2.txt" -TotalCount 1) -join ' '))
Set-Content -Path "$D2\D2_DONE.txt" -Value "walk exit $($p.ExitCode) check exit $s3"
