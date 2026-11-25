# #1080 control walk d on win2, dh370's command (raw I1080-dh370 README, step 2) on feat/inner-mp 73dcf243, 3 procs, BelowNormal, cap 24 h.
# Checks first (worktree and blob pins, no earlier rows), then the three selftests (0, 1, 0 wanted), then the walk, then control_check.py.
$R = 'D:\choptuik-raw-i1080\I1080-win2\control_d'
$GITDIR = 'D:\choptuik-i1080d'
$WT = "$GITDIR\solver\inner_stokes"
$PYEXE = 'C:\Users\nathan\source\venv-i962\Scripts\python.exe'
$env:OMP_NUM_THREADS = '1'; $env:OPENBLAS_NUM_THREADS = '1'; $env:MKL_NUM_THREADS = '1'
function Step($s) { Add-Content -Path "$R\steps_control_d.txt" -Value ("{0} UTC {1}" -f [DateTime]::UtcNow.ToString('yyyy-MM-dd HH:mm:ss'), $s) }
function Blob($p) { (& git -C $GITDIR hash-object --no-filters $p).Substring(0, 8) }
$head = (& git -C $GITDIR rev-parse --short=8 HEAD)
$pins = "$head $(Blob "$WT\zero_mp.py") $(Blob "$WT\value_mp.py") $(Blob "$WT\inner_mp.py") $(Blob "$R\control_check.py")"
if ($pins -ne '73dcf243 1077ea0e 56bb4856 563bc062 483e9871') { Step "STOP: pins read '$pins'"; Set-Content "$R\CONTROL_D_DONE.txt" 'NOT RUN'; exit 9 }
if (Test-Path "$R\control_walk_d.jsonl") { Step "STOP: control_walk_d.jsonl exists"; exit 9 }
Push-Location $WT
& $PYEXE zero_mp.py selftest > "$R\logs\selftest_zero_mp_d.txt" 2>&1; $s0 = $LASTEXITCODE
& $PYEXE zero_mp.py selftest --mutate=sign > "$R\logs\selftest_zero_mp_d_mutsign.txt" 2>&1; $s1 = $LASTEXITCODE
& $PYEXE "$R\control_check.py" selftest > "$R\logs\selftest_control_check_d.txt" 2>&1; $s2 = $LASTEXITCODE
$ver = (& $PYEXE -c "import sys, mpmath; print(sys.version.split()[0], 'mpmath', mpmath.__version__, mpmath.libmp.BACKEND)")
Pop-Location
Step "pins $pins; $ver; zero_mp.py selftest exit $s0 (0 wanted), with --mutate=sign exit $s1 (1 wanted); control_check selftest exit $s2 (0 wanted)"
if ($s0 -ne 0 -or $s1 -ne 1 -or $s2 -ne 0) { Step "STOP: a selftest or its mutation did not read as written"; Set-Content "$R\CONTROL_D_DONE.txt" 'NOT RUN'; exit 1 }
$a = @('-u', 'zero_mp.py', '2.726475885672135', '1.0156030949093042', '-', "$R\control_walk_d.jsonl", '--M=5',
       '--v0=0.14617320927726193,0.014239435701575993,0.008040315603426431,0.0013895510043319215', '--procs=3', '--iters=8')
$p = Start-Process -FilePath $PYEXE -ArgumentList $a -WorkingDirectory $WT -NoNewWindow -PassThru `
     -RedirectStandardOutput "$R\logs\control_walk_d.log" -RedirectStandardError "$R\logs\control_walk_d.err"
$null = $p.Handle                                # keeps the exit code readable after the wait
$p.PriorityClass = 'BelowNormal'
Step "walk start pid $($p.Id), BelowNormal, cap 86400 s"
Set-Content -Path "$R\control_walk_d.pid" -Value $p.Id
$done = $p.WaitForExit(86400 * 1000)
if (-not $done) { & taskkill /T /F /PID $p.Id | Out-Null; Step "CAP: killed pid $($p.Id) after 86400 s"; Set-Content "$R\control_walk_d.exit" 'cap'; exit 3 }
Step "walk exit $($p.ExitCode)"
Set-Content -Path "$R\control_walk_d.exit" -Value $p.ExitCode
& $PYEXE "$R\control_check.py" "$R\logs\control_walk_d.log" "$R\control_walk_d.jsonl" > "$R\control_check_d.txt" 2>&1; $s3 = $LASTEXITCODE
Step ("control_check exit $s3 (0 = PASS): " + ((Get-Content "$R\control_check_d.txt" -TotalCount 1) -join ' '))
Set-Content -Path "$R\CONTROL_D_DONE.txt" -Value "walk exit $($p.ExitCode) check exit $s3"
