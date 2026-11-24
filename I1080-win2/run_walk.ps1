# #1080 x2: zero_mp.py's M = 5 walk from the polished start (v0 = logs/polish_x2.json's v, 42 digits), as walk d's
# command; selftest (0 wanted) and --mutate=sign (1 wanted) first. 5 processes, BelowNormal, cap 40 h. Rows walk_x2.jsonl.
$R = 'D:\choptuik-raw-i1080\I1080-win2'
$WT = 'D:\choptuik-i1080x2\solver\inner_stokes'
$PY = 'C:\Users\nathan\source\venv-i962\Scripts\python.exe'
$env:OMP_NUM_THREADS = '1'; $env:OPENBLAS_NUM_THREADS = '1'
function Step($s) { Add-Content -Path "$R\steps_walk.txt" -Value ("{0} UTC {1}" -f [DateTime]::UtcNow.ToString('yyyy-MM-dd HH:mm:ss'), $s) }
$head = (& git -C 'D:\choptuik-i1080x2' rev-parse --short=8 HEAD)
if ($head -ne 'dd00111a') { Step "STOP: HEAD $head, not dd00111a"; exit 9 }
if (Test-Path "$R\walk_x2.jsonl") { Step "STOP: walk_x2.jsonl exists"; exit 9 }
Push-Location $WT
& $PY zero_mp.py selftest > "$R\logs\selftest_zero_mp.txt" 2>&1; $s0 = $LASTEXITCODE
& $PY zero_mp.py selftest --mutate=sign > "$R\logs\selftest_zero_mp_mutsign.txt" 2>&1; $s1 = $LASTEXITCODE
$v0 = (& $PY -c "import json; print(','.join(json.loads(open(r'$R\logs\polish_x2.json').read().strip().splitlines()[-1])['v']))")
Pop-Location
Step "selftest exit $s0 (0 wanted), --mutate=sign exit $s1 (1 wanted); v0 $v0"
if ($s0 -ne 0 -or $s1 -ne 1) { Step "STOP: a selftest did not read as written"; exit 1 }
$a = @('-u', 'zero_mp.py', '3.526473056695715', '0.211497981391215', '-', "$R\walk_x2.jsonl", '--M=5', "--v0=$v0", '--procs=5', '--iters=8')
$p = Start-Process -FilePath $PY -ArgumentList $a -WorkingDirectory $WT -NoNewWindow -PassThru `
     -RedirectStandardOutput "$R\logs\walk_x2.log" -RedirectStandardError "$R\logs\walk_x2.err"
$null = $p.Handle                                # keeps the exit code readable after the wait
$p.PriorityClass = 'BelowNormal'
Step "walk start pid $($p.Id), BelowNormal, cap 144000 s"
Set-Content -Path "$R\walk_x2.pid" -Value $p.Id
$done = $p.WaitForExit(144000 * 1000)
if (-not $done) { & taskkill /T /F /PID $p.Id | Out-Null; Step "CAP: killed pid $($p.Id) after 144000 s"; Set-Content "$R\walk_x2.exit" 'cap'; exit 3 }
Step "walk exit $($p.ExitCode), cpu (launcher tree) $([int]$p.TotalProcessorTime.TotalSeconds) s"
Set-Content -Path "$R\walk_x2.exit" -Value $p.ExitCode
